import streamlit as st
import pandas as pd
import numpy as np
import time

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="Gait Insight Advanced",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------
# LOAD DATA (CORRECT FILE NAME)
# ------------------------------------------------
df = pd.read_csv("clinical_dashboard_15_subjects.csv")
df.columns = df.columns.str.strip()

# Detect columns safely
subject_col = "subject"
condition_col = "condition"

# Numeric columns
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------
st.sidebar.title("Gait Insight Advanced")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home Dashboard",
        "Subject Comparison",
        "Condition Analysis",
        "Live Simulation",
        "AI Report"
    ]
)

# ------------------------------------------------
# PAGE 1 HOME
# ------------------------------------------------
if page == "Home Dashboard":

    st.title("Clinical Gait Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Records", len(df))
    c2.metric("Subjects", df[subject_col].nunique())
    c3.metric("Conditions", df[condition_col].nunique())
    c4.metric("Parameters", len(numeric_cols))

    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

    param = st.selectbox("Choose Parameter", numeric_cols)

    st.subheader("Average by Subject")
    st.bar_chart(df.groupby(subject_col)[param].mean())

# ------------------------------------------------
# PAGE 2 SUBJECT COMPARISON
# ------------------------------------------------
elif page == "Subject Comparison":

    st.title("Compare Subjects")

    subjects = sorted(df[subject_col].unique().tolist())

    col1, col2 = st.columns(2)

    with col1:
        s1 = st.selectbox("Select Subject 1", subjects)

    with col2:
        s2 = st.selectbox("Select Subject 2", subjects, index=1)

    param = st.selectbox("Select Parameter", numeric_cols)

    d1 = df[df[subject_col] == s1]
    d2 = df[df[subject_col] == s2]

    compare = pd.DataFrame({
        str(s1): d1[param].reset_index(drop=True),
        str(s2): d2[param].reset_index(drop=True)
    })

    st.subheader("Line Comparison")
    st.line_chart(compare)

    st.subheader("Statistics")

    stats = pd.DataFrame({
        "Metric": ["Mean", "Max", "Min"],
        str(s1): [
            d1[param].mean(),
            d1[param].max(),
            d1[param].min()
        ],
        str(s2): [
            d2[param].mean(),
            d2[param].max(),
            d2[param].min()
        ]
    })

    st.table(stats)

# ------------------------------------------------
# PAGE 3 CONDITION ANALYSIS
# ------------------------------------------------
elif page == "Condition Analysis":

    st.title("Condition Analysis")

    param = st.selectbox("Choose Parameter", numeric_cols)

    st.subheader("Average by Condition")
    st.bar_chart(df.groupby(condition_col)[param].mean())

    cond = st.selectbox(
        "Choose Condition",
        sorted(df[condition_col].unique().tolist())
    )

    temp = df[df[condition_col] == cond]

    st.subheader("Filtered Data")
    st.dataframe(temp, use_container_width=True)

# ------------------------------------------------
# PAGE 4 LIVE SIMULATION
# ------------------------------------------------
elif page == "Live Simulation":

    st.title("Live Gait Simulation")

    param = st.selectbox("Choose Parameter", numeric_cols)

    chart = st.line_chart(
        pd.DataFrame(np.random.randn(10,1), columns=[param])
    )

    progress = st.progress(0)

    for i in range(100):
        new = pd.DataFrame(np.random.randn(1,1), columns=[param])
        chart.add_rows(new)
        progress.progress(i+1)
        time.sleep(0.03)

    st.success("Simulation Completed")

# ------------------------------------------------
# PAGE 5 AI REPORT
# ------------------------------------------------
elif page == "AI Report":

    st.title("AI Insights Report")

    param = st.selectbox("Choose Parameter", numeric_cols)

    c1, c2, c3 = st.columns(3)

    c1.metric("Average", round(df[param].mean(),2))
    c2.metric("Maximum", round(df[param].max(),2))
    c3.metric("Minimum", round(df[param].min(),2))

    top = df.groupby(subject_col)[param].mean().idxmax()
    low = df.groupby(subject_col)[param].mean().idxmin()

    st.success(f"Top performer for {param}: {top}")
    st.warning(f"Lowest performer for {param}: {low}")

    st.subheader("Summary Statistics")
    st.dataframe(df.describe(), use_container_width=True)

# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.markdown("---")
st.write("Powered by Streamlit | Final Advanced Dashboard")
