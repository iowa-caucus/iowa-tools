#!/usr/bin/env python

import argparse
import re
from collections import OrderedDict

import dpath.util as du

from iowa_tools.constants import ST_FULL, ST_VOTES, ST_SDES, ST_TOTALS, ST_SDE_COUNTY_TOTALS, PRECINCT, COUNTY
from iowa_tools.dataframe import split_dataframe
from iowa_tools.formats import JsonDataset, convert_json_to_dataframe
from iowa_tools.io import write_dataset_as_json, write_dataset_as_csv, get_html_filename, \
    open_input_reference_file, write_json


def parse_iowa_html(ipd_ref_dataset):
    headers = []
    data = []

    with open_input_reference_file(get_html_filename(ipd_ref_dataset)) as idp_file:
        for i, line in enumerate(idp_file):
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
                            val = item.replace('&amp;', '&')

                        assert col_idx != 0
                        if col_idx == 1:
                            cur_precinct = item
                            cur_row = OrderedDict()
                            cur_row[headers[0][0]] = cur_county
                            cur_row[headers[1][0]] = cur_precinct
                            data.append(cur_row)

                        du.new(cur_row, list(reversed(headers[col_idx])), val)

                    col_idx += 1

    json_dataset = JsonDataset(data, headers)
    full_df = convert_json_to_dataframe(json_dataset)
    votes_df, sdes_df, totals_df, sde_totals_df = split_dataframe(full_df)

    votes_df = votes_df.sort_values([COUNTY, PRECINCT], ascending=True)
    sdes_df = sdes_df.sort_values([COUNTY, PRECINCT], ascending=True)
    totals_df = totals_df.sort_values([COUNTY, PRECINCT], ascending=True)
    sde_totals_df = sde_totals_df.sort_values([COUNTY, PRECINCT], ascending=True)

    write_json(json_dataset, ipd_ref_dataset, ST_FULL)

    write_dataset_as_csv(full_df, ipd_ref_dataset, ST_FULL)
    write_dataset_as_csv(votes_df, ipd_ref_dataset, ST_VOTES)
    write_dataset_as_csv(sdes_df, ipd_ref_dataset, ST_SDES)
    write_dataset_as_csv(totals_df, ipd_ref_dataset, ST_TOTALS)
    write_dataset_as_csv(sde_totals_df, ipd_ref_dataset, ST_SDE_COUNTY_TOTALS)

    write_dataset_as_json(votes_df, ipd_ref_dataset, ST_VOTES)
    write_dataset_as_json(sdes_df, ipd_ref_dataset, ST_SDES)
    write_dataset_as_json(totals_df, ipd_ref_dataset, ST_TOTALS)
    write_dataset_as_json(sde_totals_df, ipd_ref_dataset, ST_SDE_COUNTY_TOTALS)


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
    parser.add_argument('ipd_ref_dataset')
    args = parser.parse_args()

    parse_iowa_html(args.idp_ref_dataset)


if __name__ == "__main__":
    main()
