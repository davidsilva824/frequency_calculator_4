### Class to extract the zipf values from subtlex-UK.

import pandas as pd

class Zipf_calculator_subtlex:
    def __init__(self, test_files=None): 

        
        df = pd.read_excel("SUBTLEX-UK.xlsx", sheet_name="Sheet1", usecols=["Spelling", "LogFreq(Zipf)"])
        self.subtlex_dict = dict(zip(df['Spelling'], df['LogFreq(Zipf)']))
         
        self.test_files = test_files or []
        
   #### methods to obtain and display zipf values from subtlex for single words, lists of words or files with words. 

    def get_zipf_subtlex_word(self, word): # retrieves the zipf value from subtlex for a single word.
        value = self.subtlex_dict.get(word.lower())
        return round(value, 5) if isinstance(value, (int, float)) else 0
    
    def get_zipf_subtlex_list(self, words): # retrieves the zipf value from subtlex for a list of words.
        return [self.get_zipf_subtlex_word(word) for word in words]
    
    def get_zipf_subtlex_file(self, file): # retrieves the zipf value from subtlex for a list of words in a csv file.
        with open(file, encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
        return self.get_zipf_subtlex_list(words)
    
    def zipf_subtlex(self, input): #returns the zipf values from subtlex for any string, list or file provided in the input. 
        print()

        if isinstance(input, str) and input.endswith(".csv"):
            words = [line.strip() for line in open(input, encoding="utf-8") if line.strip()]
        elif isinstance(input, str):
            words = [input]
        elif isinstance(input, list):
            words = input
        else:
            print("Unsupported input")
            return
        
        for word in words:
            value = self.get_zipf_subtlex_word(word)
            print(f"{word}: {value}")


        