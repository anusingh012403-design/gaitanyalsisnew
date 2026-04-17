import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
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

# clean columns
df.columns = df.columns.str.strip().str.lower()

# rename columns if needed
if "subject_id" in df.columns:
    df.rename(columns={"subject_id": "subject"}, inplace=True)

if "subject id" in df.columns:
    df.rename(columns={"subject id": "subject"}, inplace=True)

subject_col = "subject"
condition_col = "condition"

# ONLY real parameters (remove subject)
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

if subject_col in numeric_cols:
    numeric_cols.remove(subject_col)

# ---------------------------------------------------
# CSS
# ---------------------------------------------------
st.markdown("""
<style>
.main{
background:linear-gradient(to right,#f8fbff,#edf5ff);
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
    "Choose Page",
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
    st.subheader("AI Based Reverse Walking Monitoring")

    # IMAGE REMOVED

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Records", len(df))
    c2.metric("Subjects", df[subject_col].nunique())
    c3.metric("Conditions", df[condition_col].nunique())
    c4.metric("Parameters", len(numeric_cols))

    st.markdown("---")

    speed_col = numeric_cols[0]

    col1,col2 = st.columns(2)

    with col1:
        avg = df.groupby(subject_col, as_index=False)[speed_col].mean()

        fig = px.bar(
            avg,
            x=subject_col,
            y=speed_col,
            color=speed_col,
            text_auto=True,
            title="Average Parameter by Subject"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        grp = df.groupby(condition_col, as_index=False)[speed_col].mean()

        fig2 = px.pie(
            grp,
            names=condition_col,
            values=speed_col,
            hole=0.45,
            title="Condition Distribution"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Dataset Preview")
    st.dataframe(df.head(15), use_container_width=True)

# ===================================================
# SUBJECT COMPARISON
# ===================================================
elif page == "📊 Subject Comparison":

    st.title("📊 Subject Comparison")

    subjects = sorted(df[subject_col].unique())

    col1,col2 = st.columns(2)

    s1 = col1.selectbox("Select Subject 1", subjects)
    s2 = col2.selectbox("Select Subject 2", subjects, index=1)

    param = st.selectbox("Choose Parameter", numeric_cols)

    # FIXED: subject removed from parameter list

    val1 = df[df[subject_col]==s1][param].mean()
    val2 = df[df[subject_col]==s2][param].mean()

    compare_df = pd.DataFrame({
        "Subject":[s1,s2],
        "Value":[val1,val2]
    })

    fig = px.bar(
        compare_df,
        x="Subject",
        y="Value",
        color="Subject",
        text_auto=True,
        title="Bar Comparison"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Radar Graph
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

    st.plotly_chart(fig2, use_container_width=True)

# ===================================================
# CONDITION ANALYSIS
# ===================================================
elif page == "📈 Condition Analysis":

    st.title("📈 Condition Analysis")

    param = st.selectbox("Choose Parameter", numeric_cols)

    grp = df.groupby(condition_col, as_index=False)[param].mean()

    fig = px.bar(
        grp,
        x=condition_col,
        y=param,
        color=condition_col,
        text_auto=True,
        title="Average by Condition"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.pie(
        grp,
        names=condition_col,
        values=param,
        hole=0.45,
        title="Condition Pie Chart"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ===================================================
# AI REPORT
# ===================================================
elif page == "🤖 AI Report":

    st.title("🤖 AI Subject Report")

    subjects = sorted(df[subject_col].unique())

    s = st.selectbox("Choose Subject", subjects)

    user = df[df[subject_col]==s]

    vals = user[numeric_cols[:6]].mean()

    c1,c2,c3 = st.columns(3)

    c1.metric("Average", round(vals.mean(),2))
    c2.metric("Maximum", round(vals.max(),2))
    c3.metric("Minimum", round(vals.min(),2))

    fig = px.bar(
        x=vals.index,
        y=vals.values,
        text_auto=True,
        title="Performance Parameters"
    )
    st.plotly_chart(fig, use_container_width=True)

    best = vals.idxmax()
    weak = vals.idxmin()

    st.success(f"Best Parameter: {best}")
    st.warning(f"Needs Improvement: {weak}")

    report = f"""
CLINICAL GAIT REPORT

Subject : {s}

Average Values:

{vals.to_string()}

Best Parameter : {best}
Needs Improvement : {weak}

Generated by AI Dashboard
"""

    st.download_button(
        "📥 Download Report",
        report,
        file_name=f"subject_{s}_report.txt"
    )

# ===================================================
# LIVE SIMULATION
# ===================================================
elif page == "🎥 Live Simulation":

    st.title("🎥 Live Reverse Walking Simulation")

    st.info("Sensor Motion Simulation")

    s = st.selectbox("Choose Subject", sorted(df[subject_col].unique()))

    user = df[df[subject_col]==s]

    st.line_chart(user[numeric_cols[:4]])
