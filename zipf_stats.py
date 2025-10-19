# This class calculates statistics: mean, standard deviation and cohen's d.

import pandas as pd

class Zipf_stats:
    def __init__(self, result_file, output_stats_file):

        self.result_file = result_file
        self.output_stats_file = output_stats_file
        self.df = pd.read_csv(result_file)
        self.stats = []


    def mean_group_subtlex(self, group):
        subset = self.df[self.df["group"] == group]
        mean = subset["zipf_subtlex"].mean()
        return mean
    

    def mean_group_babyLM_10M(self, group):
        subset = self.df[self.df["group"] == group]
        mean = subset["zipf_babyLM_10M"].mean()
        return mean
    
    def mean_group_babyLM_100M(self, group):
        subset = self.df[self.df["group"] == group]
        mean = subset["zipf_babyLM_100M"].mean()
        return mean
    
    def all_means_one_group(self, group):
        means = {
            "group": group,
            "mean_zipf_subtlex": self.mean_group_subtlex(group),
            "mean_zipf_babyLM_10M": self.mean_group_babyLM_10M(group),
            "mean_zipf_babyLM_100M": self.mean_group_babyLM_100M(group)
        }
        return pd.DataFrame([means])

    def all_means_all_groups(self):
        df_list = [self.all_means_one_group(group) for group in self.df["group"].unique()]
        df_all = pd.concat(df_list, ignore_index=True)
        return df_all


    def sd_group_subtlex(self, group):
        subset = self.df[self.df["group"] == group]
        return subset["zipf_subtlex"].std()

    def sd_group_babyLM_10M(self, group):
        subset = self.df[self.df["group"] == group]
        return subset["zipf_babyLM_10M"].std()

    def sd_group_babyLM_100M(self, group):
        subset = self.df[self.df["group"] == group]
        return subset["zipf_babyLM_100M"].std()
    
    def all_sd_one_group(self, group):
        sds = {
            "group": group,
            "sd_zipf_subtlex": self.sd_group_subtlex(group),
            "sd_zipf_babyLM_10M": self.sd_group_babyLM_10M(group),
            "sd_zipf_babyLM_100M": self.sd_group_babyLM_100M(group)
            }
        return pd.DataFrame([sds])
    
    def all_sd_all_groups(self):
        df = pd.concat([self.all_sd_one_group(g) for g in self.df["group"].unique()], ignore_index=True)
        return df
    
         
    def sd_diff_groups(self, group1, group2, column): # calculates the sd of the differences between two groups. Ther order of the words must be matched in the files.  
        subset1 = self.df[self.df["group"] == group1].reset_index(drop=True)
        subset2 = self.df[self.df["group"] == group2].reset_index(drop=True)

        min_len = min(len(subset1), len(subset2))
        diffs = subset1[column][:min_len] - subset2[column][:min_len]

        return diffs.std()
          

    def cohens_d_one_zipf(self, group1, group2, column): # columns can be 'sd_zipf_subtlex', 'sd_zipf_babyLM_10M' or 'sd_zipf_babyLM_100M'. 
        subset1 = self.df[self.df["group"] == group1].reset_index(drop=True)
        subset2 = self.df[self.df["group"] == group2].reset_index(drop=True)

        min_len = min(len(subset1), len(subset2))
        diffs = subset1[column][:min_len] - subset2[column][:min_len]

        std = self.sd_diff_groups(group1, group2, column)
        return round(diffs.mean() / std, 3)
    
    def cohens_d_all(self, group1, group2):
        columns = ["zipf_subtlex", "zipf_babyLM_10M", "zipf_babyLM_100M"]
        results = []

        for col in columns:
            d_value = self.cohens_d_one_zipf(group1, group2, col)
            results.append({
                "comparison": f"{group1} vs {group2}",
                "source": col,
                "cohens_d": d_value
            })

        df = pd.DataFrame(results)
        return df
        

    

    

        


    

        
