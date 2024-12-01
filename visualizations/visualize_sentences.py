# visualize_sentences.py
#
# Provide some visualization functions with suitable parameters for ACM
#   fellows and their respective publications.


from sentence_transformers import SentenceTransformer

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


### Basic Functions (With Established Parameters)
def scale_embeddings(embeddings):
    scaler = MinMaxScaler()
    embeddings = scaler.fit_transform(embeddings)
    return embeddings


def get_sbert_embeddings(sentences):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(sentences)

    return embeddings


def get_tsne_3d_reductions(embeddings):
    tsne = TSNE(n_components=3, perplexity=4, metric="cosine")
    embeddings = tsne.fit_transform(embeddings)
    
    return embeddings


def get_pca_reductions(embeddings):
    pca = PCA(n_components=50)
    embeddings = pca.fit_transform(embeddings)


def k_means_cluster(embeddings):
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(embeddings)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    return labels, centroids


def visualize_3d_embeddings(embeddings):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # ax.scatter(embeddings_3d[:, 0], embeddings_3d[:, 1], embeddings_3d[:, 2])
    for i, (x, y, z) in enumerate(embeddings):
        ax.scatter(x, y, z, label=f"Point {i}")
        ax.text(x, y, z, f"{i}", color='red')
    ax.set_title('3D Semantic Similarity Map')
    plt.show()


### Pipelined Functions




if __name__ == "__main__":
    # sentences = [
    #     "The weather is lovely today.",
    #     "It's so sunny outside!",
    #     "There are rain clouds outdoors."
    #     "He drove to the stadium.",
    #     "Japan is a lovely country.",
    #     "This paper discusses the ethical implications of autonomous vehicles.",
    #     "Spaghetti can be made al dente for optimal texture."
    # ]
    pass