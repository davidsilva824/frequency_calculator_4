from word_searcher_subtlex import Word_searcher_subtlex

searcher = Word_searcher_subtlex()

combined = searcher.search_by_variable(
    min_len=2,
    max_len=5,
    min_zipf=3.5,
    max_zipf=6.0,
    top_n=5,
    target_word='rat',
    model='glove'
)
print("Combined search:", combined)

combined = searcher.search_by_variable(
    min_len=2,
    max_len=5,
    min_zipf=3.5,
    max_zipf=6.0,
    top_n=5,
    target_word='rat',
    model='fasttext'
)
print("Combined search:", combined)

combined = searcher.search_by_variable(
    min_len=2,
    max_len=5,
    min_zipf=3.5,
    max_zipf=6.0,
    top_n=5,
    target_word='rat',
    model='transformer'
)
print("Combined search:", combined)