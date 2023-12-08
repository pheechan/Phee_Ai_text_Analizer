import streamlit as st
import openai
#from transformers import GPT2LMHeadModel, GPT2Tokenizer
my_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

client = openai.OpenAI(api_key=my_api_key)
prompt1 = """Act as an AI writing analizer in English. You will receive a 
            piece of generated writing from Ai and you will rewrite and improve the writing and make the writing more human-like making it less-detectable that it was from ai.
            Say only the writing that you generated, don't say anything else.
        """ 
prompt2 = """Act as an AI writing analizer in German. You will use the writing from the previous step and translate it to German.
            Then you must find interesting vocabulary and 

        """

# pip install -r requirements.txt
# pip list


# Initialize the GPT-3 model
def initialize_model(my_api_key):
    #tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    #model = GPT2LMHeadModel.from_pretrained("gpt2")
    return tokenizer, model

# Function to analyze the text
def analyze_text(text):
    # This is a placeholder. In reality, you would need to implement
    # your own analysis based on your specific criteria.
    return text

# Function to rewrite the text
def rewrite_text(text, tokenizer, model):
    #inputs = tokenizer.encode(text, return_tensors='pt')
    #outputs = model.generate(inputs, max_length=100, num_return_sequences=1, no_repeat_ngram_size=2)
    #new_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text #new_text


# Set up the streamlit app
st.title('AI Text Analyzer and Rewriter')

user_input = st.text_input("Enter the text to analyze and rewrite:", "Your text here")

if my_api_key and user_input:
    tokenizer, model = initialize_model(my_api_key)
    analyzed_text = analyze_text(user_input)
    rewritten_text = rewrite_text(analyzed_text, tokenizer, model)
    
    st.write("Rewritten text:")
    st.write(rewritten_text)
    st.divider()
    show_original = st.toggle('Show original text')
    if show_original:  
        st.write("Original text:")
        st.write(user_input)
    st.divider()
    on = st.toggle('Translater')

    if on:
        option = st.selectbox(
        "What language would you like to translate to?",
        ("German", "Thai", "Spanish", "French"),
        
        index=None,
        placeholder="Select Language...",
        )

        st.write('You selected:', option)
        st.write('Translation will be here')