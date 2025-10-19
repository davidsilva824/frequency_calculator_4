### class to search for words with certain characteristics in Subtlex-UK.
### You need to provide and hugging_face token

import pandas as pd
from zipf_calculator import Zipf_calculator
from word_semantic_similarity import Word_semantic_similarity
import numpy as np
from sentence_transformers import util


class Word_searcher_subtlex(Zipf_calculator, Word_semantic_similarity):
    def __init__(self, hf_token=None, test_files=None):
        Zipf_calculator.__init__(self, test_files)
        Word_semantic_similarity.__init__(self, hf_token)

        df = pd.read_excel("SUBTLEX-UK.xlsx", sheet_name="Sheet1", usecols=["Spelling", "LogFreq(Zipf)", "DomPoS"]) #selects only the nouns
        df = df[df['DomPoS'].str.contains('noun', case=False, na=False)]
        df = df[df['Spelling'].apply(lambda x: isinstance(x, str))]
        df = df.drop(columns=['DomPoS'])

        self.subtlex_dict = dict(zip(df['Spelling'], df['LogFreq(Zipf)']))


    def search_words_ended_with(self, ending):
        return [w for w in self.subtlex_dict if isinstance(w, str) and w.endswith(ending)] ### rever esta questão desta string
    
    def search_words_length(self, length):
        return [w for w in self.subtlex_dict if len(w) == length]
    
    def search_words_length_range(self, min_len, max_len):
        return [w for w in self.subtlex_dict if min_len <= len(w) <= max_len]
    
    def search_words_zipf_range(self, min_zipf, max_zipf):
        return [w for w in self.subtlex_dict
                if min_zipf <= self.get_zipf_subtlex_word(w) <= max_zipf]
    
    def search_words_similarity_range(self, target_word, min_sim, max_sim, model="transformer"):
        results = []

        if target_word and model:
            if model == "glove":
                self.initialize_glove()
            elif model == "fasttext":
                self.initialize_fasttext()
            elif model == "transformer":
                self.initialize_model()

        for word in self.subtlex_dict:
            if word == target_word:
                continue

            if model == "glove":
                sim = self.get_similarity_glove(target_word, word)

            elif model == "fasttext":
                sim = self.get_similarity_fasttext(target_word, word)

            elif model == "transformer":
                sim = self.get_similarity_transformer(target_word, word)
            else:
                raise ValueError("Model must be 'glove', 'fasttext', or 'transformer'")

            if isinstance(sim, (int, float)) and min_sim <= sim <= max_sim:
                results.append((word, sim))

        return sorted(results, key=lambda x: -x[1])



    def search_by_variable(
        self,
        min_len = None,
        max_len = None,
        min_zipf = None,
        max_zipf = None,
        target_word=None,
        model=None,
        top_n=None,
        ending=None
    ):
        results = []

    # Pre-filter words by length, zipf, ending (exclude similarity first)
        filtered_words = []
        for word in self.subtlex_dict:
            length = len(word)
            if min_len is not None and length < min_len:
                continue
            if max_len is not None and length > max_len:
                continue
            zipf = self.get_zipf_subtlex_word(word)
            if min_zipf is not None and zipf < min_zipf:
                continue
            if max_zipf is not None and zipf > max_zipf:
                continue
            if ending and not word.endswith(ending):
                continue
            filtered_words.append((word, zipf))

        # If transformer + target word, batch encode similarity
        if target_word and model == "transformer":
            self.initialize_model()
            target_vec = self.model.encode(target_word)
            words = [w for w, _ in filtered_words]
            word_vecs = self.model.encode(words, batch_size=64)

            sims = util.cos_sim(word_vecs, target_vec).cpu().numpy().flatten()

            # Build results with similarity
            results = [(w, z, sim) for (w, z), sim in zip(filtered_words, sims)]
            results = [r for r in results if r[2] is not None]
            results.sort(key=lambda x: -x[2])

        else:
            # For glove or fasttext, compute similarity inside loop
            if target_word and model == "glove":
                self.initialize_glove()
            elif target_word and model == "fasttext":
                self.initialize_fasttext()

            for word, zipf in filtered_words:
                if target_word and model:
                    if model == "glove":
                        sim = self.get_similarity_glove(target_word, word)
                    elif model == "fasttext":
                        sim = self.get_similarity_fasttext(target_word, word)
                    else:
                        sim = None
                else:
                    sim = None
                results.append((word, zipf, sim))

            if target_word and model:
                results = [r for r in results if r[2] is not None]
                results.sort(key=lambda x: -x[2])
            else:
                results.sort(key=lambda x: -x[1])

        if top_n is not None:
            results = results[:top_n]

        return results


### adicionar metodo final que procura uma palavra cruzando todos estes métodos e a semantica também. 
        
   
    
        
    
    






