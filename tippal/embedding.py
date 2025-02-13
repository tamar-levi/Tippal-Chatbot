# importing required modules
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os
from load_index import index, metadata
# creating a pdf reader object


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


# reader = PdfReader(r'C:\tippal\english_tips.pdf')
# all_text = ""
# for page in reader.pages:
#         all_text += page.extract_text()
# text_chunks = all_text.split('.')
# embedding_sentences(text_chunks)


def embedding_sentences(text_chunks):
    """
    Add new text chunks to the existing metadata and update the FAISS index.
    """
    # Append new text chunks to the existing metadata
    metadata["text_chunks"].extend(text_chunks)
    print(f"Added {len(text_chunks)} new text chunks to metadata.")

    # Encode the new text chunks into embeddings
    embeddings = model.encode(text_chunks)
    vector_dim = embeddings.shape[1]
    print(f"The dimension of the embeddings is: {vector_dim}")

    # Add new embeddings to the existing FAISS index
    print(f"Number of vectors in the index before adding: {index.ntotal}")
    index.add(embeddings)
    print(f"Number of vectors in the index after adding: {index.ntotal}")

    # Save the updated FAISS index
    faiss.write_index(index, r"C:\tippal\venv\tippal1.index")
    print("FAISS index updated and saved successfully.")

    # Save the updated metadata
    metadata_path = r"C:\tippal\tippal_metadata.pkl"
    with open(metadata_path, "wb") as f:
        pickle.dump(metadata, f)
    print(f"Metadata saved successfully! Total text chunks: {len(metadata['text_chunks'])}")