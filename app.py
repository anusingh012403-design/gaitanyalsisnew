import streamlit as st

st.set_page_config(
    page_title="Clinical Gait Analysis Dashboard",
    page_icon="🦿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- PAGE CSS ----------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.hero-wrap {
    background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 55%, #06b6d4 100%);
    border-radius: 28px;
    padding: 2.2rem;
    color: white;
    box-shadow: 0 20px 50px rgba(0,0,0,0.18);
    margin-bottom: 1.5rem;
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.7rem;
}

.hero-sub {
    font-size: 1.05rem;
    line-height: 1.8;
    opacity: 0.96;
    margin-bottom: 1rem;
}

.pill {
    display: inline-block;
    padding: 0.45rem 0.9rem;
    margin-right: 0.5rem;
    margin-top: 0.4rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.22);
    font-size: 0.9rem;
    font-weight: 500;
}

.card {
    background: white;
    border-radius: 22px;
    padding: 1.2rem 1rem;
    box-shadow: 0 10px 25px rgba(2,6,23,0.08);
    border: 1px solid rgba(15,23,42,0.06);
    text-align: center;
    height: 100%;
}

.card h3 {
    margin: 0;
    color: #0f172a;
    font-size: 1.8rem;
    font-weight: 800;
}

.card p {
    margin: 0.35rem 0 0;
    color: #475569;
    font-size: 0.96rem;
}

.section-head {
    font-size: 1.4rem;
    font-weight: 800;
    color: #0f172a;
    margin-top: 0.5rem;
    margin-bottom: 0.8rem;
}

.info-box {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 22px;
    padding: 1.3rem;
    border-left: 6px solid #2563eb;
    box-shadow: 0 8px 20px rgba(15,23,42,0.06);
}

.info-box p {
    color: #334155;
    font-size: 1rem;
    line-height: 1.8;
    margin: 0;
}

.stImage img {
    border-radius: 24px;
    box-shadow: 0 14px 30px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=90)
st.sidebar.title("Clinical Gait AI")
st.sidebar.markdown("### Navigation")
st.sidebar.markdown("- 🏠 Home Dashboard")
st.sidebar.markdown("- 📊 Subject Comparison")
st.sidebar.markdown("- 🧠 Condition Analysis")
st.sidebar.markdown("- 📈 Monitoring")
st.sidebar.markdown("- 🤖 AI Insights Report")

# ---------- HERO ----------
left, right = st.columns([1.15, 1])

with left:
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-title">🦿 Clinical Gait Analysis Dashboard</div>
        <div class="hero-sub">
            Explore <b>Control</b>, <b>Reverse Walking</b>, and
            <b>Reverse Walking using Smartphone</b> conditions with a clean,
            interactive, and clinically inspired dashboard design.
        </div>
        <span class="pill">Reverse Walking</span>
        <span class="pill">Spatiotemporal Analysis</span>
        <span class="pill">Clinical Insights</span>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.image(
        "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/b2c3638e0351aea65ba1dda28a9bc1c056653996.jpg",
        use_container_width=True
    )

# ---------- HIGHLIGHTS ----------
st.markdown('<div class="section-head">Dashboard Highlights</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
        <h3>3</h3>
        <p>Subjects</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <h3>9</h3>
        <p>Total Trials</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
        <h3>3</h3>
        <p>Walking Conditions</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- ABOUT ----------
st.markdown('<div class="section-head">About This Project</div>', unsafe_allow_html=True)
st.markdown("""
<div class="info-box">
    <p>
        This dashboard focuses on clinical gait analysis with special attention to
        reverse walking performance. It helps compare subjects across different walking
        conditions using parameters such as speed, cadence, stride length, symmetry,
        and gait profile measures. Reverse walking is commonly studied in rehabilitation
        and movement analysis because it can reveal changes in balance, coordination,
        and lower-limb control.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🚀 Start exploring from the sidebar")
st.info("Use Subject Comparison, Condition Analysis, Monitoring, and AI Insights to navigate your report.")
