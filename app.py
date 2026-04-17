# ==========================================================
# ADVANCED PROFESSIONAL HOME PAGE + FULL DASHBOARD
# Replace complete app.py with this code
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="Clinical Gait Analysis Dashboard",
    layout="wide",
    page_icon="🧠"
)

# ----------------------------------------------------------
# PROFESSIONAL CSS
# ----------------------------------------------------------
st.markdown("""
<style>
.main{
    background:#f8fafc;
}
h1,h2,h3{
    color:#0f172a;
}
[data-testid="metric-container"]{
    background:white;
    border:1px solid #e2e8f0;
    padding:18px;
    border-radius:14px;
    box-shadow:0 4px 10px rgba(0,0,0,0.05);
}
.hero{
    padding:20px;
    background:linear-gradient(90deg,#0f172a,#1e293b);
    color:white;
    border-radius:16px;
}
.small-note{
    color:#475569;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------
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

# ----------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------
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

# ==========================================================
# PAGE 1 HOME DASHBOARD (PROFESSIONAL)
# ==========================================================
if page == "🏠 Home Dashboard":

    st.markdown("""
    <div class='hero'>
        <h1>🧠 Advanced Clinical Gait Dashboard</h1>
        <h3>AI Powered Reverse Walking • EMG • Motion Analysis</h3>
        <p>Clinical biomechanics monitoring platform for subject movement analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Records", len(df))
    c2.metric("Subjects", df[subject_col].nunique())
    c3.metric("Conditions", df[condition_col].nunique())
    c4.metric("Parameters", len(numeric_cols))

    st.markdown("---")

    # --------------------------------------------
    # PROFESSIONAL IMAGE SECTION
    # --------------------------------------------
    st.subheader("🎥 Clinical Reverse Walking Lab Setup")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.image(
            "https://images.unsplash.com/photo-1518611012118-696072aa579a",
            caption="Sensor Based Walking Analysis",
            use_container_width=True
        )

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b",
            caption="Camera Lab Motion Capture",
            use_container_width=True
        )

    with col3:
        st.image(
            "https://images.unsplash.com/photo-1517836357463-d25dfeac3438",
            caption="Reverse Gait Monitoring",
            use_container_width=True
        )

    st.markdown("---")

    # --------------------------------------------
    # CHARTS
    # --------------------------------------------
    col1,col2 = st.columns(2)

    with col1:
        speed = df.groupby(subject_col)["walking_speed"].mean().reset_index()

        fig = px.bar(
            speed,
            x=subject_col,
            y="walking_speed",
            color="walking_speed",
            title="Average Walking Speed by Subject",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(
            df,
            names=condition_col,
            title="Walking Condition Distribution",
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    st.subheader("📋 Dataset Preview")
    st.dataframe(df, use_container_width=True)

# ==========================================================
# PAGE 2 SUBJECT COMPARISON
# ==========================================================
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
        fig = px.bar(compare,x="Subject",y="Value",color="Subject",
                     text="Value",template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(compare,names="Subject",values="Value",
                      template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

    radar_params = numeric_cols[:6]

    r1 = [df[df[subject_col]==s1][p].mean() for p in radar_params]
    r2 = [df[df[subject_col]==s2][p].mean() for p in radar_params]

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(
        r=r1, theta=radar_params, fill='toself', name=f"Subject {s1}"
    ))

    radar.add_trace(go.Scatterpolar(
        r=r2, theta=radar_params, fill='toself', name=f"Subject {s2}"
    ))

    radar.update_layout(template="plotly_white")

    st.plotly_chart(radar, use_container_width=True)

# ==========================================================
# PAGE 3 LIVE MONITORING
# ==========================================================
elif page == "📡 Live Monitoring":

    st.title("📡 Live Monitoring")

    subject = st.selectbox("Select Subject", sorted(df[subject_col].unique()))
    param = st.selectbox("Select Parameter", numeric_cols)

    vals = df[df[subject_col]==subject][param].values

    holder = st.empty()

    for i in range(len(vals)):
        temp = pd.DataFrame({
            "Time": np.arange(i+1),
            "Value": vals[:i+1]
        })

        fig = px.line(
            temp,x="Time",y="Value",
            markers=True,
            template="plotly_white"
        )

        holder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.4)

# ==========================================================
# PAGE 4 CLINICAL REPORT
# ==========================================================
elif page == "📄 Clinical Report":

    st.title("📄 Subject Clinical Report")

    subject = st.selectbox("Choose Subject", sorted(df[subject_col].unique()))

    sub = df[df[subject_col]==subject]

    c1,c2,c3 = st.columns(3)

    c1.metric("Avg Speed", round(sub["walking_speed"].mean(),2))
    c2.metric("Avg Cadence", round(sub["cadence"].mean(),2))
    c3.metric("Avg Stride", round(sub["stride_length"].mean(),2))

    report = sub[numeric_cols].mean().reset_index()
    report.columns = ["Parameter","Value"]

    fig = px.bar(
        report,
        x="Parameter",
        y="Value",
        color="Value",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(sub, use_container_width=True)

    csv = sub.to_csv(index=False)

    st.download_button(
        "📥 Download Subject Report",
        csv,
        file_name=f"Subject_{subject}_Report.csv",
        mime="text/csv"
    )

# ==========================================================
# PAGE 5 FULL DATASET
# ==========================================================
elif page == "📁 Full Dataset Insights":

    st.title("📁 Full Dataset Insights")

    param = st.selectbox("Choose Parameter", numeric_cols)

    avg = df.groupby(subject_col)[param].mean().reset_index()

    fig = px.line(
        avg,x=subject_col,y=param,
        markers=True,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df.describe(), use_container_width=True)

    st.download_button(
        "📥 Download Full Dataset",
        df.to_csv(index=False),
        file_name="Full_Dataset.csv",
        mime="text/csv"
    )
