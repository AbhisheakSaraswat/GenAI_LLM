import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from langchain_groq.chat_models import ChatGroq
import os

# Initialize the language model
llm = ChatGroq(model_name = "llama3-70b-8192", 
               api_key="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")

# Load Data
df = pd.read_excel("superstore.xls")
smart_df = SmartDataframe(df, config = {"llm" : llm})

# print(smart_df.chat("How many rows and columns in the data set?"))

# Initialize session state for question history
if 'question_history' not in st.session_state:
    st.session_state.question_history = []

# Streamlit interface
st.title("Exploring Conversations with Data using LLM")

# Display data
st.sidebar.header("Options")
show_data = st.sidebar.checkbox("show raw data")
if show_data:
    st.subheader("Superstore Data")
    st.dataframe(df.head(20))

user_question = st.text_input("Ask a question about the data.")

# Display the response to the user's question
if st.button("Get Answer"):
    answer = smart_df.chat(user_question)
    st.write(answer)
    st.session_state.question_history.append(user_question)
    image_path = r"exports/charts/temp_chart.png"

    if os.path.exists(image_path):
        st.image(image_path, caption = "Sample Chart", use_column_width=True)
        os.remove(image_path)

# Display the history of questions
st.subheader("Question History")
for i, question in enumerate(st.session_state.question_history,1):
    st.write(f"{i}. {question}")        




