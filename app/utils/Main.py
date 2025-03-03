from pdf_reader import readPDF
from comparison import comparePDF,compareTemplate

reference,user,template=readPDF()
#print(comparePDF(reference,user))
print(compareTemplate(template,user))