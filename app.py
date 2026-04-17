# ==============================
# REMOVE OLD DASHBOARD IMAGE CODE
# Replace ONLY Home Dashboard page code
# ==============================

if page == "🏠 Home Dashboard":

    st.markdown("""
    <h1 style='text-align:center; color:#1f4e79;'>
    🧠 Advanced Clinical Gait Dashboard
    </h1>
    <h4 style='text-align:center; color:gray;'>
    Multi Subject Motion Analysis System
    </h4>
    """, unsafe_allow_html=True)

    # ===== NO IMAGE SECTION =====
    # Old image removed completely

    # ===== KPI CARDS =====
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Records", len(df))
    c2.metric("Subjects", df["subject"].nunique())
    c3.metric("Conditions", df["condition"].nunique())
    c4.metric("Parameters", len(numeric_cols))

    st.markdown("---")

    # ===== CHARTS =====
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Average Walking Speed")

        avg_speed = df.groupby("subject")["walking_speed"].mean().reset_index()

        fig = px.bar(
            avg_speed,
            x="subject",
            y="walking_speed",
            color="walking_speed",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Condition Distribution")

        cond = df["condition"].value_counts().reset_index()
        cond.columns = ["condition", "count"]

        fig2 = px.pie(
            cond,
            names="condition",
            values="count",
            hole=0.4
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    st.subheader("Dataset Preview")
    st.dataframe(df.head(15), use_container_width=True)
