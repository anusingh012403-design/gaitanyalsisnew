import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Clinical Gait Analysis Dashboard",
    layout="wide",
    page_icon="🧠"
)

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}
h1,h2,h3 {
    color: #0f172a;
}
.metric-box {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
}
</style>
""", unsafe_allow_html=True)

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
# SIDEBAR
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
# HOME DASHBOARD
# ==================================================
if page == "🏠 Home Dashboard":

    st.title("🧠 Clinical Gait Analysis Dashboard")
    st.markdown("### Advanced Multi-Subject Biomechanics Monitoring System")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Records", len(df))
    c2.metric("Subjects", df[subject_col].nunique())
    c3.metric("Conditions", df[condition_col].nunique())
    c4.metric("Parameters", len(numeric_cols))

    st.markdown("---")

    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    st.subheader("Average Walking Speed by Subject")

    speed = df.groupby(subject_col)["walking_speed"].mean().reset_index()

    fig = px.bar(
        speed,
        x=subject_col,
        y="walking_speed",
        color="walking_speed",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# SUBJECT COMPARISON
# ==================================================
elif page == "📊 Subject Comparison":

    st.title("📊 Subject Comparison")

    col1,col2 = st.columns(2)

    s1 = col1.selectbox("Select Subject 1", sorted(df[subject_col].unique()))
    s2 = col2.selectbox("Select Subject 2", sorted(df[subject_col].unique()), index=1)

    param = st.selectbox("Choose Parameter", numeric_cols)

    d1 = df[df[subject_col]==s1][param].mean()
    d2 = df[df[subject_col]==s2][param].mean()

    compare = pd.DataFrame({
        "Subject":[s1,s2],
        "Value":[d1,d2]
    })

    fig = px.bar(
        compare,
        x="Subject",
        y="Value",
        color="Subject",
        text="Value",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Radar Graph
    st.subheader("Radar Comparison")

    radar_params = numeric_cols[:6]

    val1 = [df[df[subject_col]==s1][p].mean() for p in radar_params]
    val2 = [df[df[subject_col]==s2][p].mean() for p in radar_params]

    fig2 = go.Figure()

    fig2.add_trace(go.Scatterpolar(
        r=val1,
        theta=radar_params,
        fill='toself',
        name=f"Subject {s1}"
    ))

    fig2.add_trace(go.Scatterpolar(
        r=val2,
        theta=radar_params,
        fill='toself',
        name=f"Subject {s2}"
    ))

    fig2.update_layout(template="plotly_white")

    st.plotly_chart(fig2, use_container_width=True)

# ==================================================
# CONDITION ANALYSIS
# ==================================================
elif page == "📈 Condition Analysis":

    st.title("📈 Condition Analysis")

    param = st.selectbox("Choose Parameter", numeric_cols)

    avg = df.groupby(condition_col)[param].mean().reset_index()

    col1,col2 = st.columns(2)

    with col1:
        fig = px.bar(
            avg,
            x=condition_col,
            y=param,
            color=condition_col,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(
            df,
            names=condition_col,
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)

# ==================================================
# LIVE MONITORING
# ==================================================
elif page == "📡 Live Monitoring":

    st.title("📡 Live Monitoring Simulation")

    subject = st.selectbox("Choose Subject", sorted(df[subject_col].unique()))
    param = st.selectbox("Choose Parameter", numeric_cols)

    live = df[df[subject_col]==subject][param].values

    chart = st.empty()

    for i in range(len(live)):
        temp = pd.DataFrame({
            "Time": np.arange(i+1),
            "Value": live[:i+1]
        })

        fig = px.line(
            temp,
            x="Time",
            y="Value",
            markers=True,
            template="plotly_white"
        )

        chart.plotly_chart(fig, use_container_width=True)

# ==================================================
# AI REPORT
# ==================================================
elif page == "🤖 AI Report":

    st.title("🤖 AI Insights Report")

    subject = st.selectbox("Select Subject", sorted(df[subject_col].unique()))

    sub = df[df[subject_col]==subject]

    c1,c2,c3 = st.columns(3)

    c1.metric("Avg Speed", round(sub["walking_speed"].mean(),2))
    c2.metric("Avg Cadence", round(sub["cadence"].mean(),2))
    c3.metric("Avg Stride", round(sub["stride_length"].mean(),2))

    st.markdown("---")

    st.subheader("Performance Graph")

    graph = sub[numeric_cols].mean().reset_index()
    graph.columns = ["Parameter","Value"]

    fig = px.bar(
        graph,
        x="Parameter",
        y="Value",
        color="Value",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    report = sub.describe().to_csv(index=True)

    st.download_button(
        "📥 Download Full AI Report",
        report,
        file_name=f"Subject_{subject}_AI_Report.csv",
        mime="text/csv"
    )
