import  ollama

def get_topics(user,selected_model):
    ollama.generate(model=selected_model)