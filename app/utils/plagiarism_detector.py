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
    params = {
    "q": title ,        # your search query
    "hasFullText": "true",           # only return items with full text
    "limit": 10,                     # number of results
    "apiKey": "H9F2ZVkoQpcYyXazGhlSsunLIUm5Cext"
}
    URL = f"https://api.core.ac.uk/v3/search/works"
    try:
        response = requests.get(URL, params=params )
        response.raise_for_status()
        data=response.json()
        results=data.get("results",[])
        print(data)
        dois = []
        url =[]
        for result in results:
            doi = result.get("doi")
            if doi is None:
                continue
            else:
                dois.append(doi)
        return dois
        
    except requests.exceptions.RequestException as e:
        print(f"API Key test failed: {str(e)}")



coreAPICall('gay')