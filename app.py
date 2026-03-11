import streamlit as st
import pandas as pd
import plotly.express as px
import os
from openai import OpenAI

st.set_page_config(page_title="Talking Rabbitt", layout="wide")

st.title("🐰 Talking Rabbitt")
st.subheader("Talk to your business data")

api_key = st.secrets.get("OPENROUTER_API_KEY")

if not api_key:
    st.error("API key not found. Please add OPENROUTER_API_KEY in Streamlit Secrets.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)
uploaded_file = st.file_uploader("Upload your sales CSV", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.write("### Data Preview")
    st.dataframe(df.head())

    question = st.text_input("Ask a question about your data")

    if question:

        prompt = f"""
You are a business data analyst.

Dataset columns:
{df.columns.tolist()}

Sample data:
{df.head(5).to_string()}

User Question:
{question}

Give a short, clear answer.
"""

        response = client.chat.completions.create(
    model="meta-llama/llama-3-8b-instruct",
    messages=[{"role": "user", "content": prompt}],
    extra_headers={
        "HTTP-Referer": "https://streamlit.io",
        "X-Title": "Talking Rabbitt"
    }
)

        answer = response.choices[0].message.content

        st.write("### Insight")
        st.write(answer)

    st.write("### Quick Visualization")

    x_col = st.selectbox("X Axis", df.columns)
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:
        y_col = st.selectbox("Y Axis", numeric_cols)

        fig = px.bar(df, x=x_col, y=y_col)
        st.plotly_chart(fig)
