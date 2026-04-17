import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Clinical Gait Analysis Dashboard",
    layout="wide",
    page_icon="🧠"
)

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data():
    df = pd.read_csv("clinical_dashboard_15_subjects.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

# ==================================================
# COLUMN SETUP
# ==================================================
subject_col = "subject"
condition_col = "condition"

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

if subject_col in numeric_cols:
    numeric_cols.remove(subject_col)

# ==================================================
# SIDEBAR  (NO IMAGE HERE)
# ==================================================
st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Choose Page",
    [
        "🏠 Home Dashboard",
        "📊 Subject Comparison",
        "📈 Condition Analysis",
        "📡 Live Monitoring",
        "🤖 AI Report"
    ]
)

# ==================================================
# HOME PAGE
# ==================================================
if page == "🏠 Home Dashboard":

    st.title("Clinical Gait Analysis Dashboard")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Records", len(df))
    c2.metric("Subjects", df[subject_col].nunique())
    c3.metric("Conditions", df[condition_col].nunique())
    c4.metric("Parameters", len(numeric_cols))

    st.markdown("---")

    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

# ==================================================
# SUBJECT COMPARISON
# ==================================================
elif page == "📊 Subject Comparison":

    st.title("Subject Comparison")

    col1,col2 = st.columns(2)

    s1 = col1.selectbox("Select Subject 1", sorted(df[subject_col].unique()))
    s2 = col2.selectbox("Select Subject 2", sorted(df[subject_col].unique()))

    param = st.selectbox("Choose Parameter", numeric_cols)

    d1 = df[df[subject_col]==s1][param].mean()
    d2 = df[df[subject_col]==s2][param].mean()

    comp = pd.DataFrame({
        "Subject":[s1,s2],
        "Value":[d1,d2]
    })

    fig = px.bar(comp, x="Subject", y="Value", color="Subject")
    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# CONDITION ANALYSIS
# ==================================================
elif page == "📈 Condition Analysis":

    st.title("Condition Analysis")

    param = st.selectbox("Choose Parameter", numeric_cols)

    avg = df.groupby(condition_col)[param].mean().reset_index()

    fig = px.bar(avg, x=condition_col, y=param, color=condition_col)
    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# LIVE MONITORING
# ==================================================
elif page == "📡 Live Monitoring":

    st.title("Live Monitoring")

    subject = st.selectbox("Select Subject", sorted(df[subject_col].unique()))
    param = st.selectbox("Choose Parameter", numeric_cols)

    temp = df[df[subject_col]==subject]

    fig = px.line(temp, y=param, markers=True)
    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# AI REPORT
# ==================================================
elif page == "🤖 AI Report":

    st.title("AI Insights Report")

    subject = st.selectbox("Select Subject", sorted(df[subject_col].unique()))

    sub = df[df[subject_col]==subject]

    st.dataframe(sub, use_container_width=True)

    report = sub.to_csv(index=False)

    st.download_button(
        "Download Report",
        report,
        file_name=f"Subject_{subject}_Report.csv",
        mime="text/csv"
    )
