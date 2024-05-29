import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_groq import ChatGroq
import streamlit as st


# Function to configure sidebar to verify and get the model  api key
def configure_apikey_sidebar():
    groq_api_key = st.sidebar.text_input(f'Enter the API Key', type='password',
                                         help='Get Groq API Key from: https://console.groq.com/keys')
    if groq_api_key == '':
        st.sidebar.warning('Enter the API key')
        file_uploader = False
    elif groq_api_key.startswith('gsk_') and (len(groq_api_key) == 56):
        st.sidebar.success('Proceed to uploading the CSV file!', icon='️👉')
        file_uploader = True
    else:
        st.sidebar.warning('Please enter the correct credentials!', icon='⚠️')
        file_uploader = False

    return groq_api_key, file_uploader


def sidebar_groq_model_selection():
    st.sidebar.subheader("Model Selection")
    model = st.sidebar.selectbox('Select the Model', ('Llama3-8b-8192', 'Llama3-70b-8192', 'Mixtral-8x7b-32768',
                                                      'Gemma-7b-it'), label_visibility="collapsed")
    return model


def query_agent(data, query, model, groq_api_key):
    # Parse the CSV file and create a Pandas DataFrame from its contents.
    df = pd.read_csv(data)

    llm = ChatGroq(groq_api_key=groq_api_key, model_name=model)

    # Create a Pandas DataFrame agent.
    agent = create_pandas_dataframe_agent(llm, df, verbose=True)

    # Python REPL: A Python shell used to evaluating and executing Python commands.
    # It takes python code as input and outputs the result. The input python code can be generated from another tool in
    # the LangChain
    return agent.invoke(query)
