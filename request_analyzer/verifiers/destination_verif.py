import os
import numpy as np
import pickle
import faiss
from sentence_transformers import SentenceTransformer


def get_project_root():
    """Return the absolute path to the project root."""
    # Assuming the script is run from within the project structure,
    # and the root contains a 'LICENSE' file.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_marker_file = 'data'
    
    while current_dir!= '/' and root_marker_file not in os.listdir(current_dir):
        current_dir = os.path.dirname(current_dir)
    
    if root_marker_file in os.listdir(current_dir):
        return current_dir
    else:
        raise FileNotFoundError(f"Could not locate {root_marker_file} to determine project root.")
    
project_root = get_project_root()
city_embeddings_path = os.path.join(project_root, 'data', 'city_embeddings.npy')
city_names_path = os.path.join(project_root, 'data', 'city_names.pkl')


# Load embeddings and city names from disk
city_embeddings = np.load(city_embeddings_path)
with open(city_names_path, 'rb') as f:
    city_names = pickle.load(f)

# Initialize FAISS index and load embeddings
index = faiss.IndexFlatL2(city_embeddings.shape[1])  # L2 distance metric
index.add(city_embeddings)  # Add city embeddings to the index

# Load the same model used for generating embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def search_city(query, city_names, model, index, k=1):
    query_embedding = model.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, k)
    results = [city_names[idx] for idx in indices[0]]
    return results



# Example usage
query_city = "Иннплис"
results = search_city(query_city, city_names, model, index)
print(f"The closest city name(s) to '{query_city}' is/are: {results}")