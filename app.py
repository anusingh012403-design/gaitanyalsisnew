import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Powered Clinical Gait Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
df = pd.read_csv("clinical_dashboard_15_subjects.csv")
df.columns = df.columns.str.strip().str.lower()

# rename safe
df.rename(columns={
    "subject_id":"subject",
    "subject id":"subject"
}, inplace=True)

# detect required cols
subject_col = "subject"
condition_col = "condition"

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(to right,#f8fbff,#eef5ff);
}
h1,h2,h3 {
    color:#0b1f4d;
}
.stButton>button {
    background:#0b1f4d;
    color:white;
    border-radius:10px;
}
.metric-box{
    background:white;
    padding:15px;
    border-radius:12px;
    box-shadow:0 4px 10px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
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

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
if page == "🏠 Home Dashboard":

    st.title("🧠 Clinical Gait Analysis Dashboard")

    # AI generated reverse walking image
    st.image(
        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=1400&q=80",
        use_container_width=True
    )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Records", len(df))
    c2.metric("Subjects", df[subject_col].nunique())
    c3.metric("Conditions", df[condition_col].nunique())
    c4.metric("Parameters", len(numeric_cols))

    st.markdown("---")

    st.subheader("Dataset Preview")
    st.dataframe(df.head(15), use_container_width=True)

    st.subheader("Average Walking Speed by Subject")

    speed_col = "walking_speed" if "walking_speed" in df.columns else numeric_cols[0]

    avg = df.groupby(subject_col)[speed_col].mean().reset_index()

    fig = px.bar(
        avg,
        x=subject_col,
        y=speed_col,
        color=speed_col,
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# SUBJECT COMPARISON
# -------------------------------------------------
elif page == "📊 Subject Comparison":

    st.title("📊 Subject Comparison Dashboard")

    subjects = sorted(df[subject_col].unique())

    c1,c2 = st.columns(2)
    s1 = c1.selectbox("Select Subject 1", subjects)
    s2 = c2.selectbox("Select Subject 2", subjects, index=1)

    param = st.selectbox("Choose Parameter", numeric_cols)

    d1 = df[df[subject_col]==s1][param].mean()
    d2 = df[df[subject_col]==s2][param].mean()

    comp = pd.DataFrame({
        "Subject":[s1,s2],
        "Value":[d1,d2]
    })

    fig = px.bar(comp,x="Subject",y="Value",color="Subject",text_auto=True)
    st.plotly_chart(fig,use_container_width=True)

    # radar graph
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

# -------------------------------------------------
# CONDITION ANALYSIS
# -------------------------------------------------
elif page == "📈 Condition Analysis":

    st.title("📈 Condition Analysis")

    param = st.selectbox("Choose Parameter", numeric_cols)

    grp = df.groupby(condition_col)[param].mean().reset_index()

    fig = px.pie(
        grp,
        names=condition_col,
        values=param,
        hole=0.45
    )
    st.plotly_chart(fig,use_container_width=True)

    fig2 = px.bar(
        grp,
        x=condition_col,
        y=param,
        color=condition_col,
        text_auto=True
    )
    st.plotly_chart(fig2,use_container_width=True)

# -------------------------------------------------
# AI REPORT
# -------------------------------------------------
elif page == "🤖 AI Report":

    st.title("🤖 AI Powered Subject Report")

    subjects = sorted(df[subject_col].unique())
    s = st.selectbox("Select Subject", subjects)

    user = df[df[subject_col]==s]

    st.subheader(f"Subject {s} Overview")

    c1,c2,c3 = st.columns(3)

    for_metric = numeric_cols[:3]

    c1.metric(for_metric[0], round(user[for_metric[0]].mean(),2))
    c2.metric(for_metric[1], round(user[for_metric[1]].mean(),2))
    c3.metric(for_metric[2], round(user[for_metric[2]].mean(),2))

    st.subheader("Performance Graph")

    vals = user[numeric_cols[:6]].mean()

    fig = px.bar(
        x=vals.index,
        y=vals.values,
        text_auto=True
    )
    st.plotly_chart(fig,use_container_width=True)

    # AI Summary
    st.subheader("AI Summary")

    best = vals.idxmax()
    worst = vals.idxmin()

    st.success(f"Best parameter: {best}")
    st.warning(f"Needs improvement: {worst}")

    # downloadable report
    report = f"""
CLINICAL GAIT REPORT

Subject: {s}

Average Values:

{vals.to_string()}

Best Parameter: {best}
Needs Improvement: {worst}

Generated by AI Powered Dashboard
"""

    st.download_button(
        "📥 Download Full AI Report",
        report,
        file_name=f"subject_{s}_report.txt"
    )

# -------------------------------------------------
# LIVE SIMULATION
# -------------------------------------------------
elif page == "🎥 Live Simulation":

    st.title("🎥 Live Reverse Walking Simulation")

    progress = st.progress(0)

    for i in range(100):
        progress.progress(i+1)

    st.success("Simulation Completed")

    sim_subject = st.selectbox("Select Subject", sorted(df[subject_col].unique()))

    user = df[df[subject_col]==sim_subject]

    st.line_chart(user[numeric_cols[:4]])

    st.info("This graph simulates gait sensor signals during reverse walking.")
