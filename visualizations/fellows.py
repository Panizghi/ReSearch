import json

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mplcursors

import pandas as pd

import visualize_sentences as vs


# filepath = "ReSearchcrawler/ReSearchcrawler/acm_profiles.jsonl"

# with open(filepath, "r") as f:
#     fellows_data = [json.loads(line) for line in f]

# sentences = []

# for line in fellows_data:
#     sentence = "Received an award {}. Affiliation is {}. Interests are {}.".format(
#         line["citation"],
#         line["affiliation"],
#         line["interests"],
#     )
#     sentences.append(sentence)

filepath = "data/acm_fellows.csv"

sentences = []
df = pd.read_csv(filepath)
df=df.head(30)

for fellow in df.itertuples():
    # sentence = "Received an award {}. Affiliation is {}. Interests are {}.".format(
    #     fellow.Citation,
    #     fellow.Affiliation,
    #     fellow.Interests,
    # )
    sentence = "Received an award {}. Interests are {}.".format(
        fellow.Citation,
        fellow.Interests,
    )
    sentences.append(sentence)

print(sentences)

embeddings = vs.get_sbert_embeddings(sentences)
# embeddings = vs.get_pca_reductions(embeddings)
embeddings = vs.get_tsne_3d_reductions(embeddings)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(embeddings[:,0], embeddings[:,1], embeddings[:,2])

cursor = mplcursors.cursor(ax, hover=True)
@cursor.connect("add")

def on_add(sel):
    index = sel.index
    # sel.annotation.set_text(df.loc[index, "Last Name"])
    sel.annotation.set_text(df.loc[index, "Citation"])

# for i, (x, y, z) in enumerate(embeddings):
#     ax.scatter(x, y, z, label=f"Point {i}")
#     # ax.text(x, y, z, f"{df.loc[i,"Last Name"]}", color='red')
ax.set_title('3D Semantic Similarity Map')
plt.show()
