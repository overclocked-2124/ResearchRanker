from ollama import chat


def compare_methods(reference_text, user_text):
    # System prompt
    system_prompt = """
    You are a research methodology expert. Your task is to compare two research papers and analyze their methodologies.
    Focus on the following aspects:
    1. Problem Statement: Identify the problem both papers address.
    2. Methodology Comparison:
       - Efficiency: Compare computational/time complexity.
       - Innovation: Evaluate the novelty of the approaches.
       - Effectiveness: Analyze the results/accuracy.
    3. Conclusion: Determine if the user's method is better and explain why or why not.
    Be concise, clear, and objective in your analysis.
    """

    # User prompt
    user_prompt = f"""
    REFERENCE PAPER:
    {reference_text}

    USER'S PAPER:
    {user_text}

    Analyze and compare the methodologies of the two papers as per the instructions above.
    """

    # Generate the comparison using Ollama's chat function
    stream = chat(
        # model='llama3.3:70b-instruct-q3_K_M',
        model='llama3.2',  # using llama3.2 for testing will change to main model later.
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={
            "temperature": 0.3,  # Lowered temperature for factual and to reduce hallusinations.
        },
        stream=True,
    )

    # Collect and return the response
    response = ""
    for chunk in stream:
        response += chunk["message"]["content"]

    return response