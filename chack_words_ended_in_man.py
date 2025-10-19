import pandas as pd

# Parameters
file_path = "SUBTLEX-UK.xlsx"
min_zipf = 2.7
max_zipf = 6

# Load and preprocess
df = pd.read_excel(file_path, sheet_name="Sheet1")
df = df[["Spelling", "LogFreq(Zipf)"]].dropna()
df["Spelling"] = df["Spelling"].str.lower()

# Build lookup
zipf_dict = dict(zip(df["Spelling"], df["LogFreq(Zipf)"]))
words = set(zipf_dict)

# Output list
man_pairs = []

# Search for "men" -> "man" patterns
for plural in words:
    if plural.endswith("men"):
        singular = plural[:-3] + "man"
        if singular in words:
            plural_zipf = zipf_dict[plural]
            singular_zipf = zipf_dict[singular]
            if min_zipf <= plural_zipf <= max_zipf and min_zipf <= singular_zipf <= max_zipf:
                man_pairs.append((singular, plural, singular_zipf, plural_zipf))

# Show results
result_df = pd.DataFrame(man_pairs, columns=["Singular", "Plural", "Singular_Zipf", "Plural_Zipf"])
print(result_df.to_string(index=False))

import pandas as pd

# Parameters
file_path = "SUBTLEX-UK.xlsx"
min_zipf = 2.7
max_zipf = 6

# Load and preprocess
df = pd.read_excel(file_path, sheet_name="Sheet1")
df = df[["Spelling", "LogFreq(Zipf)"]].dropna()
df["Spelling"] = df["Spelling"].str.lower()

# Build lookup
zipf_dict = dict(zip(df["Spelling"], df["LogFreq(Zipf)"]))
words = set(zipf_dict)

# Output list
man_pairs = []

# Search for "men" -> "man" patterns
for plural in words:
    if plural.endswith("men"):
        singular = plural[:-3] + "man"
        if singular in words:
            plural_zipf = zipf_dict[plural]
            singular_zipf = zipf_dict[singular]
            if min_zipf <= plural_zipf <= max_zipf and min_zipf <= singular_zipf <= max_zipf:
                man_pairs.append((singular, plural, singular_zipf, plural_zipf))

# Show results
result_df = pd.DataFrame(man_pairs, columns=["Singular", "Plural", "Singular_Zipf", "Plural_Zipf"])
print(result_df.to_string(index=False))

result_df.to_csv("men_pairs_results.csv", sep="\t", index=False)
