# iowa-tools

Set of tools to be used for crowd sourcing the repair of the Iowa Caucus results of the 2020 Democratic Party presidential primaries.

As of Feb 8 2020, there is still a large amount of errors and inconsistencies in the results, and most media sites have not called the 
winner. Bernie Sanders has won the popular vote, while Pete Buttigieg for now is marginally leading the State Delegate Equivalents.

The following [article published in heavy.com](https://heavy.com/news/2020/02/iowa-caucus-results-state-delegates/) contains a nice 
overview of many of the remaining issues/

There have been a number of initiatives on social media sites, such as:

- [Reddit: WayOfTheBern Crowd sourcing initiative](https://www.reddit.com/r/WayOfTheBern/comments/ezjlwq/crowd_source_help_needed_asap/)
- [Twitter thread on inconsistencies](https://twitter.com/Taniel/status/1225597027851100160)
- [Inconsistencies published by the Bernie Sanders campaign](https://twitter.com/IAStartingLine/status/1225615234196557825)
- [2020 Iowa Caucus Precinct Errors](https://docs.google.com/spreadsheets/d/1JLQvIHaasTYTPOeEPKXquNPx9VCvJNNzCIJlxEkrBfQ/edit#gid=0)

What is lacking, though, is a way to merge all of these efforts together in a way that allows for easy contributions, while also 
allowing for adding automated discrepancy checks and validation processes, most importantly including continuous recalculation of 
the delegate scores. Previous efforts have mostly used Google Sheets for this process, which is useful to gather information quickly,
but hard to automate. GitHub, on the other hand, excels in automation, as well as in setting up proper reviewing processes.

- The initial implementation has been done in Python, using the Pandas library for table management.
- The last few data releases from the Iowa Democratic Party has been parsed and converted to both [JSON and CSV formats](out_data/idp-2020-02-08-100).
- GitHub allows web-based editing of text files and CSV files, including transparent review processes using Pull Requests.
- There are utility functions for converting from JSON data to Pandas DataFrames and back to both JSON and CSV files. More 
conversion utilities should be easy to create.
- The [iowa_tools/analyze.py](iowa_tools/analyze.py) module contains a simple framework for adding analyses and discrepancy checks. 
Output from these can be viewed in specific subdirectories in the `out_data` directory.
- Please also make use of the [Issues](issues) feature to provide feature requests and bug reports. If you want to be granted write 
permissions to the repo, please create an issue with some information about yourself, so that I can do a brief review. For this to 
work, we need to share the responsibilities, with a few people being granted the permissions to review the work of a larger group of 
people doing the brunt work.
- We need to hammer out the details as we go.

Analysis features implemented:

- Check on whether more people voted in the second round than in the first, with [the results here](out_data/more_final_votes/more_votes.csv)
- The [out_data/to_validate](out_data/to_validate) directory contains CSV and JSON versions of the voting data, which should be 
validated towards evidence. Here, non-programmers can contribute with manual validation of precinct data against evidence. Much has been done already, for instance [on Reddit](https://www.reddit.com/r/WayOfTheBern/comments/ezjlwq/crowd_source_help_needed_asap/), but the validated data is not so easily available for automated downstream calculations.

What is planned to be added:

- Validity checks of the viability thresholds
- Calculation of delegates at all levels
- Pipeline to include validated precinct votes into the calculations 
- More discrepancy checks
- Automated builds
- And more...

Let's do this!
