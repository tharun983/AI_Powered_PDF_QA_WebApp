import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load pre-trained model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def load_preprocessed_text(file_path):
    """
    Loads the preprocessed text from a file and splits it into chunks.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into lines or sentences
    return text.split('\n\n')  # Or use a sentence splitter if necessary

def build_faiss_index(texts):
    """
    Builds a FAISS index from a list of texts.
    """
    # Convert texts to embeddings
    embeddings = model.encode(texts)
    
    # Create a FAISS index
    dimension = embeddings.shape[1]  # Dimension of embedding
    index = faiss.IndexFlatL2(dimension)  # L2 distance metric
    index.add(np.array(embeddings))  # Add embeddings to index
    
    return index, texts

def search_faiss_index(index, query, texts, k=5):
    """
    Searches the FAISS index for the closest matches to the query.
    """
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)
    
    return [(texts[i], distances[0][idx]) for idx, i in enumerate(indices[0])]
