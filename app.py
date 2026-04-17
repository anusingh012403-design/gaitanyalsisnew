# ==============================
# ADVANCED 5 PAGE GAIT DASHBOARD
# Replace full app.py with this
# ==============================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Advanced Clinical Gait Dashboard",
    layout="wide",
    page_icon="🧠"
)

# --------------------------------
# STYLE
# --------------------------------
st.markdown("""
<style>
.main {
    background-color:#f7fafc;
}
h1,h2,h3 {
    color:#0f172a;
}
[data-testid="metric-container"] {
    background: white;
    border:1px solid #e2e8f0;
    padding:15px;
    border-radius:14px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# LOAD DATA
# --------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("clinical_dashboard_15_subjects.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

subject_col = "subject"
condition_col = "condition"

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

if subject_col in numeric_cols:
    numeric_cols.remove(subject_col)

# --------------------------------
# SIDEBAR
# --------------------------------
st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "🏠 Home Dashboard",
        "📊 Subject Comparison",
        "📡 Live Monitoring",
        "📄 Clinical Report",
        "📁 Full Dataset Insights"
    ]
)

# ======================================================
# PAGE 1 HOME DASHBOARD
# ======================================================
if page == "🏠 Home Dashboard":

    st.title("🧠 Advanced Clinical Gait Dashboard")
    st.markdown("### Multi Subject Motion Analysis System")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Records", len(df))
    c2.metric("Subjects", df[subject_col].nunique())
    c3.metric("Conditions", df[condition_col].nunique())
    c4.metric("Parameters", len(numeric_cols))

    st.markdown("---")

    col1,col2 = st.columns(2)

    with col1:
        speed = df.groupby(subject_col)["walking_speed"].mean().reset_index()

        fig = px.bar(
            speed,
            x=subject_col,
            y="walking_speed",
            color="walking_speed",
            title="Average Walking Speed",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(
            df,
            names=condition_col,
            title="Condition Distribution",
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

# ======================================================
# PAGE 2 SUBJECT COMPARISON
# ======================================================
elif page == "📊 Subject Comparison":

    st.title("📊 Subject Comparison Dashboard")

    c1,c2 = st.columns(2)

    s1 = c1.selectbox("Select Subject 1", sorted(df[subject_col].unique()))
    s2 = c2.selectbox("Select Subject 2", sorted(df[subject_col].unique()), index=1)

    param = st.selectbox("Choose Parameter", numeric_cols)

    v1 = df[df[subject_col]==s1][param].mean()
    v2 = df[df[subject_col]==s2][param].mean()

    compare = pd.DataFrame({
        "Subject":[s1,s2],
        "Value":[v1,v2]
    })

    col1,col2 = st.columns(2)

    with col1:
        fig = px.bar(
            compare,
            x="Subject",
            y="Value",
            color="Subject",
            text="Value",
            title="Bar Comparison",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(
            compare,
            names="Subject",
            values="Value",
            title="Pie Comparison",
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Radar Comparison")

    radar_params = numeric_cols[:6]

    r1 = [df[df[subject_col]==s1][p].mean() for p in radar_params]
    r2 = [df[df[subject_col]==s2][p].mean() for p in radar_params]

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(
        r=r1,
        theta=radar_params,
        fill='toself',
        name=f"Subject {s1}"
    ))

    radar.add_trace(go.Scatterpolar(
        r=r2,
        theta=radar_params,
        fill='toself',
        name=f"Subject {s2}"
    ))

    radar.update_layout(template="plotly_white")

    st.plotly_chart(radar, use_container_width=True)

# ======================================================
# PAGE 3 LIVE MONITORING
# ======================================================
elif page == "📡 Live Monitoring":

    st.title("📡 Live Monitoring")

    subject = st.selectbox("Select Subject", sorted(df[subject_col].unique()))
    param = st.selectbox("Select Parameter", numeric_cols)

    vals = df[df[subject_col]==subject][param].values

    chart = st.empty()

    for i in range(len(vals)):
        temp = pd.DataFrame({
            "Time": np.arange(i+1),
            "Value": vals[:i+1]
        })

        fig = px.line(
            temp,
            x="Time",
            y="Value",
            markers=True,
            title=f"Live {param}",
            template="plotly_white"
        )

        chart.plotly_chart(fig, use_container_width=True)
        time.sleep(0.5)

# ======================================================
# PAGE 4 CLINICAL REPORT
# ======================================================
elif page == "📄 Clinical Report":

    st.title("📄 Subject Clinical Report")

    subject = st.selectbox("Choose Subject", sorted(df[subject_col].unique()))

    sub = df[df[subject_col]==subject]

    c1,c2,c3 = st.columns(3)

    c1.metric("Avg Speed", round(sub["walking_speed"].mean(),2))
    c2.metric("Avg Cadence", round(sub["cadence"].mean(),2))
    c3.metric("Avg Stride", round(sub["stride_length"].mean(),2))

    st.markdown("---")

    report_df = sub[numeric_cols].mean().reset_index()
    report_df.columns = ["Parameter","Value"]

    fig = px.bar(
        report_df,
        x="Parameter",
        y="Value",
        color="Value",
        title=f"Subject {subject} Report",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(sub, use_container_width=True)

    csv = sub.to_csv(index=False)

    st.download_button(
        "📥 Download Full Subject Report",
        csv,
        file_name=f"Subject_{subject}_Report.csv",
        mime="text/csv"
    )

# ======================================================
# PAGE 5 FULL DATASET INSIGHTS
# ======================================================
elif page == "📁 Full Dataset Insights":

    st.title("📁 Full Dataset Insights")

    param = st.selectbox("Choose Parameter", numeric_cols)

    avg = df.groupby(subject_col)[param].mean().reset_index()

    fig = px.line(
        avg,
        x=subject_col,
        y=param,
        markers=True,
        title=f"{param} Across Subjects",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Summary Statistics")
    st.dataframe(df.describe(), use_container_width=True)

    full_csv = df.to_csv(index=False)

    st.download_button(
        "📥 Download Full Dataset",
        full_csv,
        file_name="Full_Gait_Dataset.csv",
        mime="text/csv"
    )
