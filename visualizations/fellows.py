import json

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import visualize_sentences as vs


filepath = "ReSearchcrawler/ReSearchcrawler/acm_profiles.jsonl"

with open(filepath, "r") as f:
    fellows_data = [json.loads(line) for line in f]

sentences = []

for line in fellows_data:
    sentence = "Received an award {}. Affiliation is {}. Interests are {}.".format(
        line["citation"],
        line["affiliation"],
        line["interests"],
    )
    sentences.append(sentence)

embeddings = vs.get_sbert_embeddings(sentences)
embeddings = vs.get_pca_reductions(embeddings)
embeddings = vs.get_tsne_3d_reductions(embeddings)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i, (x, y, z) in enumerate(embeddings):
    ax.scatter(x, y, z, label=f"Point {i}")
    ax.text(x, y, z, f"{fellows_data[i]["full_named"]}", color='red')
ax.set_title('3D Semantic Similarity Map')
plt.show()
