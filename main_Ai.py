import streamlit as st
import openai
import pandas as pd
import json
from langchain.chat_models import GPTAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# from streamlit_chat import Message

# pip install streamlit-chat
prompt1 = """Act as an AI writing analizer in English. You will receive a 
            piece of generated writing from Ai and you will rewrite and improve the writing and make the writing more human-like making it less-detectable that it was from ai.
            Say only the writing that you generated, don't say anything else.
        """ 
prompt2 = """Act as an AI writing analizer in German, French, Spanish. You will use the writing from the previous step and translate it to German.
            Then you must find interesting vocabulary and store them in a list.

        """
#pip install langchain openai


def main():
    # Set up the streamlit app
    st.set_page_config(
        page_title='AI Text Analyzer and Rewriter',
        page_icon= '🤖'
    )

    # Message("Hello World")
    # Message("Hello World eiei", is_user = True)

    # Set up key
    my_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    
    client = openai.OpenAI(api_key=my_api_key)
    
    user_input = st.text_area("Enter the text to analyze and rewrite:", "Your text here")
    

    if st.button('Submit'):
        Submit_messages = [
            {"role": "system", "content": prompt1},
            {'role': 'user', 'content': user_input},
        ]
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = Submit_messages
        )

        st.markdown('**AI response:**')
        suggestion_answer = response.choices[0].message.content

        ans = json.loads(suggestion_answer)

        print (ans)
        answer_pandas = pd.DataFrame.from_dict(ans)
        print(answer_pandas)
        st.table(answer_pandas)


# if my_api_key and user_input:
#     tokenizer, model = initialize_model(my_api_key)
#     analyzed_text = analyze_text(user_input)
#     rewritten_text = rewrite_text(analyzed_text, tokenizer, model)
    
#     st.write("Rewritten text:")
#     st.write(rewritten_text)
#     st.divider()
#     show_original = st.toggle('Show original text')
#     if show_original:  
#         st.write("Original text:")
#         st.write(user_input)
#     st.divider()
#     on = st.toggle('Translater')

#     if on:
#         option = st.selectbox(
#         "What language would you like to translate to?",
#         ("German", "Spanish", "French"),
        
#         index=None,
#         placeholder="Select Language...",
#         )

#         st.write('You selected:', option)
#         st.write('Translation will be here')