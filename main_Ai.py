import streamlit as st
import openai
import pandas as pd
import json
# from openai import OpenAI

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
            piece of writing and you should make the writing more human-like, making it less-detectable that it was from ai, two factors are crucial, “perplexity” and “burstiness.” Perplexity measures the complexity of text. Separately, burstiness compares the variations of sentences. Humans tend to write with greater burstiness, for example, with some longer or complex sentences alongside shorter ones. AI sentences tend to be more uniform. Therefore, when writing the following content I am going to ask you to create, it need it to have a good amount of perplexity and burstiness.
            You must output 2 type of answer.
            1. You will rewrite the whole writing and output it as String
            2. Then you must give suggestions on how to improve it. Say only the writing that you generated, List the suggestions in a JSON array, one suggestion per line.
            Then you must seperated those two type of answer, so it won't be confusing like this example : 
            [ "the rewrite string", [Json Array]]
            ex formatted: 
            [ { "before": "Hello world here", "after": "Hello, everyone! I am here.",
                "category": "style", 
                 "comment": "Added a greeting and made the sentence more expressive." } ]
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
            [ "the translate string", [Json Array]]
            Each vocabulary should have 3 fields:
            - "Vocabulary" - the text of the vocabulary in the language you just translate to.
            - "Part of Speech" - the part of speech of the vocabulary
            - "Translation" - the translation of the vocabulary
            - "Example" - an example sentence of the vocabulary in the language you just translate to.
            Don't say anything at first. Wait for the user to say something.
        """

prompt4 = """Act as an AI auto-corrector. You will receive a piece of writing and you should correct any spelling or grammatical errors.
            The corrections should be accurate and not change the original meaning.
            For example, if the original text is 'Hllo wold her', a possible correction might be 'Hello world here'.
            You must output 2 types of answers.
            1. You will correct the whole writing and output it as a String.
            2. Then you must list the words you corrected. List the corrected words in a JSON array, one word per line.
            Then you must separate those two types of answers, so it won't be confusing like this example : 
            [ "the corrected string", [Json Array]]
            example of how you format the JSON array:
            [
            {
                "Incorrect": "Hllo",
                "Correct": "Hello",
                "Context": "Hllo wold her",
                "Type": "Spelling"
            },
            {
                "Incorrect": "wold",
                "Correct": "world",
                "Context": "Hllo wold her",
                "Type": "Spelling"
            },
            {
                "Incorrect": "her",
                "Correct": "here",
                "Context": "Hllo wold her",
                "Type": "Spelling"
            },
            {
                "Incorrect": "I goes",
                "Correct": "I go",
                "Context": "I goes to the park every day",
                "Type": "Grammar"
            },
            {
                "Incorrect": "Its raining",
                "Correct": "It's raining",
                "Context": "Its raining outside",
                "Type": "Punctuation"
            },
            {
                "Incorrect": "teh",
                "Correct": "the",
                "Context": "I love teh smell of rain",
                "Type": "Typo"
            }
            ]
            Each corrected word should have 3 fields:
            - "Incorrect" - the incorrect word before correction
            - "Correct" - the corrected word
            - "Context" - a sentence showing the word in context
            - "Type" - the type of error, one of "Spelling", "Grammar", "Punctuation", "Typo", "Other"
            Don't say anything at first. Wait for the user to say something.
        """
prompt5 = """Act as an AI summarizer. You will receive a piece of writing and you should summarize it while maintaining the key points.
            The summary should be concise and to the point.
            For example, if the original text is 'Our journey through the diverse culinary landscapes of Southeast Asia, the Mediterranean, and South America has only scratched the surface of the world's gastronomic wonders. From street food stalls to elegant dining establishments, the global tapestry of flavors invites us to explore, savor, and appreciate the unique stories each dish tells. So, let your taste buds be your guide as you embark on a culinary adventure, discovering the extraordinary in the everyday delights of food.', 
            a possible summary might be 'The world offers a wide range of culinary experiences, from Southeast Asia to South America, each telling a unique story through its flavors. Exploring these diverse gastronomic landscapes can lead to extraordinary discoveries.'
            You must output 2 types of answers.
            1. You will summarize the whole writing and output it as a String.
            2. Then you must list the key points you identified in the original text. List these key points in a JSON array, one point per line.
            Then you must separate those two types of answers, so it won't be confusing like this example : 
            [ "the summarized string", [Json Array]]
            example of how you format the JSON array:
            [
            {
                "KeyPoint": "The importance of AI in today's world",
                "Context": "In the original text, the author discussed how AI is becoming increasingly important in various industries, from healthcare to finance."
            },
            {
                "KeyPoint": "The challenges of implementing AI",
                "Context": "The author also highlighted several challenges that companies may face when implementing AI, such as data privacy concerns and the need for skilled workers."
            }
            ]
            Each key point should have 2 fields:
            - "KeyPoint" - the key point identified in the original text
            - "Context" - a sentence or paragraph from the original text that illustrates the key point
            Don't say anything at first. Wait for the user to say something.
        """
# ex formatted: 
# [ { "before": "Hello world here", "after": "Hello, everyone! I am here.",
#  "category": "style", 
# "comment": "Added a greeting and made the sentence more expressive." } ]

def init():
    # Set up the streamlit app
    st.set_page_config(
        page_title='AI Text Analyzer 🤖',
        page_icon='📝',
        layout='wide'
    )
    st.title('AI Text Analyzer 🤖')

# def analyze_and_rewrite(api_key, user_input):

# pip install --upgrade openai

def main():
    init()
    st.markdown('Input the writing that you want to check.')

    # Set up key
    my_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

    user_input = st.text_area("Enter the text to analyze:", placeholder="Your text here...")
    
    your_option = st.selectbox(
        "Which Function you want to do?",
        ('pnan', 'Rewriter', 'Translator', 'Auto-Corrector', 'Summarizer'),
        index=None,
        placeholder="Select Function...",
    )
    st.write('You selected:', your_option)

    #Function Selected
    if your_option == 'pnan': your_option = prompt1
    elif your_option == 'Rewriter': your_option = prompt2
    elif your_option == 'Translator': 
        lang_option = st.selectbox(
            "Which language do you want to translate to?",
            ("German", "French", "Spanish", "Italian", "Portuguese", "Japanese", "Chinese", "Russian", "Korean", "Arabic", "Hindi", "Turkish", "Thai"),
            index=None,
            placeholder="Select language...",
        )
        st.write('You selected:', lang_option)
        your_option = prompt3.format(lang_option)
    elif your_option == 'Auto-Corrector': your_option = prompt4
    elif your_option == 'Summarizer': your_option = prompt5
    
    
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
        st.markdown("DEBUG answer:")
        st.markdown(suggestion_answer)
        st.markdown("--------------------------------")

        
        if your_option == 'Translater':
            st.markdown(sd[0])
            st.markdown("10 interesting vocabularies")
            sd = sd[1]
        
        sd = json.loads(sd)
        print (sd)
        suggestion_df = pd.DataFrame.from_dict(sd)
        print(suggestion_df)
        st.table(suggestion_df)


if __name__ == "__main__":
    main()


### Our journey through the diverse culinary landscapes of Southeast Asia, the Mediterranean, and South America has only scratched the surface of the world's gastronomic wonders. From street food stalls to elegant dining establishments, the global tapestry of flavors invites us to explore, savor, and appreciate the unique stories each dish tells. So, let your taste buds be your guide as you embark on a culinary adventure, discovering the extraordinary in the everyday delights of food.
