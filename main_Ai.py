# import streamlit as st
# import openai
# import pandas as pd
# import json

# prompt1 = """Act as an AI writing analizer in English. You will receive a 
#             piece of writing from Ai and you will rewrite and make the writing more human-like, making it less-detectable that it was from ai, two factors are crucial, “perplexity” and “burstiness.” Perplexity measures the complexity of text. Separately, burstiness compares the variations of sentences. Humans tend to write with greater burstiness, for example, with some longer or complex sentences alongside shorter ones. AI sentences tend to be more uniform. Therefore, when writing the following content I am going to ask you to create, it need it to have a good amount of perplexity and burstiness.
#             Say only the writing that you generated, don't say anything else and List the suggestions in a JSON array, one suggestion per line.
#             Each suggestion should have 3 fields:
#             - "before" - the text before the suggestion
#             - "after" - the text after the suggestion
#             - "comment" - a comment about the suggestion.
#         """ 
# prompt2 = """Act as an AI writing analizer in German, French, Spanish. You will use the writing from the previous step and translate it to German.
#             Then you must find interesting vocabulary and store them in a list.

#         """
# promt3 = """Act as an AI writing analizer in English. You will receive a piece of generated writing from Ai and you will rewrite and improve the writing and make the writing more human-like making it less-detectable that it was from ai.
#         """

# def init():
#     # Set up the streamlit app
#     st.set_page_config(
#         page_title='AI Text Analyzer and Rewriter',
#         page_icon= '🤖'
#     )

# def analyze_and_rewrite(api_key, user_input):
#     client = openai.OpenAI(api_key=api_key)
#     submit_messages = [
#         {"role": "system", "content": prompt1},
#         {'role': 'user', 'content': user_input},
#     ]
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=submit_messages
#     )
#     st.markdown('**AI response:**')
#     suggestion_answer = response.choices[0].message.content
#     st.markdown(suggestion_answer)
#     ans = json.loads(suggestion_answer)

#     # Convert to pandas DataFrame
#     answer_pandas = pd.DataFrame.from_dict(ans)
#     # answer_pandas = pd.DataFrame.from_dict([
#     #     {"content": suggestion_answer}
#     # ])
#     return answer_pandas

# def main():
#     init()
#     st.header('AI Text Analyzer and Rewriter 🤖')
#     st.markdown('Input the writing that you want to check.')

#     # Set up key
#     my_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

#     user_input = st.text_area("Enter the text to analyze and rewrite:", placeholder="Your text here...")
#     option = st.selectbox(
#    "Which language do you want to translate to?",
#    ("German", "French", "Spanish"),
#    index=None,
#    placeholder="Select language...",
#     )

#     st.write('You selected:', option)
#     if st.button('Submit') and my_api_key:
#         answer_pandas = analyze_and_rewrite(my_api_key, user_input)

#         print(answer_pandas)
#         st.table(answer_pandas)

# if __name__ == "__main__":
#     main()


### Our journey through the diverse culinary landscapes of Southeast Asia, the Mediterranean, and South America has only scratched the surface of the world's gastronomic wonders. From street food stalls to elegant dining establishments, the global tapestry of flavors invites us to explore, savor, and appreciate the unique stories each dish tells. So, let your taste buds be your guide as you embark on a culinary adventure, discovering the extraordinary in the everyday delights of food.



import streamlit as st
import openai
import json
import pandas as pd

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

client = openai.OpenAI(api_key=user_api_key)
prompt = """Act as an AI writing tutor in English. You will receive a 
            piece of writing and you should give suggestions on how to improve it.
            List the suggestions in a JSON array, one suggestion per line.
            Each suggestion should have 3 fields:
            - "before" - the text before the suggestion
            - "after" - the text after the suggestion
            - "category" - the category of the suggestion one of "grammar", "style", "word choice", "other"
            - "comment" - a comment about the suggestion
            Don't say anything at first. Wait for the user to say something.
        """    


st.title('Writing tutor')
st.markdown('Input the writing that you want to improve. \n\
            The AI will give you suggestions on how to improve it.')

user_input = st.text_area("Enter some text to correct:", "Your text here")


# submit button after text input
if st.button('Submit'):
    messages_so_far = [
        {"role": "system", "content": prompt},
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

    print (sd)
    suggestion_df = pd.DataFrame.from_dict(sd)
    print(suggestion_df)
    st.table(suggestion_df)