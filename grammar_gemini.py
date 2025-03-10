#AIzaSyDOG6wWK8NmAlCSW2LmEIO-m6v398vk-M0
import ollama
import markdown
import PyPDF2
import language_tool_python
import nltk
import google.generativeai as genai
import sys

# Ensure NLTK is ready
nltk.download('punkt')

# Configure Gemini API
genai.configure(api_key="AIzaSyBMI69pJZaO9Pugy6oaaK3pmLJz43DtzAg")
model = genai.GenerativeModel("gemini-1.5-pro")


def analyze_pdf(file_path):
    """Extracts text from a PDF and checks grammar."""
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
        print(f"❌ Error analyzing PDF: {e}", file=sys.stderr)
        return {
            "total_grammar_issues": 0,
            "total_spelling_issues": 0,
            "errors": []
        }


def check_grammar(text_by_page):
    """Checks grammar and spelling using LanguageTool."""
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


def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text_by_page = [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
    return text_by_page


def aisugGemini(pdf_res):
    """Generates AI suggestions using Gemini model."""
    error_text = "\n".join(
        f"Page {err['page']}: {err['issue_type']} - {err['message']} (Sentence: {err['sentence']})"
        for err in pdf_res.get("errors", [])
    )

    system_prompt = """
    You are a highly skilled grammar expert specializing in analyzing and 
    correcting text based on grammar-checking libraries such as NLTK, spaCy, 
    and Grammarly. When given a user-provided text along with identified grammar mistakes,
    provide clear, precise suggestions for correction. Explain why the changes are necessary while maintaining
    the original intent and style of the text. Ensure your responses are concise, structured, 
    and easy to understand. Where applicable, suggest alternative phrasings for improved clarity and fluency.
    """
    full_prompt = system_prompt + error_text

    # Debug: Print prompt sent to AI
    print("\n🔹 Sending Prompt to AI:\n", full_prompt[:500])  # Print first 500 characters

    try:
        response = model.generate_content(full_prompt)
        
        # Debug: Print AI response
        print("\n🔹 Raw AI Response:\n", response)

        if response and hasattr(response, "text"):
            markdown_response = markdown.markdown(response.text)
            return markdown_response
        else:
            print("❌ No response text received.")
            return "AI did not return a valid response."

    except Exception as e:
        print(f"❌ Error with AI request: {e}")
        return "AI request failed."


if __name__ == "__main__":
    file_path = "ref3_el.pdf"

    print("\n🔹 Starting PDF Analysis...\n")
    analysis_result = analyze_pdf(file_path)

    print("\n✅ PDF Analysis Completed.")
    print(f"Total Grammar Issues: {analysis_result['total_grammar_issues']}")
    print(f"Total Spelling Issues: {analysis_result['total_spelling_issues']}")

    print("\n🔹 Sending Grammar Issues to AI for Suggestions...\n")
    suggestions = aisugGemini(analysis_result)

    print("\n✅ AI Suggestions:\n", suggestions)
