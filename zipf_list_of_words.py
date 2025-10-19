### Running this module will allow you to obtain the Zipf values for one or more word.

from zipf_calculator import Zipf_calculator

print()

input_string = input("Insert the words separated by a comma (e.g. man, dog,...): ")
words = [word.strip().lower() for word in input_string.split(",")]

print()

a = Zipf_calculator()

print("\n\nSUBTLEX")
a.zipf_subtlex(words)

print("\n\nBabyLM 10M")
a.zipf_babyLM_10M(words)

print("\n\nBabyLM 100M")
a.zipf_babyLM_100M(words)

print()