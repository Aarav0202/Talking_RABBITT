import streamlit as st
import pandas as pd
import plotly.express as px
import os
from openai import OpenAI

st.set_page_config(page_title="Talking Rabbitt", layout="wide")

st.title("🐰 Talking Rabbitt")
st.subheader("Talk to your business data")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
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
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
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