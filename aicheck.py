import ollama
import markdown

def aisug(pdf_res, model="tinyllama:1.1b"):
    system_prompt = """
    You are a PDF analyzing expert.
    - User provides errors in a research paper.
    - Return the best possible suggestions related to each error in an HTML table format.
    - The output should be user-friendly and neatly ordered.
    """

    # Proper message structure for Ollama
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": pdf_res}
    ]

    response = ollama.chat(model=model, messages=messages)

    # Extracting response content correctly
    markdown_res = markdown.markdown(response['message']['content'])
    return markdown_res

# Test call
print(aisug("What is the capital of India?"))
