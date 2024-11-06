from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
from typing import List
import chromadb
from chromadb.utils import Persistence
from utils import extract_text_from_file
import asyncio

app = FastAPI()

# Load the sentence transformer model for embeddings (CPU)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Initialize ChromaDB persistent client
client = chromadb.Client(persistent=True)
collection = client.get_or_create_collection("documents")

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Ingests a document, extracts text, computes embeddings, and stores in ChromaDB.
    """
    # Read and process file asynchronously
    content = await file.read()
    text_content = await extract_text_from_file(content, file.filename)

    # Handle cases where text extraction fails
    if not text_content:
        raise HTTPException(status_code=400, detail="Failed to extract text from document.")

    # Compute embeddings
    embedding = model.encode(text_content).tolist()

    # Store the document's text and embeddings in ChromaDB
    collection.insert({"text": text_content, "embedding": embedding})
    return JSONResponse(content={"status": "Document ingested successfully"})

@app.get("/query")
async def query_documents(query: str, top_k: int = 5):
    """
    Retrieves the most similar documents to the query.
    """
    query_embedding = model.encode(query).tolist()
    results = collection.query({"embedding": query_embedding}, top_k=top_k)

    # Return the top-k most similar documents
    return {"results": results}

# Endpoint to clear the collection, if needed
@app.delete("/clear")
async def clear_collection():
    collection.clear()
    return {"status": "Collection cleared."}
