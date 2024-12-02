import os
import json
import logging
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sentence_transformers import SentenceTransformer
import uvicorn
import nest_asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
nest_asyncio.apply()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8050"],  # Allow both React and Dash
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model configuration
MODEL_NAME = "all-MiniLM-L6-v2"
embedding_function = HuggingFaceBgeEmbeddings(model_name=MODEL_NAME)

# Chroma persistent directory
PERSIST_DIR = "./chroma_db_final"

def get_text_collection(user_id: str):
    """
    Initializes or retrieves a Chroma vector store for textual data using the provided user ID.
    """
    collection_name = f"{user_id}_text_collection"
    return Chroma(
        collection_name=collection_name,
        embedding_function=embedding_function,
        persist_directory=PERSIST_DIR,
    )

def get_sbert_embeddings(sentences):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(sentences)

def get_tsne_3d_reductions(embeddings):
    tsne = TSNE(n_components=3, perplexity=4, metric="cosine")
    return tsne.fit_transform(embeddings)

def k_means_cluster(embeddings):
    kmeans = KMeans(n_clusters=10)
    kmeans.fit(embeddings)
    return kmeans.labels_, kmeans.cluster_centers_

def scale_embeddings(embeddings):
    scaler = MinMaxScaler()
    return scaler.fit_transform(embeddings)

def check_chroma_db():
    try:
        user_id = "default_user"
        text_store = get_text_collection(user_id)
        count = text_store._collection.count()
        logger.info(f"Chroma DB check - Collection exists at: {PERSIST_DIR}")
        logger.info(f"Chroma DB check - Number of documents: {count}")
        
        # Get a sample document if any exist
        if count > 0:
            sample = text_store._collection.peek()
            logger.info(f"Chroma DB check - Sample document exists: {bool(sample)}")
        return count
    except Exception as e:
        logger.error(f"Chroma DB check failed: {str(e)}")
        return 0

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")
    doc_count = check_chroma_db()
    if doc_count == 0:
        logger.error("No documents found in Chroma DB! Please ensure the database is properly initialized.")

@app.get("/search_with_scores")
async def search_with_scores(
    query: str = Query(..., description="Search query text"),
    k: int = Query(5, description="Number of results to fetch")
):
    try:
        user_id = "default_user"
        text_store = get_text_collection(user_id)
        results = text_store.similarity_search_with_score(query, k=k)

        if not results:
            logger.warning("No matching results found.")
            return {"results": [], "message": "No matching results found."}

        results_with_abstract = []
        suggestions = []

        for doc, score in results:
            if "Abstract not found" in doc.page_content or "failed to load" in doc.page_content:
                suggestions.append({
                    "title": doc.metadata.get("title", "Unknown Title"),
                    "url": doc.metadata.get("url", "No URL"),
                    "similarity_score": float(score),
                })
            else:
                results_with_abstract.append({
                    "title": doc.metadata.get("title", "Unknown Title"),
                    "url": doc.metadata.get("url", "No URL"),
                    "content_snippet": doc.page_content[:100],
                    "similarity_score": float(score),
                })

        response = {"results": results_with_abstract}
        if suggestions:
            response["suggestions"] = suggestions

        logger.info(f"Search results: {response}")
        return response

    except Exception as e:
        logger.error(f"Error during similarity search: {e}")
        return JSONResponse(status_code=500, content={"message": "An error occurred during search."})


@app.get("/visualize_embeddings")
async def visualize_embeddings():
    """
    Endpoint to process embeddings and clustering for visualization.
    """
    try:
        # READ DATA
        filepath = "data/acm_fellows.csv"
        df = pd.read_csv(filepath).head(500)

        # Construct sentences
        sentences = [
            f"Received an award {row.Citation}. Interests are {row.Interests}."
            for row in df.itertuples()
        ]

        # EMBEDDINGS AND CLUSTERING
        embeddings = get_sbert_embeddings(sentences)
        embeddings = get_tsne_3d_reductions(embeddings)
        cluster_labels, _ = k_means_cluster(embeddings)
        embeddings = scale_embeddings(embeddings)

        # Convert embeddings and labels to JSON serializable format
        visualization_data = [
            {
                "x": float(embedding[0]),
                "y": float(embedding[1]),
                "z": float(embedding[2]),
                "cluster": int(cluster),
                "citation": df.iloc[idx]["Citation"],
                "last_name": df.iloc[idx]["Last Name"],
                "given_name": df.iloc[idx]["Given Name"],
            }
            for idx, (embedding, cluster) in enumerate(zip(embeddings, cluster_labels))
        ]

        return {"data": visualization_data}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {e}"})


if __name__ == "__main__":
    os.makedirs(PERSIST_DIR, exist_ok=True)
    import sys
    import uvicorn

    # Dynamically resolve the module name for reload
    module_name = __name__.split(".")[0]
    # Pass the app as a module import string
    uvicorn.run(f"{module_name}:app", host="127.0.0.1", port=8000, reload=True)  
