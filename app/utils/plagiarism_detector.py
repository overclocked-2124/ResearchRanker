import requests
import fitz 

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
    return largest_text if largest_text else "No title found"

def coreAPICall(title):
    API_KEY = "H9F2ZVkoQpcYyXazGhlSsunLIUm5Cext"  
    QUERY='title'
    URL = f"https://api.core.ac.uk/v3/search/works?q={QUERY}&apikey={API_KEY}"
    response = requests.get(URL)
