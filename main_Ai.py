import streamlit as st
import openai
import pandas as pd
import json
from Prompts_text import prompt1, prompt2, prompt3, prompt4, prompt5, languages_key

def init():
    # Set up the streamlit app
    st.set_page_config(
        page_title='AI Text Analyzer 🤖',
        page_icon='📝',
        layout='wide'
    )
    st.title('AI Text Analyzer 🤖')

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
    check = False
    if your_option == 'pnan': your_option = prompt1
    elif your_option == 'Rewriter': your_option = prompt2
    elif your_option == 'Translator': 
        lang_sel = st.selectbox(
            "Which language do you want to translate to?",
            ("German", "French", "Spanish", "Italian", "Portuguese", "Japanese", "Chinese", "Russian", "Korean", "Arabic", "Hindi", "Turkish", "Thai"),
            index=None,
            placeholder="Select language...",
        )
        st.write('You selected:', lang_sel)
        # lang_option = languages_key[lang_sel]
        check = True
        your_option = prompt3.format(lang_sel)
    elif your_option == 'Auto-Corrector': your_option = prompt4
    elif your_option == 'Summarizer': your_option = prompt5
    
    openai.api_key = my_api_key
    
    if st.button('Submit') and my_api_key:
        messages_so_far = [
            {"role": "system", "content": your_option},
            {'role': 'user', 'content': user_input},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_so_far,
            #temperature = 
        )
        # Show the response from the AI in a box
        st.markdown('**AI response:**')
        suggestion_answer = response.choices[0].message.content
        #Debugging
        st.markdown("DEBUG answer:")
        st.markdown(suggestion_answer)
        
        st.markdown("--------------------------------")

        try:
            if suggestion_answer[0] != '[' or suggestion_answer[len(suggestion_answer)-1] != ']':
                st.markdown("Sorry, Please Submit again.")
            else : 
                sd = json.loads(suggestion_answer)
            
                if check or your_option == prompt2 or your_option == prompt5 or your_option == prompt4:
                    original_answer = sd[0]
                    st.markdown(original_answer)
                    if check and len(sd) > 1: st.markdown("Interesting Vocabulary Lists")
                    if len(sd) > 1: sd = sd[1]
                
                print (sd)
                suggestion_df = pd.DataFrame.from_dict(sd)
                print(suggestion_df)
                st.table(suggestion_df)
        except json.JSONDecodeError:
            st.markdown("Sorry, Please Submit again.")
        except IndexError:
            st.markdown("Sorry, Please Submit again.")

if __name__ == "__main__":
    main()