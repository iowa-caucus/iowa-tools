# TABLE_HEADERS_AND_RESERVED_KEYWORDS

COUNTY = 'County'
PRECINCT = 'Precinct'
FIRST = 'First Expression'
FINAL = 'Final Expression'
SDE = 'SDE'
TOTAL_SDE = 'Total SDE'
INC_VOTES = 'Final Vote Increase'
DOCUMENTATION_URL = 'URL to Documentation'
VALIDATED = 'Manually validated'
PRECINCT_SN = 'Precinct Short Name'
DUPLICATE = 'Duplicate'
DUP_FIRST = 'First'
DUP_FINAL = 'Final'
DUP_SDE = 'SDE'
DUP_FIRST_FINAL = 'First & Final'
DUP_FINAL_SDE = 'Final & SDE'
DUP_FULL = 'Full'
DUP_ANY_MINUS_SDE = 'Any (-SDE)'
DUP_ANY = 'Any'

STD_COL_ORDER = [COUNTY, PRECINCT, FIRST, FINAL, INC_VOTES, DOCUMENTATION_URL, VALIDATED, SDE]

BENNET = "Bennet"
BIDEN = "Biden"
BLOOMBERG = "Bloomberg"
BUTTIGIEG = "Buttigieg"
DELANEY = "Delaney"
GABBARD = "Gabbard"
KLOBUCHAR = "Klobuchar"
PATRICK = "Patrick"
SANDERS = "Sanders"
STEYER = "Steyer"
WARREN = "Warren"
YANG = "Yang"
OTHER = "Other"
UNCOMMITTED = "Uncommitted"
TOTAL = 'Total'


# DIRECTORY NAMES

REF_DATA_DIR = 'ref_data'
DATA_DIR = 'data'


# REFERENCE DATASETS

IDP_92_PERCENT = 'idp-2020-02-06-92'
IDP_97_PERCENT = 'idp-2020-02-06-97'
IDP_100_PERCENT = 'idp-2020-02-08-100'
GOP_2008_RESULTS = 'iagop2008certifiedresults'
IDP_PRECINCT_DELEGATES = 'idp-precinct-delegates'
SPSTEVE_PRECINCT_DELEGATES = 'spsteve_precinct_delegates'


# OUTPUT DATASETS

MORE_FINAL_VOTES = 'more_final_votes'
TO_VALIDATE = 'to_validate'
PRECINCTS = 'precinct_delegates'
DUPLICATED_PRECINCTS = 'duplicated_precincts'


# OUTPUT DATASET SUBTYPES

ST_FULL = 'full'
ST_VOTES = 'votes'
ST_TOTALS = 'totals'
ST_SDES = 'sdes'
ST_SDE_COUNTY_TOTALS = 'sde_county_totals'
ST_SDE_PRECINCT_TOTALS = 'sde_precinct_totals'
ST_MORE_VOTES = 'more_votes'
ST_MAPPING = 'name_mapping'
ST_FIRST_DUPLICATES = 'first_duplicates'
ST_FINAL_DUPLICATES = 'final_duplicates'
ST_FIRST_FINAL_DUPLICATES = 'first_final_duplicates'
ST_SDE_DUPLICATES = 'sde_duplicates'
ST_FINAL_SDE_DUPLICATES = 'final_sde_duplicates'
ST_FIRST_FINAL_SDE_DUPLICATES = 'first_final_sde_duplicates'
ST_ALL_DUPLICATES_MINUS_SDE = 'all_duplicates_minus_sde'
ST_ALL_DUPLICATES = 'all_duplicates'


# FILE SUFFIXES

CSV_SUFFIX = '.csv'
HTML_SUFFIX = '.html'
JSON_HEADERS_SUFFIX = '.headers.json'
JSON_DATA_SUFFIX = '.json'
