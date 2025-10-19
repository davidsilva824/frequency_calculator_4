from sentence_transformers import SentenceTransformer, util
import pandas as pd
import inflect
import torch

# Setup
hf_token = "insert_your_token_here"  # Replace with your token
target_word = "ox"
zipf_range = 3  # You can change this range

# Load model
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2", use_auth_token=hf_token)
if torch.cuda.is_available():
    model = model.to('cuda')

# Load SUBTLEX
file_path = "SUBTLEX-UK.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")
df = df[["Spelling", "LogFreq(Zipf)"]].dropna()
df["Spelling"] = df["Spelling"].str.lower()
zipf_dict = dict(zip(df["Spelling"], df["LogFreq(Zipf)"]))

# Inflect engine
p = inflect.engine()
plural_form = p.plural(target_word)
singular_zipf = zipf_dict.get(target_word)
plural_zipf = zipf_dict.get(plural_form)

# Compute dynamic zipf limits
if singular_zipf is None and plural_zipf is None:
    raise ValueError("Zipf value for target word not found.")
zipfs = [z for z in [singular_zipf, plural_zipf] if z is not None]
min_zipf = min(zipfs) - zipf_range
max_zipf = max(zipfs) + zipf_range

# Utility to compute letter difference
def letter_difference(w1, w2):
    if abs(len(w1) - len(w2)) > 1:
        return 2  # fast fail
    diffs = sum(1 for a, b in zip(w1, w2) if a != b) + abs(len(w1) - len(w2))
    return diffs

# Collect regular plural pairs ending in 's' within zipf range and 1-letter difference
regular_pairs = []
for plural in df["Spelling"]:
    if not plural.endswith("s"):
        continue
    singular = p.singular_noun(plural)
    if singular and singular in zipf_dict and plural in zipf_dict:
        singular_zipf = zipf_dict[singular]
        plural_zipf = zipf_dict[plural]
        if min_zipf <= singular_zipf <= max_zipf and min_zipf <= plural_zipf <= max_zipf:
            if letter_difference(singular, target_word) <= 1:
                regular_pairs.append((singular, plural, singular_zipf, plural_zipf))

# Create DataFrame
result_df = pd.DataFrame(regular_pairs, columns=["Singular", "Plural", "Singular_Zipf", "Plural_Zipf"])

# Compute similarities
target_vec = model.encode(target_word)
result_df["Similarity"] = result_df["Singular"].apply(
    lambda word: util.cos_sim(model.encode(word), target_vec).item()
)

# Sort and limit
ordered_df = result_df.sort_values(by="Similarity", ascending=False).head(100)

# Output
print(ordered_df)

filename = f"semantic_similarity_{target_word}.csv"
with open(filename, "w") as f:
    f.write("Word\tZipf\tSimilarity\n")
    for _, row in ordered_df.iterrows():
        f.write(f"{row.Singular}\t{row.Singular_Zipf}\t{row.Similarity}\n")
        f.write(f"{row.Plural}\t{row.Plural_Zipf}\t{row.Similarity}\n")
