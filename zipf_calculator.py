### this class inerits from Zipf_calculator_babyLM and Zipf_calculator_subtlex, combining their methods in a single class.
# adds a few other useful methods. 


import os
import csv
import pandas as pd
from zipf_calculator_babyLM import Zipf_calculator_babyLM
from zipf_calculator_subtlex import Zipf_calculator_subtlex

class Zipf_calculator(Zipf_calculator_babyLM, Zipf_calculator_subtlex):

    def __init__(self, test_files=None):
        Zipf_calculator_babyLM.__init__(self, test_files=None) # ineritance of atributes and methods from the other two classes. 
        Zipf_calculator_subtlex.__init__(self, test_files=None)

        self.test_files = test_files or []


    def zipf_test_files(self, output_file): # returns the zipf values for all the words in one or more files
                                            # and saves them in a csv file (output_file), with the name of the test file they were taken from. 

        rows = []

        with open(output_file, "w", encoding="utf-8", newline="") as out:
            writer = csv.writer(out)
            writer.writerow(["group", "word", "zipf_subtlex", "zipf_babyLM_10M", "zipf_babyLM_100M"])

            for file in self.test_files:
                group = os.path.splitext(os.path.basename(file))[0]
                with open(file, encoding="utf-8") as f:
                    for line in f:
                        word = line.strip().lower()
                        if not word:
                            continue

                        zipf_subtlex = self.get_zipf_subtlex_word(word)
                        zipf_10M = self.get_zipf_babyLM_10M_word(word)
                        zipf_100M = self.get_zipf_babyLM_100M_word(word)

                        rows.append([group, word, zipf_subtlex, zipf_10M, zipf_100M])
                        writer.writerow([group, word, zipf_subtlex, zipf_10M, zipf_100M])

        df = pd.DataFrame(rows, columns=["group", "word", "zipf_subtlex", "zipf_babyLM_10M", "zipf_babyLM_100M"])
        print()
        print(df.to_string(index=False))    