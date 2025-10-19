from zipf_stats import Zipf_stats


stat = Zipf_stats('results_non_heads.csv','stat_non_head_all.csv')

print(stat.all_means_all_groups())

print(stat.all_sd_all_groups())

print(stat.cohens_d_all('irregular_singular','irregular_plural'))

