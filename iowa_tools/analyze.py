#!/usr/bin/env python

import argparse
import sys
from collections import OrderedDict

import pandas as pd

from iowa_tools.constants import FIRST, FINAL, INC_VOTES, ST_VOTES, ST_MORE_VOTES, COUNTY, \
    DOCUMENTATION_URL, VALIDATED, IDP_PRECINCT_DELEGATES, GOP_2008_RESULTS, \
    SPSTEVE_PRECINCT_DELEGATES, PRECINCT_SN, ST_MAPPING, ST_SDE_PRECINCT_TOTALS, ST_SDES, \
    TOTAL_SDE, DUPLICATE, ST_FIRST_DUPLICATES, ST_FINAL_DUPLICATES, ST_FIRST_FINAL_DUPLICATES, \
    ST_SDE_DUPLICATES, ST_FINAL_SDE_DUPLICATES, ST_FIRST_FINAL_SDE_DUPLICATES, DUP_FINAL, \
    DUP_FIRST, DUP_FIRST_FINAL, DUP_SDE, DUP_FINAL_SDE, DUP_FULL, DUP_ANY, ST_ALL_DUPLICATES, \
    ST_ALL_DUPLICATES_MINUS_SDE, DUP_ANY_MINUS_SDE
from iowa_tools.dataframe import extract_subtable_by_labels
from iowa_tools.io import read_dataset_from_json, read_reference_dataset_from_csv, \
    write_dataset_as_json, write_dataset_as_csv


ANALYSES = [
    'more_final_votes',
    'generate_validation_files',
    'harmonize_precinct_metadata',
    'duplicated_precincts'
]


def more_final_votes(input_dataset, output_dataset):
    df = read_dataset_from_json(input_dataset, ST_VOTES)

    first_votes = df[FIRST].sum(axis=1)
    final_votes = df[FINAL].sum(axis=1)
    diff_votes = final_votes - first_votes

    df[INC_VOTES] = diff_votes
    more_votes_df = df[diff_votes > 0]
    more_votes_df = more_votes_df.sort_values(INC_VOTES, ascending=False)

    write_dataset_as_json(more_votes_df, output_dataset, ST_MORE_VOTES)
    write_dataset_as_csv(more_votes_df, output_dataset, ST_MORE_VOTES)


def generate_validation_files(input_dataset, output_dataset):
    df = read_dataset_from_json(input_dataset, ST_VOTES)

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

    gop_df.drop(gop_df.columns[range(23, 26)], axis=1, inplace=True)
    gop_df.drop(gop_df.columns[range(17, 22)], axis=1, inplace=True)
    gop_df.drop(gop_df.columns[range(0, 8)], axis=1, inplace=True)
    spsteve_df.drop(spsteve_df.columns[range(0, 2)], axis=1, inplace=True)

    join_df = idp_df.join(gop_df, on=(COUNTY, PRECINCT_SN))
    join_df = join_df.join(spsteve_df, on=(COUNTY, PRECINCT_SN))
    join_df = join_df.sort_values([COUNTY, PRECINCT_SN], ascending=True)

    write_dataset_as_csv(join_df, output_dataset, ST_MAPPING)

    sdes_df = read_dataset_from_json(input_dataset, ST_SDES)
    guthrie_df = sdes_df.loc['Guthrie'].sum(axis=1).to_frame(TOTAL_SDE)
    write_dataset_as_csv(guthrie_df, output_dataset, 'guthrie_' + ST_SDE_PRECINCT_TOTALS)


def duplicated_precincts(input_dataset, output_dataset):
    votes_df = read_dataset_from_json(input_dataset, ST_VOTES)
    sdes_df = read_dataset_from_json(input_dataset, ST_SDES)
    full_df = votes_df.join(sdes_df)

    first_duplicated_df = extract_subtable_by_labels(votes_df, col_labels=[FIRST], col_level=0)
    final_duplicated_df = extract_subtable_by_labels(votes_df, col_labels=[FINAL], col_level=0)
    votes_duplicated_df = votes_df.copy()
    sdes_duplicated_df = sdes_df.copy()
    final_sdes_duplicated_df = final_duplicated_df.join(sdes_df)
    full_duplicated_df = full_df.copy()
    all_duplications_minus_sde_df = full_df.copy()

    first_duplicated_df[DUPLICATE, DUP_FIRST] = first_duplicated_df.duplicated(keep=False)
    final_duplicated_df[DUPLICATE, DUP_FINAL] = final_duplicated_df.duplicated(keep=False)
    votes_duplicated_df[DUPLICATE, DUP_FIRST_FINAL] = votes_duplicated_df.duplicated(keep=False)
    sdes_duplicated_df[DUPLICATE, DUP_SDE] = sdes_duplicated_df.duplicated(keep=False)
    final_sdes_duplicated_df[DUPLICATE, DUP_FINAL_SDE] = final_sdes_duplicated_df.duplicated(keep=False)
    full_duplicated_df[DUPLICATE, DUP_FULL] = full_duplicated_df.duplicated(keep=False)

    all_duplications_minus_sde_df[DUPLICATE, DUP_FIRST] = first_duplicated_df[DUPLICATE, DUP_FIRST].copy()
    all_duplications_minus_sde_df[DUPLICATE, DUP_FINAL] = final_duplicated_df[DUPLICATE, DUP_FINAL].copy()
    all_duplications_minus_sde_df[DUPLICATE, DUP_FIRST_FINAL] = votes_duplicated_df[DUPLICATE, DUP_FIRST_FINAL].copy()
    all_duplications_minus_sde_df[DUPLICATE, DUP_FINAL_SDE] = final_sdes_duplicated_df[DUPLICATE, DUP_FINAL_SDE].copy()
    all_duplications_minus_sde_df[DUPLICATE, DUP_FULL] = full_duplicated_df[DUPLICATE, DUP_FULL].copy()

    all_duplications_df = all_duplications_minus_sde_df.copy()
    all_duplications_df[DUPLICATE, DUP_SDE] = sdes_duplicated_df[DUPLICATE, DUP_SDE].copy()

    all_duplications_minus_sde_df[DUPLICATE, DUP_ANY_MINUS_SDE] = \
        all_duplications_minus_sde_df[all_duplications_minus_sde_df.columns[-5:]].any(axis=1)
    all_duplications_df[DUPLICATE, DUP_ANY] = \
        all_duplications_df[all_duplications_df.columns[-6:]].any(axis=1)

    first_duplicated_df = first_duplicated_df[first_duplicated_df[first_duplicated_df.columns[-1]]]
    final_duplicated_df = final_duplicated_df[final_duplicated_df[final_duplicated_df.columns[-1]]]
    votes_duplicated_df = votes_duplicated_df[votes_duplicated_df[votes_duplicated_df.columns[-1]]]
    sdes_duplicated_df = sdes_duplicated_df[sdes_duplicated_df[sdes_duplicated_df.columns[-1]]]
    final_sdes_duplicated_df = final_sdes_duplicated_df[final_sdes_duplicated_df[final_sdes_duplicated_df.columns[-1]]]
    full_duplicated_df = full_duplicated_df[full_duplicated_df[full_duplicated_df.columns[-1]]]
    all_duplications_minus_sde_df = all_duplications_minus_sde_df[all_duplications_minus_sde_df[all_duplications_minus_sde_df.columns[-1]]]
    all_duplications_df = all_duplications_df[all_duplications_df[all_duplications_df.columns[-1]]]

    write_dataset_as_csv(first_duplicated_df, output_dataset, ST_FIRST_DUPLICATES)
    write_dataset_as_csv(final_duplicated_df, output_dataset, ST_FINAL_DUPLICATES)
    write_dataset_as_csv(votes_duplicated_df, output_dataset, ST_FIRST_FINAL_DUPLICATES)
    write_dataset_as_csv(sdes_duplicated_df, output_dataset, ST_SDE_DUPLICATES)
    write_dataset_as_csv(final_sdes_duplicated_df, output_dataset, ST_FINAL_SDE_DUPLICATES)
    write_dataset_as_csv(full_duplicated_df, output_dataset, ST_FIRST_FINAL_SDE_DUPLICATES)
    write_dataset_as_csv(all_duplications_minus_sde_df, output_dataset, ST_ALL_DUPLICATES_MINUS_SDE)
    write_dataset_as_csv(all_duplications_df, output_dataset, ST_ALL_DUPLICATES)


def main():
    parser = argparse.ArgumentParser(description='Misc analyses')
    parser.add_argument('analysis', choices=ANALYSES)
    parser.add_argument('input_dataset')
    parser.add_argument('output_dataset')
    args = parser.parse_args()

    getattr(sys.modules[__name__], args.analysis)(args.input_dataset, args.output_dataset)


if __name__ == "__main__":
    main()
