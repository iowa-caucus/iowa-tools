#!/usr/bin/env python

import argparse

from bs4 import BeautifulSoup

from iowa_tools.constants import ST_FULL, ST_VOTES, ST_SDES, ST_TOTALS, ST_SDE_COUNTY_TOTALS, PRECINCT, COUNTY
from iowa_tools.dataframe import split_dataframe
from iowa_tools.formats import JsonDataset, convert_json_to_dataframe
from iowa_tools.io import write_dataset_as_json, write_dataset_as_csv, get_html_filename, \
    open_input_reference_file, write_json


def parse_iowa_html(ipd_ref_dataset):
    headers = []
    data = []

    with open_input_reference_file(get_html_filename(ipd_ref_dataset)) as idp_file:
        soup  = BeautifulSoup(idp_file, features='lxml')
        table = soup.select_one('.precinct-table')
        thead = table.select_one('.thead')
        shead = table.select_one('.sub-head')

        prev_tstr = None
        for titem in (e for e in thead.children if not isinstance(e, str)):
            tstr = titem.string.strip() if titem.string else None
            if tstr:
                prev_tstr = tstr
            else:
                tstr = prev_tstr
            headers.append([tstr])
        for i, sitem in enumerate(e for e in shead.children
                                    if not isinstance(e, str)):
            sstr = sitem.string.strip() if sitem.string else None
            if sstr:
                headers[i].append(sstr)

        for county_row in table.select('.precinct-rows'):
            county_item = county_row.select_one('.precinct-county')
            county      = ''.join(county_item.strings).strip()
            for row in county_row.select('ul'):
                item_iter = iter(row.select('li'))
                precinct  = next(item_iter).string.strip()
                data_row = {
                    headers[0][0]:   county,
                    headers[1][0]: precinct,
                }
                for i, item in enumerate(item_iter):
                    candidate, stat_name = headers[i+2]
                    vstr = item.string.replace(',', '')
                    try:
                        val = int(vstr)
                    except ValueError:
                        val = float(vstr)
                    stats = data_row.setdefault(stat_name, {})
                    stats[candidate] = val
                data.append(data_row)

                n = len(data)
                if n % 100 == 0:
                    print(n)

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
