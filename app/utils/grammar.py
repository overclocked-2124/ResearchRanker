import ollama
import markdown
import PyPDF2
import language_tool_python
import nltk
import sys

nltk.download('punkt')

def aisug(pdf_res, model="tinyllama:1.1b"):
    """
    Generates AI suggestions based on grammar errors in HTML format.
    
    Args:
        pdf_res (dict): Dictionary containing grammar and spelling issues.
        model (str): The Ollama model to use for generating suggestions.
    
    Returns:
        str: HTML-formatted suggestions.
    """
    system_prompt = """
    You are a PDF analyzing expert. The user provides errors in a research paper.
    For each error, provide a clear and actionable suggestion to fix it.
    Keep the response concise and focused on the error.
    
    """

    error_text = "\n".join(
        f"Page {err['page']}: {err['issue_type']} - {err['message']} (Sentence: {err['sentence']})"
        for err in pdf_res.get("errors", [])
    )

    full_prompt = system_prompt + "\n" + error_text

    try:
        response = ollama.chat(model=model, messages=[{'role': 'user', 'content': full_prompt}])
    except Exception as e:
        print(f"Error calling Ollama API: {e}", file=sys.stderr)
        return "<p>Error generating suggestions. Please try again later.</p>"

    if isinstance(response, dict):
        content = response.get('message', {}).get('content', str(response))
    else:
        content = str(response)

    # Parse the model's response for suggestions
    suggestions = {}
    if content:
        for line in content.split("\n"):
            if "Page" in line and ":" in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    page = parts[0].replace("Page", "").strip()
                    suggestion = parts[1].strip()
                    suggestions[page] = suggestion

    # Generate the HTML table
    table_rows = []
    for err in pdf_res.get("errors", []):
        page = str(err['page'])
        full_prompt1="""
        Reply with suggestions for errors mentioned in prompt by user,
        -Act as English grammar expert and spellings master.
        -Correct users mistakes
        
        """
        fp1=full_prompt1+page
        suggestion = ollama.generate(model=model, prompt=fp1)
        response_dict = suggestion.model_dump()  # Convert to dictionary
        suggestion = markdown.markdown(response_dict.get("response", "")) 
        table_rows.append(f"""
            <tr>
                <td>{page}</td>
                <td>{err['issue_type']}</td>
                <td>{err['message']}</td>
                <td>{err['sentence']}</td>
                <td>{suggestion}</td>
            </tr>
        """)

    html_table = f"""
    <table border="1">
        <tr>
            <th>Page</th>
            <th>Issue Type</th>
            <th>Error</th>
            <th>Sentence</th>
            <th>Suggestion</th>
        </tr>
        {"".join(table_rows)}
    </table>
    """

    return html_table

def check_grammar(text_by_page):
    """
    Checks grammar and spelling using LanguageTool.
    
    Args:
        text_by_page (list): List of text extracted from each page of the PDF.
    
    Returns:
        tuple: Total grammar issues, total spelling issues, and error details.
    """
    tool = language_tool_python.LanguageTool('en-US')

    total_grammar_issues = 0
    total_spelling_issues = 0
    error_details = []

    for page_num, text in enumerate(text_by_page, start=1):
        matches = tool.check(text)

        for match in matches:
            issue_type = match.ruleId
            message = match.message
            error_details.append({
                "page": page_num,
                "issue_type": issue_type,
                "message": message,
                "sentence": match.sentence
            })

            if issue_type.startswith("TYPOS"):
                total_spelling_issues += 1
            else:
                total_grammar_issues += 1

    return total_grammar_issues, total_spelling_issues, error_details

def analyze_pdf(file_path):
    """
    Extracts text from a PDF and analyzes grammar issues.
    
    Args:
        file_path (str): Path to the PDF file.
    
    Returns:
        dict: Dictionary containing total grammar issues, total spelling issues, and error details.
    """
    try:
        with open(file_path, 'rb') as pdf_file:
            text_by_page = extract_text_from_pdf(pdf_file)
        
        if not text_by_page:
            raise ValueError("No text extracted from the PDF.")

        total_grammar_issues, total_spelling_issues, error_details = check_grammar(text_by_page)

        result = {
            "total_grammar_issues": total_grammar_issues,
            "total_spelling_issues": total_spelling_issues,
            "errors": error_details
        }
        
        return result

    except Exception as e:
        print(f"Error analyzing PDF: {e}", file=sys.stderr)
        return {
            "total_grammar_issues": 0,
            "total_spelling_issues": 0,
            "errors": []
        }

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.
    
    Args:
        pdf_file (file-like object): PDF file to extract text from.
    
    Returns:
        list: List of text extracted from each page.
    """
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text_by_page = [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
    return text_by_page

if __name__ == "__main__":
    file_path = "ref3_el.pdf"
    analysis_result = analyze_pdf(file_path)
    suggestions = aisug(analysis_result)
    print(suggestions)