#!/usr/bin/env python

import argparse
import sys
from collections import OrderedDict

import pandas as pd

from iowa_tools.constants import FIRST, FINAL, INC_VOTES, VOTES, MORE_VOTES, COUNTY, \
    DOCUMENTATION_URL, VALIDATED, IDP_PRECINCT_DELEGATES, GOP_2008_RESULTS, \
    SPSTEVE_PRECINCT_DELEGATES, PRECINCT_SN, MAPPING, SDE_PRECINCT_TOTALS, SDES, TOTAL_SDE
from iowa_tools.io import read_dataset_from_json, read_reference_dataset_from_csv, \
    write_dataset_as_json, write_dataset_as_csv


ANALYSES = [
    'more_final_votes',
    'generate_validation_files',
    'harmonize_precinct_metadata'
]


def more_final_votes(input_dataset, output_dataset):
    df = read_dataset_from_json(input_dataset, VOTES)

    first_votes = df[FIRST].sum(axis=1)
    final_votes = df[FINAL].sum(axis=1)
    diff_votes = final_votes - first_votes

    df[INC_VOTES] = diff_votes
    more_votes_df = df[diff_votes > 0]
    more_votes_df = more_votes_df.sort_values(INC_VOTES, ascending=False)

    write_dataset_as_json(more_votes_df, output_dataset, MORE_VOTES)
    write_dataset_as_csv(more_votes_df, output_dataset, MORE_VOTES)


def generate_validation_files(input_dataset, output_dataset):
    df = read_dataset_from_json(input_dataset, VOTES)

    df[DOCUMENTATION_URL] = ""
    df[VALIDATED] = "false"

    dfs = OrderedDict([(county, _) for county, _ in df.groupby(COUNTY)])

    for county, df in dfs.items():
        subtype = county.lower().replace(' ', '_')
        write_dataset_as_json(df, output_dataset, subtype)
        write_dataset_as_csv(df, output_dataset, subtype)


def harmonize_precinct_metadata(input_dataset, output_dataset):
    idp_df = read_reference_dataset_from_csv(IDP_PRECINCT_DELEGATES)
    gop_df = read_reference_dataset_from_csv(GOP_2008_RESULTS, index_cols=(19, 20))
    spsteve_df = read_reference_dataset_from_csv(SPSTEVE_PRECINCT_DELEGATES)

    gop_df.drop(gop_df.columns[20], axis=1, inplace=True)
    gop_df.drop(gop_df.columns[range(1, 18)], axis=1, inplace=True)
    spsteve_df.drop(spsteve_df.columns[range(0, 2)], axis=1, inplace=True)

    join_df = idp_df.join(gop_df, on=(COUNTY, PRECINCT_SN))
    join_df = join_df.join(spsteve_df, on=(COUNTY, PRECINCT_SN))
    join_df = join_df.sort_values([COUNTY, PRECINCT_SN], ascending=True)

    write_dataset_as_csv(join_df, output_dataset, MAPPING)

    sdes_df = read_dataset_from_json(input_dataset, SDES)
    guthrie_df = sdes_df.loc['Guthrie'].sum(axis=1).to_frame(TOTAL_SDE)
    write_dataset_as_csv(guthrie_df, output_dataset, 'guthrie_' + SDE_PRECINCT_TOTALS)


def main():
    parser = argparse.ArgumentParser(description='Misc analyses')
    parser.add_argument('analysis', choices=ANALYSES)
    parser.add_argument('input_dataset')
    parser.add_argument('output_dataset')
    args = parser.parse_args()

    getattr(sys.modules[__name__], args.analysis)(args.input_dataset, args.output_dataset)


if __name__ == "__main__":
    main()
