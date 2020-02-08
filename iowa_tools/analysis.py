#!/usr/bin/env python

import argparse
import sys
import pandas as pd

from iowa_tools.common import read_dataframe, write_dataframe_as_json, write_dataframe_as_csv
from iowa_tools.constants import FIRST, FINAL, INC_VOTES, VOTES, MORE_VOTES


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


def main():
    parser = argparse.ArgumentParser(description='Misc analyses')
    parser.add_argument('analysis', choices=['more_final_votes'])
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')
    args = parser.parse_args()

    getattr(sys.modules[__name__], args.analysis)(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
