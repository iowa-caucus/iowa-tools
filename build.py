#!/usr/bin/env python

from iowa_tools.constants import IDP_100_PERCENT, MORE_FINAL_VOTES, TO_VALIDATE
import iowa_tools.parse_iowa as parse_iowa
import iowa_tools.analyze as analyze


# Parse reference data

parse_iowa.parse_iowa_html(IDP_100_PERCENT)


# Analyze datasets

analyze.more_final_votes(IDP_100_PERCENT, MORE_FINAL_VOTES)
analyze.generate_validation_files(IDP_100_PERCENT, TO_VALIDATE)
