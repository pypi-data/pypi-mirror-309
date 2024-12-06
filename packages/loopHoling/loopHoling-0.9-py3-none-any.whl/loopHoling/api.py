import google.generativeai as genai

def give(prompt):
     # Configure the API key
    api_key = "AIzaSyAV0pHOO0FbEiM_lBBrMJ6qm4RxHmRMEnY"
    genai.configure(api_key=api_key)

    # Create a model
    model = genai.GenerativeModel("gemini-1.5-flash")
    preprompt = "give python code "
    # Generate content with optional preprompt
    if preprompt:
        full_prompt = f"{preprompt}\n{prompt}"
    else:
        full_prompt = prompt

    response = model.generate_content(full_prompt)
    return response.text