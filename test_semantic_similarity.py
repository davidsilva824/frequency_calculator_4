from word_semantic_similarity import Word_semantic_similarity  # Adjust if your file has a different name
import os

# Initialize class
sim = Word_semantic_similarity(hf_token="put_your_token_here")



# Initialize models
sim.initialize_glove()
sim.initialize_fasttext()
sim.initialize_model()

# Test words
word1 = "rat"
word2 = "mouse"
word3 = "nonsenseword"

print()

# GloVe tests
print("GloVe similarity (rat,mouse):", sim.get_similarity_glove(word1, word2))
print("GloVe with inexistent word:", sim.get_similarity_glove(word1, word3))

print()

# FastText tests
print("FastText similarity (rat,mouse):", sim.get_similarity_fasttext(word1, word2))
print("FastText with inexistent word:", sim.get_similarity_fasttext(word1, word3))

print()

# Transformer test
print("Transformer similarity (rat,mouse):", sim.get_similarity_transformer(word1, word2))

print()