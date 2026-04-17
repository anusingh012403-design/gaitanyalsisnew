import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gait Analysis Dashboard", layout="wide")

st.title("Gait Analysis Dashboard")
st.write("Compare two subjects gait data")

# Load CSV files
df1 = pd.read_csv("Subject_ID 1.csv")
df2 = pd.read_csv("subject_ID 2.csv")

# Show previews
col1, col2 = st.columns(2)

with col1:
    st.subheader("Subject 1 Data")
    st.write(df1.head())

with col2:
    st.subheader("Subject 2 Data")
    st.write(df2.head())

# Common columns
columns = df1.columns

# Select parameter
parameter = st.selectbox("Choose Parameter to Compare", columns)

# Compare Graph
st.subheader("Comparison Graph")

compare_df = pd.DataFrame({
    "Subject 1": df1[parameter],
    "Subject 2": df2[parameter]
})

st.line_chart(compare_df)

# Statistics
st.subheader("Statistics")

stats = pd.DataFrame({
    "Subject 1 Mean": [df1[parameter].mean()],
    "Subject 2 Mean": [df2[parameter].mean()],
    "Subject 1 Max": [df1[parameter].max()],
    "Subject 2 Max": [df2[parameter].max()]
})

st.write(stats)
