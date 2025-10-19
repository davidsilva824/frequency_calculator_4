from gensim.models import KeyedVectors
from gensim.models.fasttext import load_facebook_model
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import inflect
import torch
import urllib.request
import os


class Word_semantic_similarity:
    def __init__(self, hf_token, model_name = None): #add later the option to change the model. 

        self.hf_token = hf_token
        df = pd.read_excel("SUBTLEX-UK.xlsx", sheet_name="Sheet1") # extracts from the xlsx a dictionary with the all the words in the subtlex file and their zipf values.
        self.subtlex_dict = dict(zip(df['Spelling'], df['LogFreq(Zipf)'])) 
        
    
    def initialize_glove(self):
        import os, urllib.request, zipfile
        from gensim.scripts.glove2word2vec import glove2word2vec

        zip_path = 'glove.6B.zip'
        glove_txt = 'glove.6B.300d.txt'
        word2vec_txt = 'glove.6B.300d.word2vec.txt'

        if not os.path.isfile(word2vec_txt):
            if not os.path.isfile(zip_path):
                print("Downloading GloVe...")
                urllib.request.urlretrieve('http://nlp.stanford.edu/data/glove.6B.zip', zip_path)

            print("Extracting GloVe...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extract(glove_txt)

            print("Converting to word2vec format...")
            glove2word2vec(glove_txt, word2vec_txt)

        self.glove_model = KeyedVectors.load_word2vec_format(word2vec_txt, binary=False)

    
    def initialize_fasttext(self):
        path = 'cc.en.300.bin'
        url = 'https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz'
        if not os.path.isfile(path):
            print("Downloading FastText model...")
            urllib.request.urlretrieve(url, 'cc.en.300.bin.gz')
            import gzip, shutil
            with gzip.open('cc.en.300.bin.gz', 'rb') as f_in:
                with open(path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        self.fasttext_model = load_facebook_model(path) 
  
    
    def initialize_model(self): #adapt later for other models.
        self.model = SentenceTransformer(
            "sentence-transformers/all-mpnet-base-v2",
            use_auth_token=self.hf_token).to('cuda' if torch.cuda.is_available() else 'cpu')
        

    def get_similarity_glove(self, word1, word2):
        if word1 in self.glove_model and word2 in self.glove_model:
            return self.glove_model.similarity(word1, word2)
        return "not found"

    def get_similarity_fasttext(self, word1, word2):
        if word1 in self.fasttext_model.wv and word2 in self.fasttext_model.wv:
            return self.fasttext_model.wv.similarity(word1, word2)
        return "word not found"
  
    def get_similarity_transformer(self, word1, word2):
        emb1 = self.model.encode(word1, convert_to_tensor=True)
        emb2 = self.model.encode(word2, convert_to_tensor=True)
        return util.cos_sim(emb1, emb2).item()

    
