# Uses the classes in the modules 'zipf_calculator.py' and 'zipf_stats.py' to calculate the necessary statistics for the non-head compounds. 

from zipf_calculator import Zipf_calculator
from zipf_stats import Zipf_stats

zipf = Zipf_calculator([
    "regular_singular.csv",
    "regular_plural.csv",
    "irregular_singular.csv",
    "irregular_plural.csv"
])

zipf.zipf_test_files('results_non_heads.csv')

stat = Zipf_stats('results_non_heads.csv','stat_non_head_all.csv')

print()

print(stat.all_means_all_groups())

print()

print(stat.all_sd_all_groups())

print()

print(stat.cohens_d_all('regular_singular','regular_plural'))

print()

print(stat.cohens_d_all('irregular_singular','irregular_plural'))

print()





