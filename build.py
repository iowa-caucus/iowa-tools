#!/usr/bin/env python

from iowa_tools.constants import IDP_92_PERCENT, IDP_97_PERCENT, IDP_100_PERCENT_FEB8, \
    MORE_FINAL_VOTES, TO_VALIDATE, PRECINCTS, DUPLICATED_PRECINCTS, IDP_100_PERCENT_FEB10
import iowa_tools.parse_iowa as parse_iowa
import iowa_tools.analyze as analyze


# Parse reference data

parse_iowa.parse_iowa_html(IDP_92_PERCENT)
parse_iowa.parse_iowa_html(IDP_97_PERCENT)
parse_iowa.parse_iowa_html(IDP_100_PERCENT_FEB8)
parse_iowa.parse_iowa_html(IDP_100_PERCENT_FEB10)


# Analyze datasets

analyze.more_final_votes(IDP_100_PERCENT_FEB10, MORE_FINAL_VOTES)
analyze.generate_validation_files(IDP_100_PERCENT_FEB10, TO_VALIDATE)
analyze.harmonize_precinct_metadata(IDP_100_PERCENT_FEB10, PRECINCTS)
analyze.duplicated_precincts(IDP_100_PERCENT_FEB10, DUPLICATED_PRECINCTS)
