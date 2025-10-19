from sentence_transformers import SentenceTransformer, util
import pandas as pd
import inflect
import torch


hf_token = "place your HF token here"  # Replace with your token
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2", use_auth_token=hf_token)
target_word = "salesman"
min_zipf = 2.45
max_zipf = 4.2
min_len = 7
max_len = 9


if torch.cuda.is_available():
    model = model.to('cuda')

file_path = "SUBTLEX-UK.xlsx"  # Update this path if needed
df = pd.read_excel(file_path, sheet_name="Sheet1")

df = df[["Spelling", "LogFreq(Zipf)"]].dropna()
df["Spelling"] = df["Spelling"].str.lower()

# Build lookup dictionary
zipf_dict = dict(zip(df["Spelling"], df["LogFreq(Zipf)"]))

# Inflect engine
p = inflect.engine()

# Output list
regular_pairs = []

# Scan for regular plural–singular pairs
for plural in df["Spelling"]:
    if not plural.endswith("s"):
        continue
    singular = p.singular_noun(plural)
    if singular and singular in zipf_dict:
        plural_zipf = zipf_dict[plural]
        singular_zipf = zipf_dict[singular]
        
        if (
            min_zipf <= plural_zipf <= max_zipf
            and min_zipf <= singular_zipf <= max_zipf
            and min_len <= len(singular) <= max_len
            and min_len <= len(plural) <= max_len
        ):
            regular_pairs.append((singular, plural, singular_zipf, plural_zipf))

# Create and show final DataFrame
result_df = pd.DataFrame(regular_pairs, columns=["Singular", "Plural", "Singular_Zipf", "Plural_Zipf"])
print(result_df)


# Your Hugging Face token (keep private!)

target_vec = model.encode(target_word)

# Add similarity column comparing to singular form
result_df["Similarity"] = result_df["Singular"].apply(
    lambda word: util.cos_sim(model.encode(word), target_vec).item()
)

# Sort by similarity
ordered_df = result_df.sort_values(by="Similarity", ascending=False)

# Show result
print(ordered_df)

filename = f"semantic_similarity_results_{target_word}.txt"

with open(f"semantic_similarity_{target_word}.csv", "w") as f:
    f.write("Word\tZipf\tSimilarity\n")
    for _, row in ordered_df.iterrows():
        f.write(f"{row.Singular}\t{row.Singular_Zipf}\t{row.Similarity}\n")
        f.write(f"{row.Plural}\t{row.Plural_Zipf}\t{row.Similarity}\n")