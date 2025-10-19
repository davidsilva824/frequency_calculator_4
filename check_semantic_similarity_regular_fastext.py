import os
import urllib.request
import gzip
import shutil
import pandas as pd
import inflect
from gensim.models.fasttext import load_facebook_model

# -----------------------
# Parameters
# -----------------------
target_word = "fisherman"
min_zipf = 3.25
max_zipf = 4.5
min_len = 8
max_len = 10

# -----------------------
# Download + Load FastText
# -----------------------
URL = "https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz"
COMPRESSED_FILE = "cc.en.300.bin.gz"
MODEL_FILE = "cc.en.300.bin"

if not os.path.exists(COMPRESSED_FILE) and not os.path.exists(MODEL_FILE):
    print("Downloading FastText vectors...")
    urllib.request.urlretrieve(URL, COMPRESSED_FILE)
    print("Download complete.")

if not os.path.exists(MODEL_FILE):
    print("Extracting...")
    with gzip.open(COMPRESSED_FILE, "rb") as f_in:
        with open(MODEL_FILE, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    print("Extraction complete.")

print("Loading FastText model (this may take a while)...")
model = load_facebook_model(MODEL_FILE)


# -----------------------
# Load SUBTLEX
# -----------------------
file_path = "SUBTLEX-UK.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")

df = df[["Spelling", "LogFreq(Zipf)"]].dropna()
df["Spelling"] = df["Spelling"].str.lower()

zipf_dict = dict(zip(df["Spelling"], df["LogFreq(Zipf)"]))

p = inflect.engine()
regular_pairs = []

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

result_df = pd.DataFrame(
    regular_pairs, columns=["Singular", "Plural", "Singular_Zipf", "Plural_Zipf"]
)

# -----------------------
# Compute similarity (FastText)
# -----------------------
target_vec = model.wv[target_word]

def cosine_sim(w):
    try:
        return model.wv.similarity(w, target_word)
    except KeyError:
        return None  # OOV (rare in FastText)

result_df["Similarity"] = result_df["Singular"].apply(cosine_sim)
result_df = result_df.dropna(subset=["Similarity"])

ordered_df = result_df.sort_values(by="Similarity", ascending=False)
print(ordered_df)

# -----------------------
# Save EXACTLY like your transformer code
# -----------------------
filename = f"semantic_similarity_{target_word}_fastext.csv"

with open(filename, "w") as f:
    f.write("Word\tZipf\tSimilarity\n")
    for _, row in ordered_df.iterrows():
        f.write(f"{row.Singular}\t{row.Singular_Zipf}\t{row.Similarity}\n")
        f.write(f"{row.Plural}\t{row.Plural_Zipf}\t{row.Similarity}\n")

print(f"Results saved to {filename}")
