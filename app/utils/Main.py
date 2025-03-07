from pdf_reader import readPDF
from comparison import comparePDF,compareTemplate


model = "llama3.2" #Change to required model


reference,user,template=readPDF()
#print(comparePDF(reference,user,model))
print(compareTemplate(template,user,model))