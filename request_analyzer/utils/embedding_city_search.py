import os
import numpy as np
import pickle
import faiss
from sentence_transformers import SentenceTransformer

class EmbeddingCitySearch():

    def __init__(self) -> None:
        self.project_root = self._get_project_root()
        self.city_embeddings_path = os.path.join(self.project_root, 'data', 'city_embeddings.npy')
        self.city_names_path = os.path.join(self.project_root, 'data', 'city_names.pkl')
        
        # Load embeddings and city names from disk
        self.city_embeddings = np.load(self.city_embeddings_path)
        with open(self.city_names_path, 'rb') as f:
            self.city_names = pickle.load(f)
        
        # Initialize FAISS index and load embeddings
        self.index = faiss.IndexFlatL2(self.city_embeddings.shape[1])  # L2 distance metric
        self.index.add(self.city_embeddings)  # Add city embeddings to the index

        # Load the same model used for generating embeddings
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def search_city(self, query, k=1):
        query_embedding = self.model.encode([query]).astype('float32')
        distances, indices = self.index.search(query_embedding, k)
        results = [self.city_names[idx] for idx in indices[0]]
        return results, distances
            
    
    def _get_project_root(self):
        """Return the absolute path to the project root."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_marker_file = 'data'
        
        while current_dir != '/' and root_marker_file not in os.listdir(current_dir):
            current_dir = os.path.dirname(current_dir)
        
        if root_marker_file in os.listdir(current_dir):
            return current_dir
        else:
            raise FileNotFoundError(f"Could not locate {root_marker_file} to determine project root.")
        
        
# Example usage
query_city = "Иннплdcscsdcsис"

searcher = EmbeddingCitySearch()
print(searcher.search_city(query_city))