from collections import OrderedDict, namedtuple

import pandas as pd
from dpath import util as du

from iowa_tools.constants import STD_COL_ORDER


# Data structures

JsonDataset = namedtuple('JsonDataset', ('data', 'headers'))


# Functions

def convert_dataframe_to_dict(df):
    temp_dict = df.to_dict(orient='index', into=OrderedDict)

    out = []
    for county_precinct, cols in temp_dict.items():
        row = OrderedDict()
        row[df.index.names[0]] = county_precinct[0]
        row[df.index.names[1]] = county_precinct[1]

        for top_header in list(set(header[0] for header in cols.keys())):
            row[top_header] = OrderedDict()

        for header, val in sorted(cols.items()):
            if header[1] == '':
                header = [header[0]]
            du.new(row, list(header), val)
        out.append(row)

    return out


def convert_dataframe_to_json(df):
    df = df.reindex(sort_top_headers_according_to_std(df.columns.levels[0]), level=0, axis=1)
    df_dict = convert_dataframe_to_dict(df)
    header_list = [[header] for header in df.index.names] + list(df.columns)
    return JsonDataset(df_dict, header_list)


def convert_dataframe_to_csv(df):
    df = df.reindex(sort_top_headers_according_to_std(df.columns.levels[0]), level=0, axis=1)
    csv_content = df.to_csv()
    return csv_content


def convert_json_to_dataframe(json_dataset):
    data, headers = json_dataset
    df = pd.json_normalize(data, meta=headers)
    df = df.set_index(headers[0] + headers[1])  # use county and prefix and index
    df.columns = df.columns.str.split('.', expand=True)  # create hierarchical columns
    return df


def convert_csv_to_dataframe(csv_content):
    pass


# Util functions

def sort_top_headers_according_to_std(top_headers):
    col_order = STD_COL_ORDER + sorted([_ for _ in top_headers if _ not in STD_COL_ORDER])
    return sorted(top_headers, key=lambda x: col_order.index(x))
