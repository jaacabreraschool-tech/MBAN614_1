import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render(df, df_raw, selected_year):
    st.subheader("Survey & Feedback Analytics")

    # -----------------------------
    # Load survey datasets
    # -----------------------------
    df_engagement = pd.read_excel("Emp Engagement.xlsx", sheet_name="Sheet1")
    df_participation = pd.read_excel("Participation.xlsx", sheet_name="Sheet1")

    # Clean up column names
    df_engagement.columns = df_engagement.columns.str.strip()
    df_participation.columns = df_participation.columns.str.strip()

    # Normalize Calendar Year
    df_engagement["Calendar Year"] = pd.to_datetime(df_engagement["Calendar Year"], errors="coerce")
    df_engagement["Year"] = df_engagement["Calendar Year"].dt.year

    df_participation["Calendar Year"] = pd.to_datetime(df_participation["Calendar Year"], errors="coerce")
    df_participation["Year"] = df_participation["Calendar Year"].dt.year

    # -----------------------------
    # Filter by selected year
    # -----------------------------
    engagement_year = df_engagement[df_engagement["Year"] == int(selected_year)]
    participation_year = df_participation[df_participation["Year"] == int(selected_year)]

    # -----------------------------
    # Top metrics row
    # -----------------------------
    if not participation_year.empty:
        participation_rate = participation_year["Participation Rate"].iloc[0] * 100
    else:
        participation_rate = 0

    col1, col2 = st.columns(2)
    col1.metric("Survey Participation Rate", f"{participation_rate:.1f}%")
    col2.metric("Number of Engagement Dimensions", len(engagement_year))

    # -----------------------------
    # Prepare data for stacked chart
    # -----------------------------
    df_long = df_engagement.melt(
        id_vars=["Dimensions", "Year"],
        value_vars=["Outstanding", "Average", "Needs Improvement"],
        var_name="Rating Type",
        value_name="Score"
    )
    df_long["Score %"] = df_long["Score"] * 100
    df_long_year = df_long[df_long["Year"] == int(selected_year)]

    pivot_df = df_long_year.pivot(index="Dimensions", columns="Rating Type", values="Score %").fillna(0)

    # -----------------------------
    # Stacked Bar Chart
    # -----------------------------
    st.markdown("## Engagement Ratings Breakdown")

    fig_stacked = go.Figure()

    for rating, color in zip(["Outstanding", "Average", "Needs Improvement"], ["#ADD8E6", "#1f77b4", "#ff7f0e"]):
        fig_stacked.add_trace(go.Bar(
            y=pivot_df.index,
            x=pivot_df[rating],
            name=rating,
            orientation="h",
            marker_color=color,
            text=pivot_df[rating].round(0).astype(str) + "%",
            textposition="inside"
        ))

    row_count = len(pivot_df.index)
    chart_height = max(300, 40 * row_count)

    fig_stacked.update_layout(
        barmode="stack",
        title=f"Engagement Ratings – {selected_year}",
        xaxis=dict(title="Percentage", ticksuffix="%"),
        yaxis=dict(title="Dimensions", automargin=True),
        height=chart_height,
        margin=dict(l=20, r=100, t=80, b=80),
        legend_title="Rating Type"
    )

    st.plotly_chart(fig_stacked, use_container_width=True)
