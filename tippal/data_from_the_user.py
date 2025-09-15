import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer, CrossEncoder
# from load_index import index, metadata
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import vertexai
from vertexai.generative_models import GenerativeModel
import requests
from embedding import embedding_sentences
import re


embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
vertexai.init(project="valiant-airlock-448312-k6")


def insert_to_index(data):
    import requests
    print("enter insert")

    prompt = f"""From the following data, return a list of advice and tips without any interpretations. Here is the data::{data}"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code == 200:
            tips_list = response.json()["response"]
            print("Response from Ollama:", tips_list)
            text_chunks = tips_list.split('.')
            text_chunks = [chunk.strip() for chunk in text_chunks if chunk.strip() and re.search(r'[a-zA-Zא-ת]', chunk)]
            print(text_chunks)
            embedding_sentences(text_chunks)
            return True
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.text}")
            return False
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return False

