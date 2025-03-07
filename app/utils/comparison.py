import ollama
from ollama import chat

def comparePDF(reference,user,selected_model):
    generated_text =ollama.generate(model=selected_model,
    system="""
    You are a research methodology expert. Your task is to compare two research papers and analyze their methodologies.
    Focus on the following aspects:
    1. Problem Statement: Identify the problem both papers address.
    2. Methodology Comparison:
       - Efficiency: Compare computational/time complexity.
       - Innovation: Evaluate the novelty of the approaches.
       - Effectiveness: Analyze the results/accuracy.
    3. Conclusion: Determine if the user's method is better and explain why or why not.
    4.Do not give any introductory statement or anything extra at the end.Only the analysis.
    Be concise, clear, and objective in your analysis.
    """,
    prompt=f"""
    REFERENCE PAPER:
    {reference}

    USER'S PAPER:
    {user}

    Analyze and compare the methodologies of the two papers as per the instructions above.
    """,stream=False)['response']

    return generated_text

def compareTemplate(template,user,selected_model):
    generated_text=ollama.generate(model=selected_model,
    system="""## PDF Structure Assessment System Prompt

    **Objective:** Analyze and compare structural elements between two PDF documents (template vs user-submitted) to generate a 1-10 alignment rating based solely on formatting and document structure.

    **Structural Elements to Evaluate:**
    - Section hierarchy and nesting levels
    - Heading styles (font, size, hierarchy)
    - Paragraph formatting (indentation, spacing, alignment)
    - Page layout (margins, columns, orientation)
    - Use of tables/figures placement logic
    - Header/footer structure and positioning
    - Bullet/numbered list formatting
    - Page numbering system
    - Overall document flow and visual rhythm
    
    **Processing Steps:**
    1. **Feature Extraction**  
       - Parse both PDFs using PyPDF's structure analysis
       - Create structural fingerprints showing element positions and styles
       - Generate normalized page templates for comparison
    
    2. **Comparative Analysis**  
       - Calculate alignment percentages for:
         - Section hierarchy match (%)
         - Formatting consistency (%)
         - Page layout similarity (%)
         - Visual element positioning (%)
    
    3. **Scoring Algorithm**  
       `Final Score = (Hierarchy × 0.4) + (Formatting × 0.3) + (Layout × 0.2) + (Elements × 0.1)`
    
    **Output Format:**
    - Numerical rating (1-10 scale)
    - Structural alignment percentage
    - Top 3 formatting discrepancies
    - Top 3 successful alignments
    - Confidence score (0-100%)
    
    **Example Output:**
    `Rating: 7.8/10  
    Alignment: 78% structural match  
    Discrepancies: 1) Heading hierarchy mismatch (3 levels vs 4) 2) Margin variance (±12%) 3) Table positioning deviation  
    Matches: 1) Page numbering 2) Paragraph spacing 3) Footer content positioning  
    Confidence: 92%`
    
    **System Constraints:**
    - Temperature: 0.3 (strict analytical mode)
    - Max token count: 4096
    - Prioritize positional data over semantic content
    - Disregard text content meaning entirely of the user pdf but the template pdf has hints for 
      what the block/paragraph should contain so use that to asses if the user pdf has the required content at the best place.
        """,
    prompt=f"""
    [STRUCTURAL ANALYSIS REQUEST]
    Compare formatting and document structure between:
    - Template PDF: {template}
    - User PDF: {user}
    
    Analyze only these non-content aspects:
    1. Visual hierarchy and element positioning
    2. Style consistency across sections
    3. Page layout characteristics
    4. Document object relationships
    
    Return assessment using the exact format:
    Rating: [X]/10  
    Alignment: [Y]%  
    Discrepancies: 1)... 2)... 3)...  
    Matches: 1)... 2)... 3)...  
    Confidence: [Z]%
    """
    #,options={
        #"temperature": 0.3,
        #"top_p": 0.9,
        #"stop": ["Rating:"]
        #}
    ,stream=False)['response']
    return generated_text