import streamlit as st
import pandas as pd
import plotly.express as px

def render(df, df_raw, selected_year):
    # -----------------------------
    # Section heading
    # -----------------------------
    st.markdown("### 📊 Workforce Composition")

    # -----------------------------
    # Load CSS file
    # -----------------------------
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # -----------------------------
    # Sheets
    # -----------------------------
    tenure = df["Tenure Analysis"]
    resign = df["Resignation Trends"]
    hc = df["Headcount Per Year"]

    # -----------------------------
    # Filter by selected year
    # -----------------------------
    tenure_year = tenure[tenure["Year"] == selected_year]
    resign_year = resign[resign["Year"] == selected_year]
    hc_year = hc[hc["Year"] == selected_year]

    # -----------------------------
    # Compute metrics
    # -----------------------------
    active_count = int(tenure_year["Count"].sum()) if not tenure_year.empty else 0
    leaver_count = int(resign_year["LeaverCount"].sum()) if not resign_year.empty else 0
    total_headcount = active_count + leaver_count

    # -----------------------------
    # Display summary metrics
    # -----------------------------
    mcol1, mcol2, mcol3 = st.columns(3)
    mcol1.markdown(f"<div class='metric-label'>Total Headcount</div><div class='metric-value'>{total_headcount:,}</div>", unsafe_allow_html=True)
    mcol2.markdown(f"<div class='metric-label'>Active Employees</div><div class='metric-value'>{active_count:,}</div>", unsafe_allow_html=True)
    mcol3.markdown(f"<div class='metric-label'>Leavers</div><div class='metric-value'>{leaver_count:,}</div>", unsafe_allow_html=True)

    # -----------------------------
    # Normalize values for charts
    # -----------------------------
    df_raw["Resignee Checking"] = df_raw["Resignee Checking"].str.strip().str.upper()
    df_raw["Generation"] = df_raw["Generation"].str.strip().str.capitalize()
    df_raw["Position/Level"] = df_raw["Position/Level"].str.strip()
    df_raw["Gender"] = df_raw["Gender"].str.strip().str.capitalize()
    if "Age Bucket" in df_raw.columns:
        df_raw["Age Bucket"] = df_raw["Age Bucket"].str.strip().str.capitalize()

    active_df = df_raw[df_raw["Resignee Checking"] == "ACTIVE"]

    # -----------------------------
    # Row 1: Headcount charts
    # -----------------------------
    top_col1, top_col2 = st.columns(2)

    with top_col1:
        st.markdown("### Headcount per Position/Level")
        headcount_summary = (
            active_df.groupby(["Calendar Year", "Position/Level"])
            .size()
            .reset_index(name="Headcount")
            .sort_values("Calendar Year")
        )
        fig1 = px.bar(headcount_summary, x="Calendar Year", y="Headcount",
                      color="Position/Level", barmode="stack",
                      color_discrete_map={"Associate": "#ADD8E6", "Manager & Up": "#00008B"})
        st.plotly_chart(fig1, use_container_width=True, height=300)

    with top_col2:
        st.markdown("### Headcount per Generation")
        headcount_gen = (
            active_df.groupby(["Calendar Year", "Generation"])
            .size()
            .reset_index(name="Headcount")
            .sort_values("Calendar Year")
        )
        fig2 = px.bar(headcount_gen, x="Calendar Year", y="Headcount",
                      color="Generation", barmode="stack",
                      color_discrete_sequence=["#ADD8E6", "#00008B", "#87CEEB", "#1E3A8A", "#4682B4"])
        st.plotly_chart(fig2, use_container_width=True, height=300)

    # -----------------------------
    # Row 2: Age Distribution, Gender Diversity, Tenure Analysis
    # -----------------------------
    colA, colB, colC = st.columns(3)

    with colA:
        st.markdown(f"### Age Distribution ({selected_year})")
        age_year = df["Age Distribution"][df["Age Distribution"]["Year"] == selected_year].copy()
        avg_age = round(age_year["Age"].mean(), 1) if not age_year.empty else 0
        median_age = float(age_year["Age"].median()) if not age_year.empty else 0

        a1, a2 = st.columns(2)
        a1.markdown(f"<div class='metric-label'>Average Age</div><div class='metric-value'>{avg_age}</div>", unsafe_allow_html=True)
        a2.markdown(f"<div class='metric-label'>Median Age</div><div class='metric-value'>{median_age}</div>", unsafe_allow_html=True)

        if "Generation" in age_year.columns:
            fig3 = px.histogram(
                age_year, x="Age",
                y="Count",
                color="Generation",
                barmode="group",
                color_discrete_sequence=["#ADD8E6", "#00008B", "#87CEEB", "#1E3A8A", "#4682B4"]
            )
        else:
            fig3 = px.histogram(
                age_year,
                x="Age",
                y="Count",
                color_discrete_sequence=["#ADD8E6", "#00008B"]
            )
        fig3.update_layout(showlegend=True, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig3, use_container_width=True, height=300, key="age_distribution")

    with colB:
        st.markdown(f"### Gender Diversity ({selected_year})")
        gender = df["Gender Diversity"]
        gender_year = gender[gender["Year"] == selected_year]
        gender_counts = gender_year.groupby("Gender")["Count"].sum()

        gcols = st.columns(len(gender_counts))
        for i, (g, c) in enumerate(gender_counts.items()):
            gcols[i].markdown(f"<div class='metric-label'>{g} Employees</div><div class='metric-value'>{int(c)}</div>", unsafe_allow_html=True)

        fig4 = px.bar(gender_year, x="Position/Level", y="Count", color="Gender", barmode="stack")
        st.plotly_chart(fig4, use_container_width=True, height=300)

    with colC:
        st.markdown(f"### Tenure Analysis ({selected_year})")
        avg_tenure = round(tenure_year["Tenure"].mean(), 1) if not tenure_year.empty else 0
        median_tenure = float(tenure_year["Tenure"].median()) if not tenure_year.empty else 0
        max_tenure = float(tenure_year["Tenure"].max()) if not tenure_year.empty else 0

        t1, t2, t3 = st.columns(3)
        t1.markdown(f"<div class='metric-label'>Average Tenure</div><div class='metric-value'>{avg_tenure} yrs</div>", unsafe_allow_html=True)
        t2.markdown(f"<div class='metric-label'>Median Tenure</div><div class='metric-value'>{median_tenure} yrs</div>", unsafe_allow_html=True)
        t3.markdown(f"<div class='metric-label'>Longest Tenure</div><div class='metric-value'>{max_tenure} yrs</div>", unsafe_allow_html=True)

        fig5 = px.scatter(tenure, x="Tenure", y="Count", color="YearJoined", size="Count")
        st.plotly_chart(fig5, use_container_width=True, height=300)
