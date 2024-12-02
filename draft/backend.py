import os
import json
import logging
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import uvicorn
import nest_asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
nest_asyncio.apply()

# Initialize FastAPI app
app = FastAPI()

# Model configuration
MODEL_NAME = "BAAI/bge-m3"
embedding_function = HuggingFaceBgeEmbeddings(model_name=MODEL_NAME)

# Chroma persistent directory
PERSIST_DIR = "./chroma_db"

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

@app.get("/search_with_scores")
async def search_with_scores(
    query: str = Query(..., description="Search query text"),
    k: int = Query(5, description="Number of results to fetch")
):
    """
    Perform a similarity search for a given query and return results with similarity scores.
    Add suggestions for documents missing abstracts.
    """
    try:
        # Initialize Chroma collection
        user_id = "default_user"
        text_store = get_text_collection(user_id)

        # Perform similarity search with scores
        results = text_store.similarity_search_with_score(query, k=k)

        if not results:
            return {"results": [], "message": "No matching results found."}

        # Separate results with and without abstracts
        results_with_abstract = []
        suggestions = []

        for doc, score in results:
            if "Abstract not found" in doc.page_content or "failed to load" in doc.page_content:
                suggestions.append({
                    "title": doc.metadata.get("title", "Unknown Title"),
                    "url": doc.metadata.get("url", "No URL"),
                    "similarity_score": score
                })
            else:
                results_with_abstract.append({
                    "title": doc.metadata.get("title", "Unknown Title"),
                    "url": doc.metadata.get("url", "No URL"),
                    "content_snippet": doc.page_content[:100],  # Limit to 100 characters for snippet
                    "similarity_score": score
                })

        response = {"results": results_with_abstract}

        # Add suggestions if available
        if suggestions:
            response["suggestions"] = suggestions

        return response

    except Exception as e:
        logger.error(f"Error during similarity search: {e}")
        return JSONResponse(status_code=500, content={"message": "An error occurred during search."})

if __name__ == "__main__":
    # Ensure the persistent directory exists
    os.makedirs(PERSIST_DIR, exist_ok=True)
    
    # Run the FastAPI app
    uvicorn.run(app, host="127.0.0.1", port=8000)
