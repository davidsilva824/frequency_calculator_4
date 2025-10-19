### some basic tests to the classes created. Need to add true unittests still.

from zipf_calculator import Zipf_calculator

# Instantiating without parameters (only SUBTLEX methods will be used)
z = Zipf_calculator()

print(z.get_zipf_subtlex_word("dog")) 

print(z.get_zipf_subtlex_word("nonsenseword")) 


words = ["dog", "cat", "nonsenseword"]
print(z.get_zipf_subtlex_list(words))

print(z.get_zipf_subtlex_file("irregular_plural.csv"))


z.zipf_subtlex("dog")
z.zipf_subtlex(["dog", "cat", "nonsenseword"])
z.zipf_subtlex("regular_plural.csv")


# Test with string
text = "The dog barked. The dog ran."
print(z.tokenize(text))  # ['the', 'dog', 'barked', 'the', 'dog', 'ran']
print(z.get_number_of_tokens(text))  # 6
print(z.get_freq("dog", text))  # 2

# Test with file
print(z.tokenize("test_zipf_calculator_file.csv"))
print(z.get_number_of_tokens("test_zipf_calculator_file.csv")) 
print(z.get_freq("the", "test_zipf_calculator_file.csv")) 


print(z.get_zipf_babyLM_10M_word("rat"))
print(z.get_zipf_babyLM_100M_word("rat"))

z2 = Zipf_calculator([
    "regular_singular.csv",
    "regular_plural.csv",
    "irregular_singular.csv",
    "irregular_plural.csv"
])

z2.zipf_test_files("result_files.csv")