import streamlit as st
import openai
import pandas as pd
import json

prompt1 = """Act as an AI writing analizer in English. You will receive a 
            piece of generated writing from Ai and you will rewrite and improve the writing and make the writing more human-like making it less-detectable that it was from ai.
            Say only the writing that you generated, don't say anything else.
        """ 
prompt2 = """Act as an AI writing analizer in German, French, Spanish. You will use the writing from the previous step and translate it to German.
            Then you must find interesting vocabulary and store them in a list.

        """


def init():
    # Set up the streamlit app
    st.set_page_config(
        page_title='AI Text Analyzer and Rewriter',
        page_icon= '🤖'
    )

def analyze_and_rewrite(api_key, user_input):
    client = openai.OpenAI(api_key=api_key)
    submit_messages = [
        {"role": "system", "content": prompt1},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=submit_messages
    )
    suggestion_answer = response.choices[0].message.content
    ans = json.loads(suggestion_answer)
    answer_pandas = pd.DataFrame.from_dict(ans)
    return answer_pandas


def main():
    init()
    st.header('AI Text Analyzer and Rewriter 🤖')
    st.markdown('Input the writing that you want to check.')

    # Set up key
    my_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

    user_input = st.text_area("Enter the text to analyze and rewrite:", "Your text here")

    if st.button('Submit') and my_api_key:
        answer_pandas = analyze_and_rewrite(my_api_key, user_input)

        st.markdown('**AI response:**')
        st.table(answer_pandas)

if __name__ == "__main__":
    main()


### Our journey through the diverse culinary landscapes of Southeast Asia, the Mediterranean, and South America has only scratched the surface of the world's gastronomic wonders. From street food stalls to elegant dining establishments, the global tapestry of flavors invites us to explore, savor, and appreciate the unique stories each dish tells. So, let your taste buds be your guide as you embark on a culinary adventure, discovering the extraordinary in the everyday delights of food.
