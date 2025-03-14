import re
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

#Downloading the tokeniser (required only when running the code for first-time)
nltk.download("punkt_tab")

#Loading the S-BERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

def preprocess_text(text:str):
    """Pre-processes the text by lowercasing, removing special characters, and tokenizing into sentences."""

    #Converts into lower-case
    text = text.lower()

    #Removes special characters
    text = re.sub(r'[^a-zA-Z0-9]', '', text)

    #Tokenises into sentences
    sentences = sent_tokenize(text)

    return sentences

def get_sentence_embeddings(sentences:list[str]):
    """Converts sentences into vector embeddings using S-BERT"""

    return model.encode(sentences, convert_to_tensor=True)

def compute_similarity(text1, text2):
    """Calculates similarity score between two texts"""

    #Text Pre-processing
    sentences1 = preprocess_text(text1)
    sentences2 = preprocess_text(text2)

    #Generating Embeddings
    embeddings1 = get_sentence_embeddings(sentences1)
    embeddings2 = get_sentence_embeddings(sentences2)

    #Calculating co-sine similarities
    similarities = cosine_similarity(embeddings1.cpu().numpy(), embeddings2.cpu().numpy())

    #Calculating the final similarity score (out of 1)
    avg_similarity = np.mean(similarities)

    return avg_similarity

#Should incorporate llm-based analysis