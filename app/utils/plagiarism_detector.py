import requests
import fitz 
import re
import os
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import ollama

def extract_title(pdf_path):
    doc = fitz.open(pdf_path)
    first_page = doc[0]
    first_page_text=first_page.get_text()
    generated_titles=ollama.generate(model="gemma3:4b",
        system = """
    You are a research paper assistant. Your job is to analyze the first page of a scientific research paper, 
    understand the context, goals, and subject, and propose three high-quality, publication-ready titles.


    Guidelines:
    - Titles should be concise, clear, and reflect the core idea or methodology.
    - Use technical terms only if they are well-established in the field.
    - simpilfy the titles for an extrenal api call
    - Return ONLY the three titles as a single line, separated by a comma. Do not include labels, explanations, or extra lines.
    - Only output: Title 1, Title 2 ,Title 3
    """,
    prompt=f"""
    [First Page of Research Paper]
    {first_page_text}
    Return two suitable titles in the format: Title 1, Title 2, Title 3
    """,
    options={
        "temperature": 0.3
        }
    ,stream=False)['response']
    titles = generated_titles.split(",")
    titles = [t.strip() for t in titles]
    for x in titles :
        print(x)
    return titles


def coreAPICall(title):
    params = {
    "q": title ,        
    "hasFullText": "true",           
    "limit": 15,                     
    "apiKey": "H9F2ZVkoQpcYyXazGhlSsunLIUm5Cext"
}
    URL = f"https://api.core.ac.uk/v3/search/works"
    try:
        response = requests.get(URL, params=params )
        response.raise_for_status()
        data=response.json()
        results=data.get("results",[])
        urls_temp =[]
        for result in results:
            downloadurl = result.get("downloadUrl")
            if downloadurl is None:
                continue
            else:
                urls_temp.append(downloadurl)
        pdf_urls = [url for url in urls_temp if re.search(r'\.pdf$', url)]
        return pdf_urls[:2]
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
    return full_text if full_text.strip() else ""


 
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
 