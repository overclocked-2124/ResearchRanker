import pymupdf  

def readPDF(file_path):
    doc = pymupdf.open(file_path)
    extracted_text=""

    for page in doc:
        text=page.get_text()
        extracted_text+=text
    
    return(extracted_text)