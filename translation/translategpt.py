import openai

# Set your OpenAI API key
openai.api_key = "yourAPIkey"

def translate(text, language):
    """
    Translate the given text to specified language using ChatGPT.
    
    Args:
        text (str): The text to be translated.
        language (str): 
    
    Returns:
        str: Translated text in specified language.
    """
    try:
        # Use ChatGPT to translate the text
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Ensure you use a model that supports translation
            messages=[
                {"role": "system", "content": "You are a helpful translator."},
                {"role": "user", "content": f"Translate the following text into {language} and provide only the translation, without any additional comments or explanations: {text}"}
            ]
        )
        # Extract the translated text
        translation = response['choices'][0]['message']['content'].strip()
        return translation
    except Exception as e:
        return f"Error: {str(e)}"
