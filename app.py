from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vectorDB import build_faiss_index, search_faiss_index, load_preprocessed_text
from cohere import Client

# Load the text and build the FAISS index
texts = load_preprocessed_text('preprocessed_output.txt')
index, corpus = build_faiss_index(texts)

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",  # Frontend (React, Vue, etc.) port
    "http://your-frontend-url.com"  # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific domains to access the API
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define the request models
class QueryRequest(BaseModel):
    query: str
    k: int = 5  # Number of results to return (default 5)

class AgentRequest(BaseModel):
    query: str
    use_vectordb: bool  # Flag to choose between VectorDB or Cohere directly

# Initialize Cohere client (replace with your API key)
cohere_client = Client("8wgcLA8KR8GmgAHaM73oaE7I6mgx6lRuTVdqWKkN")


@app.get("/")
def read_root():
    return {"message": "VectorDB is running!"}


@app.post("/search/")
def search(request: QueryRequest):
    results = search_faiss_index(index, request.query, corpus, request.k)
    return {"results": results}


@app.post("/search_and_answer/")
def search_and_answer(request: QueryRequest):
    print(f"Received query: {request.query}")

    # Get results from the FAISS index
    results = search_faiss_index(index, request.query, corpus, request.k)
    print(f"FAISS search results: {results}")

    # Add type checking and ensure that results are in the expected format
    relevant_results = []
    threshold = 0.4

    for res in results:
        print(f"Result: {res}, Type of score: {type(res[0])}")
        if isinstance(res[0], (float, int)) and res[0] > threshold:
            relevant_results.append(res)

    print(f"Relevant results found: {relevant_results}")

    if relevant_results:
        return {"source": "VectorDB", "results": relevant_results}
    else:
        # Fallback to Cohere model for generating an answer
        cohere_response = cohere_client.generate(
            model='command-r-plus',  # Use an available model ID
            prompt=request.query,
            max_tokens=150,
            temperature=0.9
        )
        return {"source": "Cohere", "answer": cohere_response.generations[0].text.strip()}


@app.post("/agent/")
def agent(request: AgentRequest):
    """
    The agent endpoint allows the user to manually select whether the query
    should go through the VectorDB first or directly to Cohere.
    """
    query = request.query

    if request.use_vectordb:
        # Step 1: First go to VectorDB
        results = search_faiss_index(index, query, corpus, 5)
        print(f"FAISS search results: {results}")
        
        # Add type checking and ensure that results are in the expected format
        relevant_results = []
        threshold = 0.4

        for res in results:
            print(f"Result: {res}, Type of score: {type(res[0])}")
            if isinstance(res[0], (float, int)) and res[0] > threshold:
                relevant_results.append(res)

        if relevant_results:
            # Use the VectorDB result in Cohere API
            cohere_response = cohere_client.generate(
                model='command-r-plus',
                prompt=f"Based on the following information: {relevant_results}\n{query}",
                max_tokens=150,
                temperature=0.9
            )
            return {"source": "VectorDB + Cohere", "answer": cohere_response.generations[0].text.strip()}
        else:
            # If no relevant results, directly fall back to Cohere
            cohere_response = cohere_client.generate(
                model='command-r-plus',
                prompt=query,
                max_tokens=150,
                temperature=0.9
            )
            return {"source": "Cohere", "answer": cohere_response.generations[0].text.strip()}

    else:
        # Directly query Cohere
        cohere_response = cohere_client.generate(
            model='command-r-plus',
            prompt=query,
            max_tokens=150,
            temperature=0.9
        )
        return {"source": "Cohere", "answer": cohere_response.generations[0].text.strip()}
