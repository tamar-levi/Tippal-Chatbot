import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

index = faiss.read_index(r"C:\tippal\venv\tippal1.index")
# print(f"Number of vectors in the index before adding: {index.ntotal}")

with open(r"C:\tippal\tippal_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

