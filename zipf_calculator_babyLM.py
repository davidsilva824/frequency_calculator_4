### Class to extract the zipf values from the training corpora for babyLM.
import csv
import math
import re
from collections import Counter
import os
import requests, zipfile, io

class Zipf_calculator_babyLM:
    def __init__(self, test_files=None): 
         
        self.test_files = test_files or []
        self.urls = {
            "train_10M": "https://osf.io/download/y7djq/",
            "train_100M": "https://osf.io/download/ywea7/"
        }

        # It creates a list of file paths by joining the folder name with each corpus filename.

        self.folder_names = ["train_10M", "train_100M"]
        
        self.babylm_training_files = {
            folder_name: [f"{folder_name}/{name}" for name in [
                "bnc_spoken.train", "childes.train", "gutenberg.train",
                "open_subtitles.train", "simple_wiki.train", "switchboard.train"
            ]]
            for folder_name in self.folder_names
        }

        self.concatenated_file_10M = "concatenated_train_10M.csv"
        self.concatenated_file_100M = "concatenated_train_100M.csv"


        for folder in self.folder_names: # dowloads the folders with the corpora used to train the babyLM models
            if not os.path.isdir(folder):
                print(f"Downloading {folder}...")
                r = requests.get(self.urls[folder])
                with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                    z.extractall()
            else:
                print(f"Folder '{folder}' already exists.")

        for folder_name, concat_file in [
            ("train_10M", self.concatenated_file_10M),
            ("train_100M", self.concatenated_file_100M)
        ]:
            training_files = [f"{folder_name}/{name}" for name in [
                "bnc_spoken.train", "childes.train", "gutenberg.train",
                "open_subtitles.train", "simple_wiki.train", "switchboard.train"
            ]]

            if os.path.exists(concat_file):
                print(f"{concat_file} already exists.")
                continue

            with open(concat_file, "w", encoding="utf-8", newline='') as out: #creates files with all of the training datasets concatenated.
                writer = csv.writer(out)
                for f in training_files:
                    with open(f, encoding="utf-8") as infile:
                        for line in infile:
                            clean = line.strip()
                            if clean:
                                writer.writerow([clean])


        self.tokens_10M = self.tokenize(self.concatenated_file_10M)
        self.tokens_100M = self.tokenize(self.concatenated_file_100M)

        self.freq_10M = Counter(self.tokens_10M)
        self.freq_100M = Counter(self.tokens_100M)

        self.total_tokens_10M = len(self.tokens_10M)
        self.total_tokens_100M = len(self.tokens_100M)
        
        self.vocab_size_10M = len(self.freq_10M)
        self.vocab_size_100M = len(self.freq_100M)
    
##### methods to return zipf_values for babyLM

    def tokenize_text(self,text): #tokenizes text in a string. Returns the same text but in a list, with all the words. Ex: 'the dog bit the man!' returns [the,dog,bit,the,man]
        return re.findall(r'\b\w+\b', text.lower())
      
    def tokenize(self,input):  # works both with a string or a file with text.
        
        if isinstance(input, str) and os.path.isfile(input):
            with open(input, encoding="utf-8") as f:
                text = " ".join([line.strip() for line in f if line.strip()])
            return self.tokenize_text(text)
        
        elif isinstance(input, str):
            return self.tokenize_text(input)
        else:
            print("Wrong input. It must be a string with sentences or a file")
            return []
  
    def get_number_of_tokens(self,input):
        return len(self.tokenize(input))
        
    def get_freq_text(self,word,text): # returns the raw frequency of a word in a text

        tokenized_text = self.tokenize(text)
        return Counter(tokenized_text)[word.lower()]
    
    def get_freq_file(self,word,file_name):
        with open(file_name, encoding="utf-8") as f:
            text = " ".join([line.strip() for line in f if line.strip()])
        return self.get_freq_text(word,text)
    
    def get_freq(self,word, input):
        if isinstance(input, str) and os.path.isfile(input):
            with open(input, encoding="utf-8") as f:
                text = " ".join([line.strip() for line in f if line.strip()])
            return self.get_freq_text(word, text)
        
        elif isinstance(input, str):
            return self.get_freq_text(word, input)
        else:
            print("Wrong input. It must be a string with sentences or a file")
            return []
      
    def get_zipf_babyLM_10M_word(self, word):

        word_lower = word.lower()

        if word_lower not in self.freq_10M:
            return 0

        freq = self.freq_10M[word_lower]
        total_tokens = self.total_tokens_10M
        vocab_size = self.vocab_size_10M

        return round(math.log10((freq + 1) / ((total_tokens + vocab_size)/1000000)) + 3, 5) 

    def get_zipf_babyLM_100M_word(self, word):

        word_lower = word.lower()

        if word_lower not in self.freq_10M:
            return 0
        
        freq = self.freq_100M[word_lower]
        total_tokens = self.total_tokens_100M
        vocab_size = self.vocab_size_100M

        return round(math.log10((freq + 1) / ((total_tokens + vocab_size)/1000000)) + 3, 5)
    
    def get_zipf_babyLM_10M_list(self, words):
        return [self.get_zipf_babyLM_10M_word(word) for word in words]

    def get_zipf_babyLM_100M_list(self, words):
        return [self.get_zipf_babyLM_100M_word(word) for word in words]

    def get_zipf_babyLM_10M_file(self, file):
        with open(file, encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
        return self.get_zipf_babyLM_10M_list(words)

    def get_zipf_babyLM_100M_file(self, file):
        with open(file, encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
        return self.get_zipf_babyLM_100M_list(words)
    
    
    def zipf_babyLM_10M(self, input):
        print()

        if isinstance(input, str) and input.endswith(".csv"):
            with open(input, encoding="utf-8") as f:
                words = [line.strip() for line in f if line.strip()]
        elif isinstance(input, str):
            words = [input]
        elif isinstance(input, list):
            words = input
        else:
            print("Unsupported input")
            return

        for word in words:
            value = self.get_zipf_babyLM_10M_word(word)
            print(f"{word}: {value}")

    
    def zipf_babyLM_100M(self, input):
        print()

        if isinstance(input, str) and input.endswith(".csv"):
            with open(input, encoding="utf-8") as f:
                words = [line.strip() for line in f if line.strip()]
        elif isinstance(input, str):
            words = [input]
        elif isinstance(input, list):
            words = input
        else:
            print("Unsupported input")
            return

        for word in words:
            value = self.get_zipf_babyLM_100M_word(word)
            print(f"{word}: {value}")
    

    

   
