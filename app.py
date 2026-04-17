import streamlit as st
import pandas as pd
import numpy as np
import time

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(
    page_title="Gait Insight Advanced",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("clinical_dashboard_15_subjects(2).csv")
df.columns = df.columns.str.strip()

subject_col = "subject"
condition_col = "condition"

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("Gait Insight Advanced")

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard Home",
        "Subject Compare",
        "Condition Explorer",
        "Live Monitoring",
        "AI Report"
    ]
)

st.sidebar.markdown("---")

# ---------------------------
# PAGE 1 HOME
# ---------------------------
if page == "Dashboard Home":

    st.title("Clinical Gait Analysis Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Records", len(df))
    c2.metric("Subjects", df[subject_col].nunique())
    c3.metric("Conditions", df[condition_col].nunique())
    c4.metric("Parameters", len(numeric_cols))

    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

    parameter = st.selectbox("Choose KPI Parameter", numeric_cols)

    st.subheader("Average by Subject")
    st.bar_chart(df.groupby(subject_col)[parameter].mean())

    st.subheader("Average by Condition")
    st.line_chart(df.groupby(condition_col)[parameter].mean())

# ---------------------------
# PAGE 2 SUBJECT COMPARE
# ---------------------------
elif page == "Subject Compare":

    st.title("15 Subject Comparison")

    subjects = sorted(df[subject_col].unique().tolist())

    col1, col2 = st.columns(2)

    with col1:
        s1 = st.selectbox("Select Subject 1", subjects)

    with col2:
        s2 = st.selectbox("Select Subject 2", subjects, index=1)

    parameter = st.selectbox("Select Parameter", numeric_cols)

    d1 = df[df[subject_col] == s1]
    d2 = df[df[subject_col] == s2]

    compare = pd.DataFrame({
        str(s1): d1[parameter].reset_index(drop=True),
        str(s2): d2[parameter].reset_index(drop=True)
    })

    st.subheader("Trend Comparison")
    st.line_chart(compare)

    st.subheader("Mean Comparison")
    means = pd.DataFrame({
        "Subject": [str(s1), str(s2)],
        "Mean": [d1[parameter].mean(), d2[parameter].mean()]
    }).set_index("Subject")

    st.bar_chart(means)

# ---------------------------
# PAGE 3 CONDITION EXPLORER
# ---------------------------
elif page == "Condition Explorer":

    st.title("Condition Analysis")

    parameter = st.selectbox("Choose Parameter", numeric_cols)

    st.subheader("Condition Means")
    st.bar_chart(df.groupby(condition_col)[parameter].mean())

    selected = st.selectbox(
        "Choose Condition",
        sorted(df[condition_col].unique().tolist())
    )

    temp = df[df[condition_col] == selected]

    st.subheader("Filtered Records")
    st.dataframe(temp, use_container_width=True)

    st.subheader("Subject Performance")
    st.line_chart(temp.groupby(subject_col)[parameter].mean())

# ---------------------------
# PAGE 4 LIVE MONITORING
# ---------------------------
elif page == "Live Monitoring":

    st.title("Live Gait Monitoring")

    parameter = st.selectbox("Choose Parameter", numeric_cols)

    chart = st.line_chart(
        pd.DataFrame(np.random.randn(20,1), columns=[parameter])
    )

    progress = st.progress(0)

    for i in range(100):
        new = pd.DataFrame(np.random.randn(1,1), columns=[parameter])
        chart.add_rows(new)
        progress.progress(i+1)
        time.sleep(0.03)

    st.success("Live stream completed")

# ---------------------------
# PAGE 5 AI REPORT
# ---------------------------
elif page == "AI Report":

    st.title("AI Clinical Report")

    parameter = st.selectbox("Choose Parameter", numeric_cols)

    c1, c2, c3 = st.columns(3)

    c1.metric("Average", round(df[parameter].mean(),2))
    c2.metric("Maximum", round(df[parameter].max(),2))
    c3.metric("Minimum", round(df[parameter].min(),2))

    best = df.groupby(subject_col)[parameter].mean().idxmax()
    low = df.groupby(subject_col)[parameter].mean().idxmin()

    st.subheader("Insights")

    st.success(f"Top performer for {parameter}: {best}")
    st.warning(f"Lowest performer for {parameter}: {low}")

    st.subheader("Correlation Heatmap Data")
    st.dataframe(df[numeric_cols].corr(), use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Full Dataset",
        csv,
        "gait_dataset.csv",
        "text/csv"
    )

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.write("Powered by Streamlit | Advanced Gait Insight")
