from PyPDF2 import PdfReader

def readPDF():
    reference = ""
    user = ""
    template = ""
    reader_r = PdfReader('Reference.pdf')  # replace with desired file
    reader_u = PdfReader('User.pdf')
    reader_t = PdfReader('Template.pdf')

    n_pages_r = len(reader_r.pages)
    n_pages_u = len(reader_u.pages)
    n_pages_t = len(reader_t.pages)

    for i in range(n_pages_r):
        page_r = reader_r.pages[i]
        reference += page_r.extract_text()

    for i in range(n_pages_u):
        page_u = reader_u.pages[i]
        user += page_u.extract_text()

        for i in range(n_pages_t):
            page_t = reader_t.pages[i]
            template += page_t.extract_text()


    return reference,user,template

