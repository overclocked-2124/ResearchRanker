import requests
import fitz 
import re
import os
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def extract_title(pdf_path):
    doc = fitz.open(pdf_path)
    first_page = doc[0]
    blocks = first_page.get_text("dict")['blocks']

    largest_text = ""
    max_size = 0
    for block in blocks:
        if block['type'] == 0: 
            for line in block['lines']:
                for span in line['spans']:
                    font_size = span['size']
                    text = span['text']
                    if font_size >= max_size:
                        max_size = font_size
                        largest_text += text
    largest_text = re.sub(r'\[.*?\]', '', largest_text)  # remove things like [Undergraduate...]
    largest_text = re.sub(r'[^\w\s]', '', largest_text)  # remove punctuation
    largest_text = re.sub(r'\s+', ' ', largest_text)     # remove extra spaces
    return largest_text if largest_text else "No title found"

def coreAPICall(title):
    params = {
    "q": title ,        
    "hasFullText": "true",           
    "limit": 20,                     
    "apiKey": "H9F2ZVkoQpcYyXazGhlSsunLIUm5Cext"
}
    URL = f"https://api.core.ac.uk/v3/search/works"
    try:
        response = requests.get(URL, params=params )
        response.raise_for_status()
        data=response.json()
        results=data.get("results",[])
        urls =[]
        for result in results:
            downloadurl = result.get("downloadUrl")
            if downloadurl is None:
                continue
            else:
                urls.append(downloadurl)
        pdf_urls = [url for url in urls if re.search(r'\.pdf$', url)]
        print(pdf_urls[0])
        return pdf_urls[0]
    
    except requests.exceptions.RequestException as e:
        print(f"API Key test failed: {str(e)}")

def download_pdf_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content  # Return the PDF bytes
    except requests.exceptions.RequestException as e:
        print(f"Failed to download PDF: {str(e)}")
        return None

def extract_text_from_pdf_bytes(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes,filetype="pdf")
    full_text = ''
    for pgno in range(len(doc)):
        page = doc[pgno]
        full_text += page.get_text()
    doc.close()
    return full_text if full_text.strip() else "no text found"


 
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
 