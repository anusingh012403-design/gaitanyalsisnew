import streamlit as st
import pandas as pd

st.title("Gait Analysis Dashboard")

# Read CSV file
df = pd.read_csv("Subject_ID 1.csv")

# Show dataset
st.subheader("Dataset Preview")
st.write(df)

# Show column names
st.subheader("Parameters / Columns")
st.write(df.columns)

# Select column for chart
column = st.selectbox("Choose Parameter", df.columns)

st.subheader("Graph")
st.line_chart(df[column])
