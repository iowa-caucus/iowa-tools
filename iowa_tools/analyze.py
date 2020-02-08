#!/usr/bin/env python

import argparse
import sys
from collections import OrderedDict

import pandas as pd

from iowa_tools.common import read_dataframe, write_dataframe_as_json, write_dataframe_as_csv
from iowa_tools.constants import FIRST, FINAL, INC_VOTES, VOTES, MORE_VOTES, COUNTY, \
    DOCUMENTATION_URL, VALIDATED


def more_final_votes(input_dir, output_dir):
    df = read_dataframe(input_dir, VOTES)

    first_votes = df[FIRST].sum(axis=1)
    final_votes = df[FINAL].sum(axis=1)
    diff_votes = final_votes - first_votes

    df[INC_VOTES] = diff_votes
    more_votes_df = df[diff_votes > 0]
    more_votes_df = more_votes_df.sort_values(INC_VOTES, ascending=False)

    write_dataframe_as_json(more_votes_df, output_dir, MORE_VOTES)
    write_dataframe_as_csv(more_votes_df, output_dir, MORE_VOTES)


def generate_validation_files(input_dir, output_dir):
    df = read_dataframe(input_dir, VOTES)
    df[DOCUMENTATION_URL] = ""
    df[VALIDATED] = "false"

    dfs = OrderedDict([(county, _) for county, _ in df.groupby(COUNTY)])

    for county, df in dfs.items():
        name = county.lower().replace(' ', '_')
        write_dataframe_as_json(df, output_dir, name)
        write_dataframe_as_csv(df, output_dir, name)


def main():
    parser = argparse.ArgumentParser(description='Misc analyses')
    parser.add_argument('analysis', choices=['more_final_votes', 'generate_validation_files'])
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')
    args = parser.parse_args()

    getattr(sys.modules[__name__], args.analysis)(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
