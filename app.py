import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# ---------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------
st.set_page_config(
    page_title="Clinical Gait Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_csv("clinical_dashboard_15_subjects.csv")

df.columns = df.columns.str.strip().str.lower()

# rename if needed
if "subject_id" in df.columns:
    df.rename(columns={"subject_id":"subject"}, inplace=True)

if "subject id" in df.columns:
    df.rename(columns={"subject id":"subject"}, inplace=True)

subject_col = "subject"
condition_col = "condition"

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# ---------------------------------------------------
# CSS
# ---------------------------------------------------
st.markdown("""
<style>
.main {
background: linear-gradient(to right,#f8fbff,#edf5ff);
}
h1,h2,h3{
color:#102a43;
}
section[data-testid="stSidebar"]{
background:#0f172a;
color:white;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "🏠 Home Dashboard",
        "📊 Subject Comparison",
        "📈 Condition Analysis",
        "🤖 AI Report",
        "🎥 Live Simulation"
    ]
)

# ===================================================
# HOME DASHBOARD
# ===================================================
if page == "🏠 Home Dashboard":

    st.title("🧠 Clinical Gait Analysis Dashboard")
    st.subheader("AI Powered Reverse Walking Monitoring System")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Records", len(df))
    c2.metric("Subjects", df[subject_col].nunique())
    c3.metric("Conditions", df[condition_col].nunique())
    c4.metric("Parameters", len(numeric_cols))

    st.markdown("---")

    speed_col = "walking_speed" if "walking_speed" in df.columns else numeric_cols[0]

    col1,col2 = st.columns(2)

    with col1:
        avg = df.groupby(subject_col)[speed_col].mean().reset_index()

        fig = px.bar(
            avg,
            x=subject_col,
            y=speed_col,
            color=speed_col,
            text_auto=True,
            title="Average Walking Speed"
        )
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        grp = df.groupby(condition_col)[speed_col].mean().reset_index()

        fig2 = px.pie(
            grp,
            names=condition_col,
            values=speed_col,
            hole=0.45,
            title="Condition Distribution"
        )
        st.plotly_chart(fig2,use_container_width=True)

    st.markdown("---")
    st.subheader("Dataset Preview")
    st.dataframe(df.head(15), use_container_width=True)

# ===================================================
# SUBJECT COMPARISON
# ===================================================
elif page == "📊 Subject Comparison":

    st.title("📊 Compare Subjects")

    subjects = sorted(df[subject_col].unique())

    col1,col2 = st.columns(2)

    s1 = col1.selectbox("Select Subject 1", subjects)
    s2 = col2.selectbox("Select Subject 2", subjects, index=1)

    param = st.selectbox("Choose Parameter", numeric_cols)

    val1 = df[df[subject_col]==s1][param].mean()
    val2 = df[df[subject_col]==s2][param].mean()

    comp = pd.DataFrame({
        "Subject":[s1,s2],
        "Value":[val1,val2]
    })

    fig = px.bar(
        comp,
        x="Subject",
        y="Value",
        color="Subject",
        text_auto=True,
        title="Comparison Bar Graph"
    )
    st.plotly_chart(fig,use_container_width=True)

    # radar
    st.subheader("Radar Comparison")

    radar_cols = numeric_cols[:6]

    r1 = df[df[subject_col]==s1][radar_cols].mean()
    r2 = df[df[subject_col]==s2][radar_cols].mean()

    fig2 = go.Figure()

    fig2.add_trace(go.Scatterpolar(
        r=r1.values,
        theta=radar_cols,
        fill='toself',
        name=f"Subject {s1}"
    ))

    fig2.add_trace(go.Scatterpolar(
        r=r2.values,
        theta=radar_cols,
        fill='toself',
        name=f"Subject {s2}"
    ))

    st.plotly_chart(fig2,use_container_width=True)

# ===================================================
# CONDITION ANALYSIS
# ===================================================
elif page == "📈 Condition Analysis":

    st.title("📈 Condition Analysis")

    param = st.selectbox("Choose Parameter", numeric_cols)

    grp = df.groupby(condition_col)[param].mean().reset_index()

    fig = px.bar(
        grp,
        x=condition_col,
        y=param,
        color=condition_col,
        text_auto=True,
        title="Average by Condition"
    )
    st.plotly_chart(fig,use_container_width=True)

    fig2 = px.pie(
        grp,
        names=condition_col,
        values=param,
        hole=0.4,
        title="Condition Pie Graph"
    )
    st.plotly_chart(fig2,use_container_width=True)

# ===================================================
# AI REPORT
# ===================================================
elif page == "🤖 AI Report":

    st.title("🤖 AI Subject Report")

    subjects = sorted(df[subject_col].unique())
    s = st.selectbox("Choose Subject", subjects)

    user = df[df[subject_col]==s]

    st.subheader(f"Subject {s} Analysis")

    c1,c2,c3 = st.columns(3)

    c1.metric("Avg Speed", round(user[numeric_cols[0]].mean(),2))
    c2.metric("Max Value", round(user[numeric_cols[0]].max(),2))
    c3.metric("Min Value", round(user[numeric_cols[0]].min(),2))

    vals = user[numeric_cols[:6]].mean()

    fig = px.bar(
        x=vals.index,
        y=vals.values,
        text_auto=True,
        title="Performance Parameters"
    )
    st.plotly_chart(fig,use_container_width=True)

    best = vals.idxmax()
    weak = vals.idxmin()

    st.success(f"Best Parameter: {best}")
    st.warning(f"Needs Improvement: {weak}")

    report = f"""
CLINICAL GAIT REPORT

Subject : {s}

Average Parameters:

{vals.to_string()}

Best Parameter : {best}
Needs Improvement : {weak}

Generated by AI Dashboard
"""

    st.download_button(
        "📥 Download Full Report",
        report,
        file_name=f"subject_{s}_report.txt"
    )

# ===================================================
# LIVE SIMULATION
# ===================================================
elif page == "🎥 Live Simulation":

    st.title("🎥 Live Reverse Walking Simulation")

    progress = st.progress(0)

    for i in range(100):
        progress.progress(i+1)

    st.success("Simulation Completed")

    s = st.selectbox("Select Subject", sorted(df[subject_col].unique()))

    user = df[df[subject_col]==s]

    st.line_chart(user[numeric_cols[:4]])

    st.info("Sensor signals simulation during reverse walking.")
