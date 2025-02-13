import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer, CrossEncoder
from load_index import index, metadata
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import vertexai
from vertexai.generative_models import GenerativeModel
import requests

embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
vertexai.init(project="valiant-airlock-448312-k6")

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def correct_query_res(q):
    qur_result = []
    q_embeddings = embedding_model .encode([q])
    distances, indices = index.search(q_embeddings, 5)
    query_chunk_pairs = [(q, metadata["text_chunks"][i]) for i in indices[0]]
    print(f"Query chunk pairs: {query_chunk_pairs}")  # Debugging line
    print(f"Indices: {indices}")  # Debugging line
    print(f"Distances: {distances}")  # Debugging line
    re_rank_scores = cross_encoder.predict(query_chunk_pairs)
    results = list(zip(indices[0], distances[0], re_rank_scores))
    results.sort(key=lambda x: x[2], reverse=True)

    for i, distance, score in results:
        re_score = sigmoid(score)
        if re_score > 0.7:  # Filter based on re-ranking score
            print(f"Chunk ID: {i}")
            print(f"Text: {metadata['text_chunks'][i]}")
            print(f"Distance: {distance}")
            print(f"Re-Rank Score: {re_score}")
            print("-" * 50)
            qur_result.append(metadata['text_chunks'][i])
    return qur_result




def query_res(query):
    results = correct_query_res(query)
    if not results:
        return "I have no information on the subject you asked."
    results_text = ".".join(results)
    results_text += "."
    print(results_text)
    prompt = f"""Summarize the following query results in natural language:
             Query: '{query}'
             Results: {results_text}
             Summary: Provide a concise, well-structured paragraph that highlights the key insights from the results."""

    # שליחת הפרומפט ל-Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",  # הכתובת של Ollama
        json={
            "model": "mistral",  # המודל שבו אתם משתמשים
            "prompt": prompt,  # הפרומפט
            "stream": False  # לא להשתמש בתזרים (stream)
        }
    )

    # הדפסת התשובה
    if response.status_code == 200:
        print("Response from Ollama:")
        print(response.json()["response"])
        return response.json()["response"]




# import faiss
# import numpy as np
# import pickle
# from sentence_transformers import SentenceTransformer, CrossEncoder
# from load_index import index, metadata
# from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
# import vertexai
# from vertexai.generative_models import GenerativeModel
# import requests
# import logging
#
# # Initialize logging
# logging.basicConfig(level=logging.DEBUG)
#
# # Initialize models and FAISS index
# embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
# vertexai.init(project="valiant-airlock-448312-k6")
#
# def sigmoid(x):
#     return 1 / (1 + np.exp(-x))

# def correct_query_res(q):
#     try:
#         print("1")
#         qur_result = []
#         q_embeddings = embedding_model.encode([q])
#         print("2")
#         distances, indices = index.search(q_embeddings, 5)
#         print(f"Indices: {indices}")  # Debugging line
#         print(f"Distances: {distances}")  # Debugging line
#         logging.debug(f"Length of text_chunks: {len(metadata['text_chunks'])}")
#         logging.debug(f"Indices returned by FAISS: {indices}")
#         print("3")
#         query_chunk_pairs = [(q, metadata["text_chunks"][i]) for i in indices[0]]
#         print(f"Query chunk pairs: {query_chunk_pairs}")  # Debugging line
#         re_rank_scores = cross_encoder.predict(query_chunk_pairs)
#         results = list(zip(indices[0], distances[0], re_rank_scores))
#         results.sort(key=lambda x: x[2], reverse=True)
#
#         for i, distance, score in results:
#             re_score = sigmoid(score)
#             if re_score > 0.7:  # Filter based on re-ranking score
#                 print(f"Chunk ID: {i}")
#                 print(f"Text: {metadata['text_chunks'][i]}")
#                 print(f"Distance: {distance}")
#                 print(f"Re-Rank Score: {re_score}")
#                 print("-" * 50)
#                 qur_result.append(metadata['text_chunks'][i])
#         return qur_result
#     except Exception as e:
#         logging.error(f"Error in correct_query_res: {str(e)}")
#         return None  # Return None to indicate failure
#
# def query_res(query):
#     try:
#         results = correct_query_res(query)
#         if not results:
#             return "I have no information on the subject you asked."
#         results_text = ".".join(results)
#         results_text += "."
#         print(results_text)
#         prompt = f"""Summarize the following query results in natural language:
#                  Query: '{query}'
#                  Results: {results_text}
#                  Summary: Provide a concise, well-structured paragraph that highlights the key insights from the results."""
#
#         # Send prompt to Ollama
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": "mistral",
#                 "prompt": prompt,
#                 "stream": False
#             }
#         )
#
#         # Check response status
#         if response.status_code == 200:
#             print("Response from Ollama:")
#             print(response.json()["response"])
#             return response.json()["response"]
#         else:
#             logging.error(f"Ollama API error: {response.status_code}, {response.text}")
#             return "An error occurred while generating the response."
#     except Exception as e:
#         logging.error(f"Error in query_res: {str(e)}")
#         return "An error occurred while processing your query."