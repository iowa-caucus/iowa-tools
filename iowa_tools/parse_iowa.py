#!/usr/bin/env python

import argparse
import re
import dpath.util as du

from iowa_tools.common import write_all, get_json_filenames, read_dataframe, split_dataframe, \
    write_dataframe_as_json, write_dataframe_as_csv
from iowa_tools.constants import FULL, VOTES, SDES, TOTALS, SDE_TOTALS, PRECINCT, COUNTY


def parse_iowa_html(idp_html_file, out_dir):
    headers = []
    data = []

    with open(idp_html_file, 'r') as iowa:
        for i, line in enumerate(iowa):
            line = line.strip()
            if i % 100 == 0:
                print(i)

            if 'thead' in line:
                row_idx = -2
                col_idx = 0
                continue
            elif 'sub-head' in line:
                row_idx = -1
                col_idx = 0
                continue
            elif 'precinct-rows' in line:
                row_idx += 1
                col_idx = 0
                continue
            elif '<ul' in line:
                row_idx += 1
                col_idx = 1
                continue
            else:
                county_list = re.findall('<div class="wrap">(.+)</div>', line)
                if county_list and len(county_list) == 1:
                    cur_county = county_list[0]
                    continue

                list_item = re.findall('<li>(.*)</li>', line)
                if list_item and len(list_item) == 1:
                    item = list_item[0]

                    if row_idx == -2:  # Main header
                        headers.append([item] if item else [headers[col_idx-1][0]])
                    elif row_idx == -1:  # Subheader
                        if item:
                            headers[col_idx].append(item)
                    else:  # Row
                        if item.replace(',', '').isdigit():
                            val = int(item.replace(',', ''))
                        elif item.replace('.', '', 1).isdigit():
                            val = float(item)
                        else:
                            val = item

                        assert col_idx != 0
                        if col_idx == 1:
                            cur_precinct = item
                            cur_row = dict()
                            cur_row[headers[0][0]] = cur_county
                            cur_row[headers[1][0]] = cur_precinct
                            data.append(cur_row)

                        du.new(cur_row, list(reversed(headers[col_idx])), val)

                    col_idx += 1

    data_fn, headers_fn = get_json_filenames(FULL)
    write_all({data_fn: data, headers_fn: headers}, out_dir=out_dir)

    full_df = read_dataframe(out_dir, FULL)
    votes_df, sdes_df, totals_df, sde_totals_df = split_dataframe(full_df)

    votes_df = votes_df.sort_values([COUNTY, PRECINCT], ascending=True)

    write_dataframe_as_csv(votes_df, out_dir, VOTES)
    write_dataframe_as_csv(sdes_df, out_dir, SDES)
    write_dataframe_as_csv(totals_df, out_dir, TOTALS)
    write_dataframe_as_csv(sde_totals_df, out_dir, SDE_TOTALS)

    write_dataframe_as_json(votes_df, out_dir, VOTES)
    write_dataframe_as_json(sdes_df, out_dir, SDES)
    write_dataframe_as_json(totals_df, out_dir, TOTALS)
    write_dataframe_as_json(sde_totals_df, out_dir, SDE_TOTALS)


def main():
    parser = argparse.ArgumentParser(
        description='Parses HTML extract (the "precinct-table" div) from Iowa 2020 Democreatic '
                    'caucus result page: "https://results.thecaucuses.org/". Writes three JSON '
                    'files in output directory of choice: '
                    '"headers.json" is a list of column headers (possibly including subheaders). '
                    '"rows.json" is a json structure organized with the following hierarchy: '
                    'county->precinct->header(->subheader)->value.'
                    '"cols.json" is a json structure organized with the following hierarchy: '
                    'header(->subheader)->county->precinct->list of values')
    parser.add_argument('iowa_html_file', type=argparse.FileType('r'))
    parser.add_argument('out_dir')
    args = parser.parse_args()

    parse_iowa_html(args.iowa_html_file.name, args.out_dir)


if __name__ == "__main__":
    main()
