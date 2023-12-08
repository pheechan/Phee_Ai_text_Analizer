import streamlit as st
import openai
import pandas as pd
import json
from langchain import Translator 

prompt1 = """
Act as an AI writing analyzer in English. You will receive a 
piece of generated writing from Ai and you will rewrite and improve the writing and make the writing more human-like making it less-detectable that it was from AI.
Say only the writing that you generated, don't say anything else.
""" 
prompt2 = """
Act as an AI writing analyzer in German, French, Spanish. You will use the writing from the previous step and translate it to German.
Then you must find interesting vocabulary and store them in a list.
"""

# pip install -r requirements.txt


def init():
    # Set up the streamlit app
    st.set_page_config(
        page_title='AI Text Analyzer and Rewriter',
        page_icon='🤖'
    )

def main():
    init()

    st.header('AI Text Analyzer and Rewriter 🤖')
    st.markdown('Input the writing that you want to check.')

    # Set up key
    my_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    client = openai.OpenAI(api_key=my_api_key)
    
    user_input = st.text_area("Enter the text to analyze and rewrite:", "Your text here")

    if st.button('Submit'):
        Submit_messages = [
            {"role": "system", "content": prompt1},
            {'role': 'user', 'content': user_input},
        ]

        # Analyze and rewrite using OpenAI
        response = client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=Submit_messages
        )

        generated_text = response['choices'][0]['message']['content']

        # Translate to German using langchain
        translator = Translator(from_lang='en', to_lang='de')
        translated_text = translator.translate(generated_text)

        st.subheader("Generated and Translated Text:")
        st.write("Original (English):", generated_text)
        st.write("Translated (German):", translated_text)

        # Extract interesting vocabulary (you may need to customize this part)
        interesting_vocabulary = extract_interesting_vocabulary(translated_text)
        st.subheader("Interesting Vocabulary:")
        st.write(interesting_vocabulary)

def extract_interesting_vocabulary(text):
    # You can customize this function based on your criteria for interesting vocabulary
    # For example, you can use NLP libraries like spaCy or NLTK to extract keywords
    # Here, we are simply splitting the text into words
    words = text.split()
    return list(set(words))

if __name__ == "__main__":
    main()
