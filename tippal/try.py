# import faiss
# import pickle
# import os
# import numpy as np
# # Function to remove the last added vector from FAISS index and update metadata
# def remove_last_entry():
#     # Load the FAISS index
#     index = faiss.read_index(r"C:\tippal\venv\tippal1.index")
#
#     # Load the metadata (text chunks)
#     with open(r"C:\tippal\venv\tippal_metadata.pkl", "rb") as f:
#         metadata = pickle.load(f)
#
#     # Check the number of vectors in the index
#     num_vectors = index.ntotal
#     print(f"Number of vectors before removal: {num_vectors}")
#
#     if num_vectors > 0:
#         # Get the ID of the last vector (FAISS uses 0-based indexing)
#         last_index_id = num_vectors - 1
#         print(f"Removing vector with ID: {last_index_id}")
#
#         # Remove the vector from the FAISS index
#         index.remove_ids(np.array([last_index_id]))
#         print(f"Number of vectors after removal: {index.ntotal}")
#
#         # Safely remove the last text chunk from metadata
#         print(len(metadata["text_chunks"]))
#         if len(metadata["text_chunks"]) > 0:
#             metadata["text_chunks"].pop()  # Removes the last chunk
#             print(len(metadata["text_chunks"]))
#             print("Last text chunk removed from metadata.")
#
#         # Save the updated index
#         faiss.write_index(index, r"C:\tippal\venv\tippal1.index")
#
#         # Save the updated metadata
#         with open("tippal_metadata.pkl", "wb") as f:
#             pickle.dump(metadata, f)
#
#         print("Last vector and metadata updated successfully.")
#     else:
#         print("No vectors to remove.")
#
# # Call the function to remove the last entry
# remove_last_entry()
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

# Load the SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Function to save both the embeddings and metadata
def embedding_sentences(text_chunks):
    embeddings = model.encode(text_chunks)
    vector_dim = embeddings.shape[1]
    print(f"The dimension of the embeddings is: {vector_dim}")

    # Initialize the FAISS index
    if not os.path.exists("tippal1.index"):
        index = faiss.IndexFlatL2(vector_dim)
    else:
        index = faiss.read_index("tippal1.index")

    print(f"Number of vectors in the index before adding: {index.ntotal}")
    index.add(embeddings)
    print(f"Number of vectors in the index after adding: {index.ntotal}")

    # Save the index to disk
    faiss.write_index(index, r"C:\tippal\venv\tippal1.index")

    # Save metadata (text chunks)
    metadata = {"text_chunks": text_chunks}
    with open("tippal_metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)
    print("Metadata saved successfully!")

# Example: Extract text from a PDF (for testing purposes)
reader = PdfReader(r'C:\tippal\english_tips.pdf')
all_text = ""
for page in reader.pages:
    all_text += page.extract_text()
text_chunks = all_text.split('.')

# Call the function to process the text chunks and save the embeddings and metadata
embedding_sentences(text_chunks)
