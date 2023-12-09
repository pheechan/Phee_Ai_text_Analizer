import streamlit as st
import openai
import pandas as pd
import json

prompt1 = """Act as an AI writing tutor in English. You will receive a 
            piece of writing and you should give suggestions on how to improve it.
            List the suggestions in a JSON array, one suggestion per line.
            Each suggestion should have 3 fields:
            - "before" - the text before the suggestion
            - "after" - the text after the suggestion
            - "category" - the category of the suggestion one of "grammar", "style", "word choice", "other"
            - "comment" - a comment about the suggestion
            Don't say anything at first. Wait for the user to say something.
        """

prompt2 = """Act as an AI writing analizer in English. You will receive a 
            piece of writing from Ai and you will rewrite and make the writing more human-like, making it less-detectable that it was from ai, two factors are crucial, “perplexity” and “burstiness.” Perplexity measures the complexity of text. Separately, burstiness compares the variations of sentences. Humans tend to write with greater burstiness, for example, with some longer or complex sentences alongside shorter ones. AI sentences tend to be more uniform. Therefore, when writing the following content I am going to ask you to create, it need it to have a good amount of perplexity and burstiness.
            Say only the writing that you generated, List the suggestions in a JSON array, one suggestion per line.
            Each suggestion should have 3 fields:
            - "before" - the text before the suggestion
            - "after" - the text after the suggestion
            - "category" - the category of the suggestion one of "grammar", "style", "word choice", "other"
            - "comment" - a comment about the suggestion
            Don't say anything at first. Wait for the user to say something.
        """ 
prompt3 = """Act as an AI writing translater, and translate text to {}.
            You must output 2 type of answer.
            1. You will translate the whole writing and output it as String 
            2. Then you must find interesting 10 vocabularies. Say only the writing that you generated, List the vocabulary in a JSON array, one vocabulary per line.
            Then you must seperated those two type of answer, so it won't be confusing like this example : 
            [ "Hello world", [
                {
                "vocabulary": "Hello",
                "Translation": "Hallo",
                "Example": "Hallo Ich bin John"
                }
            ]]
            Each vocabulary should have 3 fields:
            - "Vocabulary" - the text of the vocabulary
            - "Translation" - the translation of the vocabulary
            - "Example" - an example sentence of the vocabulary
            Don't say anything at first. Wait for the user to say something.
        """

prompt4 = """Act as an AI writing analizer in English. You will receive a piece of generated writing from Ai and you will rewrite and improve the writing and make the writing more human-like making it less-detectable that it was from ai.
        """

# ex formatted: 
# [ { "before": "Hello world here", "after": "Hello, everyone! I am here.",
#  "category": "style", 
# "comment": "Added a greeting and made the sentence more expressive." } ]

# [ "answer from traslate the sentence" ,[ { "before": "Hello world here", "after": "Hello, everyone! I am here.", "category": "style"} ] ]

def init():
    # Set up the streamlit app
    st.set_page_config(
        page_title='AI Text Analyzer and Rewriter',
        page_icon= '🤖'
    )

# def analyze_and_rewrite(api_key, user_input):
    

def main():
    init()
    st.header('AI Text Analyzer and Rewriter 🤖')
    st.markdown('Input the writing that you want to check.')

    # Set up key
    my_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

    user_input = st.text_area("Enter the text to analyze and rewrite:", placeholder="Your text here...")
    
    your_option = st.selectbox(
        "Which Function you want to do?",
        ('pnan', 'Rewriter', 'Translater', 'f4'),
        index=None,
        placeholder="Select Function...",
    )
    st.write('You selected:', your_option)

    #Function Selected
    if your_option == 'pnan': your_option = prompt1
    elif your_option == 'Rewriter': your_option = prompt2
    elif your_option == 'Translater': 
        lang_option = st.selectbox(
            "Which language do you want to translate to?",
            ("German", "French", "Spanish"),
            index=None,
            placeholder="Select language...",
        )
        st.write('You selected:', lang_option)
        # your_option = prompt3(lang_option)
        your_option = prompt3.format(lang_option)
    elif your_option == 'f4': your_option = prompt4
    
    
    
    client = openai.OpenAI(api_key=my_api_key)
    
    if st.button('Submit') and my_api_key:
        messages_so_far = [
            {"role": "system", "content": your_option},
            {'role': 'user', 'content': user_input},
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_so_far
        )
        # Show the response from the AI in a box
        st.markdown('**AI response:**')
        suggestion_answer = response.choices[0].message.content
        st.markdown(suggestion_answer)


        sd = json.loads(suggestion_answer)

        st.markdown("10 interesting vocabularies")
        print (sd)
        suggestion_df = pd.DataFrame.from_dict(sd)
        print(suggestion_df)
        st.table(suggestion_df)


if __name__ == "__main__":
    main()


### Our journey through the diverse culinary landscapes of Southeast Asia, the Mediterranean, and South America has only scratched the surface of the world's gastronomic wonders. From street food stalls to elegant dining establishments, the global tapestry of flavors invites us to explore, savor, and appreciate the unique stories each dish tells. So, let your taste buds be your guide as you embark on a culinary adventure, discovering the extraordinary in the everyday delights of food.
