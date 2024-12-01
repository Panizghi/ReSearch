import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mplcursors

import pandas as pd
import numpy as np

import visualize_sentences as vs


# READ DATA
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


# EMBEDDINGS AND CLUSTERING
embeddings = vs.get_sbert_embeddings(sentences)
# embeddings = vs.get_pca_reductions(embeddings)
embeddings = vs.get_tsne_3d_reductions(embeddings)
cluster_labels, cluster_centroids = vs.k_means_cluster(embeddings)
embeddings = vs.scale_embeddings(embeddings)


# OUTPUT TO CSV
df_exp = df[["Last Name", "Given Name", "Citation"]]
visualizations_data = np.column_stack((embeddings, cluster_labels, df_exp.to_numpy()))
out_df = pd.DataFrame(visualizations_data, columns=["x", "y", "z", "cluster", "last name", "given name", "citation"])
out_df.to_csv("visualization.csv")


# MATPLOTLIB GRAPHING
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(embeddings[:,0], embeddings[:,1], embeddings[:,2], c=cluster_labels)

cursor = mplcursors.cursor(ax, hover=True)
@cursor.connect("add")
def on_add(sel):
    index = sel.index
    # sel.annotation.set_text(df.loc[index, "Last Name"])
    sel.annotation.set_text(df.loc[index, "Citation"])

ax.set_title('3D Semantic Similarity Map')
plt.show()
