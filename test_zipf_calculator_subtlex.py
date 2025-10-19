from zipf_calculator_subtlex import Zipf_calculator_subtlex


subtlex = Zipf_calculator_subtlex()

print(subtlex.get_zipf_subtlex_word("the"))
print(subtlex.get_zipf_subtlex_list(["the", "dog","nonsenseword"]))
print(subtlex.get_zipf_subtlex_file("regular_plural.csv"))
subtlex.zipf_subtlex("cat")
subtlex.zipf_subtlex(["cat", "table"])
subtlex.zipf_subtlex("regular_plural.csv")