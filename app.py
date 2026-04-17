import streamlit as st
import pandas as pd

st.set_page_config(page_title="Advanced Gait Analysis Dashboard", layout="wide")

st.title("Advanced Gait Analysis Dashboard")

# Load files
df1 = pd.read_csv("Subject_ID 1.csv")
df2 = pd.read_csv("subject_ID 2.csv")

# Clean columns
df1.columns = df1.columns.astype(str).str.strip()
df2.columns = df2.columns.astype(str).str.strip()

# Convert duplicate-safe columns
df1 = df1.loc[:, ~df1.columns.duplicated()]
df2 = df2.loc[:, ~df2.columns.duplicated()]

# Show preview
col1, col2 = st.columns(2)

with col1:
    st.subheader("Subject 1")
    st.dataframe(df1.head())

with col2:
    st.subheader("Subject 2")
    st.dataframe(df2.head())

# Common columns
common_cols = [col for col in df1.columns if col in df2.columns]

# Numeric common columns only
numeric_cols = []

for col in common_cols:
    try:
        df1[col] = pd.to_numeric(df1[col], errors="coerce")
        df2[col] = pd.to_numeric(df2[col], errors="coerce")

        if df1[col].notna().sum() > 0 and df2[col].notna().sum() > 0:
            numeric_cols.append(col)
    except:
        pass

# If no columns
if not numeric_cols:
    st.error("No common numeric columns found.")
else:
    parameter = st.selectbox("Choose Parameter", numeric_cols)

    st.subheader("Comparison Graph")

    compare = pd.DataFrame({
        "Subject 1": df1[parameter].reset_index(drop=True),
        "Subject 2": df2[parameter].reset_index(drop=True)
    })

    st.line_chart(compare)

    st.subheader("Statistics")

    stats = pd.DataFrame({
        "Metric": ["Mean", "Max", "Min", "Std"],
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

# Footer
st.write("Dashboard Powered by Streamlit")
