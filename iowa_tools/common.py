import json
import os
from collections import OrderedDict

import dpath.util as du
import pandas as pd

from iowa_tools.constants import SDE, TOTAL, JSON_DATA_SUFFIX, JSON_HEADERS_SUFFIX, VOTES, \
    STD_COL_ORDER, CSV_SUFFIX


def read_dataframe(out_dir, name=VOTES):
    data_fn, headers_fn = get_json_filenames(name)
    with open(os.path.join(out_dir, headers_fn), 'r') as headerfile:
        with open(os.path.join(out_dir, data_fn), 'r') as datafile:
            headers_fn = json.load(headerfile)
            data_fn = json.load(datafile)
            df = pd.json_normalize(data_fn, meta=headers_fn)
            df = df.set_index(headers_fn[0] + headers_fn[1])  # use county and prefix and index
            df.columns = df.columns.str.split('.', expand=True)  # create hierarchical columns
            return df


def get_json_filenames(name):
    data_fn = name + JSON_DATA_SUFFIX
    headers_fn = name + JSON_HEADERS_SUFFIX
    return data_fn, headers_fn


def split_dataframe(df, move_rows=[TOTAL], move_cols=[SDE], row_level=1, col_level=0):
    mv_rows = select_from_labels(df, move_rows, axis=0, level=row_level)
    kp_rows = select_from_labels(df, move_rows, axis=0, level=row_level, invert=True)
    mv_cols = select_from_labels(df, move_cols, axis=1, level=col_level)
    kp_cols = select_from_labels(df, move_cols, axis=1, level=col_level, invert=True)

    kp_df = extract_subtable_by_labels(df, kp_rows, kp_cols, row_level, col_level)
    new_row_df = extract_subtable_by_labels(df, kp_rows, mv_cols, row_level, col_level)
    new_col_df = extract_subtable_by_labels(df, mv_rows, kp_cols, row_level, col_level)
    new_row_col_df = extract_subtable_by_labels(df, mv_rows, mv_cols, row_level, col_level)

    return kp_df, new_row_df, new_col_df, new_row_col_df


def select_from_labels(df, labels, axis, level, invert=False):
    assert axis in [0, 1]
    assert level in [0, 1]

    idx = df.index.levels[level] if axis == 0 else df.columns.levels[level]
    filtered_idx = idx[~idx.isin(labels)] if invert else idx[idx.isin(labels)]
    formatted_idx = tuple(filtered_idx)
    return formatted_idx


def extract_subtable_by_labels(df, row_labels=None, col_labels=None, row_level=0, col_level=0):
    if row_labels:
        rows = [df.xs(row, axis=0, level=row_level, drop_level=False) for row in row_labels]
        df = pd.concat(rows)
    if col_labels:
        cols = [df.xs(col, axis=1, level=col_level, drop_level=False) for col in col_labels]
        df = pd.concat(cols, axis=1)
    return df


def convert_dataframe_to_dict(df):
    temp_dict = df.to_dict(orient='index')

    out = []
    for county_precinct, cols in temp_dict.items():
        row = OrderedDict()
        row[df.index.names[0]] = county_precinct[0]
        row[df.index.names[1]] = county_precinct[1]
        
        top_headers = list(set(header[0] for header in cols.keys()))
        sort_top_headers_according_to_std(top_headers)
        for top_header in top_headers:
            row[top_header] = OrderedDict()

        for header, val in sorted(cols.items()):
            if header[1] == '':
                header = [header[0]]
            du.new(row, list(header), val)
        out.append(row)

    return out


def sort_top_headers_according_to_std(top_headers):
    col_order = STD_COL_ORDER + sorted([_ for _ in top_headers if _ not in STD_COL_ORDER])
    return top_headers.sort(key=lambda x: col_order.index(x))


def write_dataframe_as_json(df, out_dir, name):
    df_dict = convert_dataframe_to_dict(df)
    header_list = [[header] for header in df.index.names] + list(df.columns)
    data_fn, header_fn = get_json_filenames(name)
    write_json(df_dict, out_dir, data_fn)
    write_json(header_list, out_dir, header_fn)


def write_dataframe_as_csv(df, out_dir, name):
    csv_content = df.to_csv()
    with open(os.path.join(out_dir, name + CSV_SUFFIX), 'w') as out_csv:
        out_csv.write(csv_content)


def write_all(obj_dict, out_dir):
    for name, obj in obj_dict.items():
        write_json(obj, out_dir, name)


def write_json(obj, out_dir, file_name):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, file_name), 'w') as json_file:
        json_file.write(json.dumps(obj, indent=4))
