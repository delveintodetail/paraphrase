import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os

st.write(
    "Has environment variables been set:",
    os.environ["openai_api_key"] == st.secrets["password"],
)


openai_api_key = os.environ["openai_api_key"]

template = """
    Below is a paragraph that may be poorly written.
    Your goal is to:
    - rewrite the paragraph
    - correct it to a professional writing style
    - 如果输入是中文就用中文修改
    - if input is english, then rewrite it in english

    
    Below is the paragraph
    input: {input}

    YOUR rewritten RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["input"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="论文修改", page_icon=":robot:")
st.header("论文修改")




def get_text():
    input_text = st.text_area(label="填写待修改内容", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 1000:
    st.write("Please enter a shorter email. The maximum length is 1000 words.")
    st.stop()


st.markdown("### ChatGPT 修改结果:")

if email_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(input=email_input)
    print(prompt_with_email)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)