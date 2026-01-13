import streamlit as st
import pandas as pd
import plotly.express as px


def render(df, df_raw, selected_year):
    st.markdown("## 📊 Career Progression Overview")

    # Ensure numeric conversion for Promotion & Transfer
    def to_num(x): 
        s = str(x).strip().upper() 
        if s in {"1", "YES", "TRUE"}: 
            return 1 
        if s in {"0", "NO", "FALSE"}: 
            return 0 
        try: 
            return float(s) 
        except: 
            return pd.NA 

    # Normalize columns
    df_raw["Promotion & Transfer"] = df_raw["Promotion & Transfer"].apply(to_num)
    df_raw["Calendar Year"] = pd.to_datetime(df_raw["Calendar Year"], errors="coerce")
    df_raw["Year"] = df_raw["Calendar Year"].dt.year
    df_raw["Resignee Checking"] = df_raw["Resignee Checking"].astype(str).str.strip().str.upper()

    # Filter by selected year and active employees
    career_year = df_raw[
        (df_raw["Year"] == int(selected_year)) &
        (df_raw["Resignee Checking"] == "ACTIVE")
    ]

    if not career_year.empty: 
        # Count only Promotion & Transfer == 1
        total_promotions_transfers = int(
            career_year["Promotion & Transfer"].fillna(0).eq(1).sum()
        )
        avg_tenure = pd.to_numeric(career_year["Tenure"], errors="coerce").mean()

        # Promotion Rate KPI (% of active employees promoted/transferred)
        active_count = len(career_year)
        promotion_rate = (total_promotions_transfers / active_count * 100) if active_count > 0 else 0
    else: 
        total_promotions_transfers = 0 
        avg_tenure = 0 
        promotion_rate = 0

    # Top metrics row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-label'>Promotions & Transfers</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{total_promotions_transfers}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-label'>Average Tenure</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{avg_tenure:.1f} yrs</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-label'>Promotion Rate</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{promotion_rate:.1f}%</div>", unsafe_allow_html=True)

    # Promotion & Transfer Tracking
    st.markdown("#### Promotion & Transfer Tracking") 

    # Summary by year (active employees only)
    promo_summary = (
        df_raw[df_raw["Resignee Checking"] == "ACTIVE"]
        .groupby("Year", as_index=False)["Promotion & Transfer"].sum()
    )

    # Two charts side by side
    col1, col2 = st.columns(2)

    with col1:
        # Line chart for yearly trend
        st.markdown("##### Promotions & Transfers per Year")
        fig1 = px.line(
            promo_summary,
            x="Year",
            y="Promotion & Transfer",
            markers=True
        )
        fig1.update_traces(line=dict(width=3, color="#00008B"), marker=dict(size=8, color="#00008B"))
        fig1.update_layout(
            height=250, margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(title="Count", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            xaxis=dict(title="Year", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            font=dict(color="var(--text-color)")
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Stacked bar chart for position/level distribution
        st.markdown("##### By Position/Level")
        pos_summary = (
            df_raw[df_raw["Resignee Checking"] == "ACTIVE"]
            .groupby(["Year", "Position/Level"], as_index=False)["Promotion & Transfer"].sum()
        )
        fig2 = px.bar(
            pos_summary,
            x="Year",
            y="Promotion & Transfer",
            color="Position/Level",
            color_discrete_map={"Associate": "#ADD8E6", "Manager & Up": "#00008B"}
        )
        fig2.update_layout(
            height=250, margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(title="Count", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            xaxis=dict(title="Year", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            font=dict(color="var(--text-color)"),
            legend=dict(font=dict(color="var(--text-color)"))
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Tenure Distribution of Promoted Employees
    st.markdown(f"#### Tenure Distribution of Promoted Employees ({selected_year})")
    promoted_employees = career_year[career_year["Promotion & Transfer"] == 1]

    if not promoted_employees.empty:
        total_promoted = len(promoted_employees)
        fig3 = px.histogram(
            promoted_employees,
            x="Tenure",
            nbins=10,
            histnorm=None,
            color_discrete_sequence=["#00008B"]
        )
        # Add count + percentage labels
        fig3.update_traces(
            texttemplate="%{y}",
            textposition="outside"
        )
        fig3.update_layout(
            height=250, margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(title="Count", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            xaxis=dict(title="Tenure (years)", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            font=dict(color="var(--text-color)"),
            showlegend=False
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No promoted employees found for the selected year.")
