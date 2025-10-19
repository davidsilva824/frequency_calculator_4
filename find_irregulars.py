from sentence_transformers import SentenceTransformer, util
import pandas as pd
import inflect

import pandas as pd
import inflect

# Load and clean data
df = pd.read_excel("SUBTLEX-UK.xlsx", sheet_name="Sheet1")
df["Spelling"] = df["Spelling"].str.lower()
zipf_dict = dict(zip(df["Spelling"], df["LogFreq(Zipf)"]))

# Setup inflect
p = inflect.engine()

# Collect irregular singulars
irregular_pairs = []
for word in df["Spelling"]:
    if not word.endswith("s"):  # Singular candidate
        plural = p.plural(word)
        if plural and plural != word and plural in zipf_dict:
            irregular_pairs.append((word, plural, zipf_dict[word], zipf_dict[plural]))

# Create and show DataFrame
result_df = pd.DataFrame(irregular_pairs, columns=["Singular", "Plural", "Singular_Zipf", "Plural_Zipf"])
print(result_df)