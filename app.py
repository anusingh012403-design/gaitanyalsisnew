import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Powered Clinical Gait Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_csv("clinical_dashboard_15_subjects.csv")
df.columns = df.columns.str.strip()

subject_col = "subject"
condition_col = "condition"

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
h1, h2, h3 {
    color: #0f172a;
}
div[data-testid="metric-container"] {
    background: white;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.image("https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600")
st.sidebar.title("Clinical Gait AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home Dashboard",
        "📊 Subject Comparison",
        "📈 Condition Analysis",
        "📡 Live Monitoring",
        "🤖 AI Insights Report"
    ]
)

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------
if page == "🏠 Home Dashboard":

    st.title("🏥 Clinical Gait Analysis Dashboard")
    st.image(
        "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=1200",
        use_container_width=True
    )

    st.markdown("### Smart AI Based Human Walking Analysis")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Subjects", df[subject_col].nunique())
    c2.metric("Records", len(df))
    c3.metric("Conditions", df[condition_col].nunique())
    c4.metric("Parameters", len(numeric_cols))

    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

    param = st.selectbox("Choose Parameter", numeric_cols)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            df.groupby(subject_col)[param].mean().reset_index(),
            x=subject_col,
            y=param,
            color=param,
            title="Average by Subject"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        pie = px.pie(
            df,
            names=condition_col,
            title="Condition Distribution"
        )
        st.plotly_chart(pie, use_container_width=True)

# ---------------------------------------------------
# SUBJECT COMPARISON
# ---------------------------------------------------
elif page == "📊 Subject Comparison":

    st.title("📊 Compare Subjects")

    subjects = sorted(df[subject_col].unique())

    col1, col2 = st.columns(2)

    with col1:
        s1 = st.selectbox("Select Subject 1", subjects)

    with col2:
        s2 = st.selectbox("Select Subject 2", subjects, index=1)

    param = st.selectbox("Select Parameter", numeric_cols)

    d1 = df[df[subject_col] == s1][param].mean()
    d2 = df[df[subject_col] == s2][param].mean()

    compare_df = pd.DataFrame({
        "Subject": [s1, s2],
        "Value": [d1, d2]
    })

    bar = px.bar(compare_df, x="Subject", y="Value", color="Subject",
                 title="Bar Comparison")
    st.plotly_chart(bar, use_container_width=True)

    # Radar chart
    radar = go.Figure()

    vals1 = df[df[subject_col] == s1][numeric_cols].mean().values
    vals2 = df[df[subject_col] == s2][numeric_cols].mean().values

    radar.add_trace(go.Scatterpolar(
        r=vals1,
        theta=numeric_cols,
        fill='toself',
        name=f"Subject {s1}"
    ))

    radar.add_trace(go.Scatterpolar(
        r=vals2,
        theta=numeric_cols,
        fill='toself',
        name=f"Subject {s2}"
    ))

    radar.update_layout(title="Radar Comparison")
    st.plotly_chart(radar, use_container_width=True)

# ---------------------------------------------------
# CONDITION ANALYSIS
# ---------------------------------------------------
elif page == "📈 Condition Analysis":

    st.title("📈 Condition Analysis")

    param = st.selectbox("Choose Parameter", numeric_cols)

    avg = df.groupby(condition_col)[param].mean().reset_index()

    bar = px.bar(avg, x=condition_col, y=param,
                 color=condition_col,
                 title="Average by Condition")
    st.plotly_chart(bar, use_container_width=True)

    donut = px.pie(avg, names=condition_col, values=param, hole=0.5,
                   title="Donut Chart")
    st.plotly_chart(donut, use_container_width=True)

# ---------------------------------------------------
# LIVE MONITORING
# ---------------------------------------------------
elif page == "📡 Live Monitoring":

    st.title("📡 Live Sensor Monitoring")

    param = st.selectbox("Choose Parameter", numeric_cols)

    chart = st.empty()

    data = []

    for i in range(50):
        data.append(np.random.randn() + df[param].mean())
        live_df = pd.DataFrame(data, columns=[param])
        fig = px.line(live_df, y=param, title="Live Signal")
        chart.plotly_chart(fig, use_container_width=True)
        time.sleep(0.1)

# ---------------------------------------------------
# AI REPORT
# ---------------------------------------------------
elif page == "🤖 AI Insights Report":

    st.title("🤖 AI Medical Report")

    param = st.selectbox("Choose Parameter", numeric_cols)

    c1, c2, c3 = st.columns(3)

    c1.metric("Average", round(df[param].mean(),2))
    c2.metric("Maximum", round(df[param].max(),2))
    c3.metric("Minimum", round(df[param].min(),2))

    best = df.groupby(subject_col)[param].mean().idxmax()
    low = df.groupby(subject_col)[param].mean().idxmin()

    st.success(f"Best performer for {param}: Subject {best}")
    st.warning(f"Needs improvement: Subject {low}")

    # download report
    report = df.describe().to_csv(index=True).encode("utf-8")

    st.download_button(
        label="📥 Download Full AI Report",
        data=report,
        file_name="AI_Gait_Report.csv",
        mime="text/csv"
    )

    heat = px.imshow(df[numeric_cols].corr(),
                     text_auto=True,
                     title="Correlation Heatmap")
    st.plotly_chart(heat, use_container_width=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.write("Developed using Streamlit + AI + Plotly | Premium Dashboard")
