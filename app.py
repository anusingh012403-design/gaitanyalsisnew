import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Advanced Gait Analysis Dashboard", layout="wide")

st.title("Advanced Gait Analysis Dashboard")
st.write("Compare, analyze and visualize multiple subject gait datasets")

# Load CSV files
df1 = pd.read_csv("Subject_ID 1.csv")
df2 = pd.read_csv("subject_ID 2.csv")

# Clean column names
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Sidebar
st.sidebar.header("Dashboard Controls")

# Show datasets
st.subheader("Dataset Preview")

col1, col2 = st.columns(2)

with col1:
    st.write("### Subject 1")
    st.dataframe(df1)

with col2:
    st.write("### Subject 2")
    st.dataframe(df2)

# Common numeric columns
common_cols = list(set(df1.columns).intersection(set(df2.columns)))

numeric_cols = []
for col in common_cols:
    try:
        df1[col] = pd.to_numeric(df1[col], errors='coerce')
        df2[col] = pd.to_numeric(df2[col], errors='coerce')
        numeric_cols.append(col)
    except:
        pass

# Parameter selection
parameter = st.sidebar.selectbox("Select Parameter", numeric_cols)

# Graph Section
st.subheader("Comparison Line Graph")

chart_df = pd.DataFrame({
    "Subject 1": df1[parameter],
    "Subject 2": df2[parameter]
})

st.line_chart(chart_df)

# Bar chart
st.subheader("Mean Comparison")

mean_df = pd.DataFrame({
    "Subjects": ["Subject 1", "Subject 2"],
    "Mean": [df1[parameter].mean(), df2[parameter].mean()]
})

st.bar_chart(mean_df.set_index("Subjects"))

# Statistics
st.subheader("Detailed Statistics")

stats = pd.DataFrame({
    "Metric": ["Mean", "Max", "Min", "Std Dev"],
    "Subject 1": [
        df1[parameter].mean(),
        df1[parameter].max(),
        df1[parameter].min(),
        df1[parameter].std()
    ],
    "Subject 2": [
        df2[parameter].mean(),
        df2[parameter].max(),
        df2[parameter].min(),
        df2[parameter].std()
    ]
})

st.table(stats)

# AI Insight
st.subheader("AI Insight")

if df1[parameter].mean() > df2[parameter].mean():
    st.success("Subject 1 has higher average value.")
elif df1[parameter].mean() < df2[parameter].mean():
    st.success("Subject 2 has higher average value.")
else:
    st.info("Both subjects have equal average values.")

# All columns
st.subheader("Available Parameters")

col3, col4 = st.columns(2)

with col3:
    st.write("Subject 1 Columns")
    st.write(df1.columns.tolist())

with col4:
    st.write("Subject 2 Columns")
    st.write(df2.columns.tolist())

# Footer
st.markdown("---")
st.write("Developed using Streamlit + GitHub")
