from word_searcher_subtlex import Word_searcher_subtlex

searcher = Word_searcher_subtlex()

print("Loaded:", len(searcher.subtlex_dict) > 0)
print("Words ending in 'ing':", searcher.search_words_ended_with("ing"))

print("Checking keys in subtlex_dict before error...")

for w in searcher.subtlex_dict:
    if not isinstance(w, str):
        print("BAD KEY FOUND:", repr(w), type(w))

print("Words with length 4:", searcher.search_words_length(4))
print("Length 3–5:", searcher.search_words_length_range(3, 5))
print("Words with Zipf 4–5:", searcher.search_words_zipf_range(4, 5))

searcher.initialize_glove()
similar = searcher.search_words_similarity_range("rat", 0.4, 1.0, model="glove")
print("Similar to 'rat' (glove):", similar[:5])

combined = searcher.search_by_variable(
    min_len=4,
    max_len=8,
    min_zipf=3.5,
    max_zipf=6.0,
    ending="ed",
    top_n=5
)
print("Combined search:", combined)


combined = searcher.search_by_variable(
    min_len=4,
    max_len=8,
    min_zipf=3.5,
    max_zipf=6.0,
    top_n=5,
    model='glove'
)
print("Combined search:", combined)

combined = searcher.search_by_variable(
    min_len=4,
    max_len=8,
    min_zipf=3.5,
    max_zipf=6.0,
    top_n=5,
    model='fasttext'
)
print("Combined search:", combined)

combined = searcher.search_by_variable(
    min_len=4,
    max_len=8,
    min_zipf=3.5,
    max_zipf=6.0,
    top_n=5,
    model='transformers'
)
print("Combined search:", combined)