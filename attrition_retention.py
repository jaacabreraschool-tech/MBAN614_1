import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render(df, df_raw, selected_year, df_attrition=None):
    st.markdown("## 📊 Attrition and Retention Overview")

    # -----------------------------
    # Ensure Retention column exists
    # -----------------------------
    def to_resigned_flag(x):
        s = str(x).strip().upper()
        return 0 if s == "ACTIVE" else 1

    if "ResignedFlag" not in df_raw.columns:
        df_raw["ResignedFlag"] = df_raw["Resignee Checking"].apply(to_resigned_flag)
    if "Retention" not in df_raw.columns:
        df_raw["Retention"] = 1 - df_raw["ResignedFlag"]

    # Normalize values
    df_raw["Gender"] = df_raw["Gender"].str.strip().str.capitalize()
    df_raw["Resignee Checking"] = df_raw["Resignee Checking"].str.strip().str.upper()

    # -----------------------------
    # Create Year column from Calendar Year
    # -----------------------------
    if "Year" not in df_raw.columns and "Calendar Year" in df_raw.columns:
        df_raw["Year"] = pd.to_datetime(df_raw["Calendar Year"]).dt.year

    # -----------------------------
    # Row 0: Summary Metrics
    # -----------------------------
    summary_year = df_raw[df_raw["Year"] == selected_year]

    total_employees = len(summary_year)
    resigned = summary_year["ResignedFlag"].sum()
    retained = summary_year["Retention"].sum()

    retention_rate = (retained / total_employees) * 100 if total_employees > 0 else 0
    attrition_rate = (resigned / total_employees) * 100 if total_employees > 0 else 0
    net_change = retained - resigned

    colA, colB, colC, colD, colE = st.columns(5)
    with colA: st.markdown("<div class='metric-label'>Total Employees</div>", unsafe_allow_html=True); st.markdown(f"<div class='metric-value'>{total_employees}</div>", unsafe_allow_html=True)
    with colB: st.markdown("<div class='metric-label'>Resigned</div>", unsafe_allow_html=True); st.markdown(f"<div class='metric-value'>{resigned}</div>", unsafe_allow_html=True)
    with colC: st.markdown("<div class='metric-label'>Retention Rate</div>", unsafe_allow_html=True); st.markdown(f"<div class='metric-value'>{retention_rate:.1f}%</div>", unsafe_allow_html=True)
    with colD: st.markdown("<div class='metric-label'>Attrition Rate</div>", unsafe_allow_html=True); st.markdown(f"<div class='metric-value'>{attrition_rate:.1f}%</div>", unsafe_allow_html=True)
    with colE: st.markdown("<div class='metric-label'>Net Change</div>", unsafe_allow_html=True); st.markdown(f"<div class='metric-value'>{net_change}</div>", unsafe_allow_html=True)

    # -----------------------------
    # Row 1: Resigned per Year
    # -----------------------------
    st.markdown("### Resigned per Year")
    resigned_per_year = df_raw.groupby("Year")["ResignedFlag"].sum().reset_index(name="Resigned")
    fig_resigned = px.bar(resigned_per_year, x="Year", y="Resigned", text="Resigned",
                          color_discrete_sequence=["#00008B"], title="Resigned Employees per Year")
    fig_resigned.update_layout(
        height=220, margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(title="Resigned Employees", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
        xaxis=dict(title="Year", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
        font=dict(color="var(--text-color)"), title_font=dict(color="var(--text-color)"),
        legend=dict(font=dict(color="var(--text-color)")),
        uniformtext_minsize=10, uniformtext_mode="hide"
    )
    st.plotly_chart(fig_resigned, use_container_width=True, key="resigned_per_year")

    # -----------------------------
    # Row 2: Retention by Gender + Retention by Generation
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Retention by Gender")
        retention_gender = df_raw.groupby(["Year", "Gender"])["Retention"].sum().reset_index()
        retention_rate = df_raw.groupby("Year")["Retention"].mean().reset_index()
        retention_rate["RetentionRatePct"] = retention_rate["Retention"] * 100
        fig = go.Figure()
        for gender in retention_gender["Gender"].unique():
            subset = retention_gender[retention_gender["Gender"] == gender]
            fig.add_bar(x=subset["Year"], y=subset["Retention"], name=gender,
                        marker_color="#ADD8E6" if gender == "Female" else "#00008B", yaxis="y1")
        fig.add_trace(go.Scatter(x=retention_rate["Year"], y=retention_rate["RetentionRatePct"],
                                 mode="lines+markers", name="Retention Rate (%)",
                                 line=dict(color="orange", width=3), yaxis="y2"))
        fig.update_layout(
            yaxis=dict(title="Retained Employees (count)", side="left",
                       tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            yaxis2=dict(title="Retention Rate (%)", overlaying="y", side="right", range=[80, 100],
                        tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            xaxis=dict(title="Year", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            font=dict(color="var(--text-color)"), title_font=dict(color="var(--text-color)"),
            legend=dict(font=dict(color="var(--text-color)")),
            barmode="group", height=220, margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True, key="retention_by_gender")

    with col2:
        st.markdown("#### Retention by Generation")
        active_df = df_raw[df_raw["Resignee Checking"] == "ACTIVE"]
        total_by_year_gen = df_raw[df_raw["Year"].between(2020, 2025)].groupby(["Year", "Generation"]).size().reset_index(name="Total")
        active_by_year_gen = active_df[active_df["Year"].between(2020, 2025)].groupby(["Year", "Generation"]).size().reset_index(name="Active")
        retention_df = pd.merge(total_by_year_gen, active_by_year_gen, on=["Year", "Generation"], how="left")
        retention_df["RetentionRate"] = (retention_df["Active"] / retention_df["Total"]) * 100
        fig_retention = px.bar(retention_df, x="Year", y="RetentionRate", color="Generation", barmode="group",
                               text=retention_df["RetentionRate"].round(1).astype(str) + "%",
                               color_discrete_sequence=["#ADD8E6", "#00008B", "#87CEEB", "#1E3A8A", "#4682B4"],
                               title="Retention by Generation (2020–2025)")
        fig_retention.update_layout(
            height=220, margin=dict(l=20, r=20, t=40, b=20),
            yaxis=dict(title="Retention Rate (%)", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            xaxis=dict(title="Year", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            font=dict(color="var(--text-color)"), title_font=dict(color="var(--text-color)"),
            legend=dict(font=dict(color="var(--text-color)")),
            uniformtext_minsize=10, uniformtext_mode="hide"
        )
        st.plotly_chart(fig_retention, use_container_width=True, key="retention_by_generation")

        # -----------------------------
    # Row 3: Attrition by Month (selected year) + Voluntary vs Involuntary (2020–2025)
    # -----------------------------
    st.markdown("### Attrition Analysis")

    col1, col2 = st.columns(2)

    # -----------------------------
    # Chart 1: Attrition by Month (selected year)
    # -----------------------------
    with col1:
        st.markdown(f"#### Attrition by Month ({selected_year})")
        attrition_selected = df_raw[(df_raw["Year"] == selected_year) & (df_raw["ResignedFlag"] == 1)].copy()

        # Ensure Month column exists
        attrition_selected["Month"] = pd.to_datetime(attrition_selected["Resignation Date"]).dt.month_name()

        monthly_attrition = (
            attrition_selected.groupby("Month")
            .size()
            .reindex([
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ])
            .reset_index(name="AttritionCount")
        )

        fig_monthly = px.bar(
            monthly_attrition,
            x="Month",
            y="AttritionCount",
            text="AttritionCount",
            color_discrete_sequence=["#00008B"],  # dark blue to match palette
            title=f"Monthly Attrition in {selected_year}"
        )

        fig_monthly.update_layout(
            height=300, margin=dict(l=20, r=20, t=40, b=20),
            yaxis=dict(title="Attrition Count",
                       tickfont=dict(color="var(--text-color)"),
                       titlefont=dict(color="var(--text-color)")),
            xaxis=dict(title="Month",
                       tickfont=dict(color="var(--text-color)"),
                       titlefont=dict(color="var(--text-color)")),
            font=dict(color="var(--text-color)"),
            title_font=dict(color="var(--text-color)"),
            legend=dict(font=dict(color="var(--text-color)")),
            uniformtext_minsize=10,
            uniformtext_mode="hide"
        )
        st.plotly_chart(fig_monthly, use_container_width=True, key="attrition_by_month")

    # -----------------------------
    # Chart 2: Voluntary vs Involuntary (2020–2025)
    # -----------------------------
    with col2:
        st.markdown("#### Attrition by Voluntary vs Involuntary (2020–2025)")

        if df_attrition is not None:
            if "Year" not in df_attrition.columns and "Calendar Year" in df_attrition.columns:
                df_attrition["Year"] = pd.to_datetime(df_attrition["Calendar Year"]).dt.year

            attrition_df = df_attrition[
                (df_attrition["Year"].between(2020, 2025)) &
                (df_attrition["Status"].isin(["Voluntary", "Involuntary"]))
            ]

            attrition_counts = (
                attrition_df.groupby(["Year", "Status"])
                .size()
                .reset_index(name="Count")
            )

            fig_attrition = px.bar(
                attrition_counts,
                x="Year",
                y="Count",
                color="Status",
                barmode="group",
                text="Count",
                color_discrete_map={
                    "Voluntary": "#ADD8E6",   # light blue
                    "Involuntary": "#00008B"  # dark blue
                },
                title="Voluntary vs Involuntary Attrition"
            )

            fig_attrition.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                yaxis=dict(title="Attrition Count",
                           tickfont=dict(color="var(--text-color)"),
                           titlefont=dict(color="var(--text-color)")),
                xaxis=dict(title="Year",
                           tickfont=dict(color="var(--text-color)"),
                           titlefont=dict(color="var(--text-color)")),
                font=dict(color="var(--text-color)"),
                title_font=dict(color="var(--text-color)"),
                legend=dict(font=dict(color="var(--text-color)")),
                uniformtext_minsize=10,
                uniformtext_mode="hide"
            )

            st.plotly_chart(fig_attrition, use_container_width=True, key="attrition_by_type")

        else:
            st.info("No Voluntary/Involuntary attrition dataset provided yet.")

               # -----------------------------
    # Row 4: Net Talent Gain/Loss
    # -----------------------------
    st.markdown("### Net Talent Gain/Loss")

    # Load Summary tab from Excel
    summary_df = pd.read_excel("HR Cleaned Data 01.09.26.xlsx", sheet_name="Summary")

    # Keep relevant columns
    net_df = summary_df[["Year", "Joins", "Resignations", "Net Change"]].copy()
    net_df.rename(columns={"Net Change": "NetChange"}, inplace=True)

    # Assign status for color coding (only Increase/Decrease)
    net_df["Status"] = net_df["NetChange"].apply(
        lambda x: "Increase" if x > 0 else "Decrease"
    )

    # Force categorical ordering for legend
    net_df["Status"] = pd.Categorical(
        net_df["Status"],
        categories=["Increase", "Decrease"],
        ordered=True
    )

    # Convert Year to string to avoid fractional values
    net_df["Year"] = net_df["Year"].astype(str)

    # Define custom colors
    color_map = {
        "Increase": "#2E8B57",     # dark green
        "Decrease": "#B22222"      # red
    }

    # Plot bar chart with Joins + Resignations in hover
    fig_net = px.bar(
        net_df,
        x="Year",
        y="NetChange",
        text=net_df["NetChange"].apply(lambda x: f"{x:+d}"),  # show +/– signs
        color="Status",
        color_discrete_map=color_map,
        hover_data={
            "Joins": True,
            "Resignations": True,
            "NetChange": True,
            "Status": True,
            "Year": True
        },
        title="Net Talent Gain/Loss by Year"
    )

    fig_net.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(title="Net Change",
                   tickfont=dict(color="var(--text-color)"),
                   titlefont=dict(color="var(--text-color)")),
        xaxis=dict(title="Year",
                   tickfont=dict(color="var(--text-color)"),
                   titlefont=dict(color="var(--text-color)")),
        font=dict(color="var(--text-color)"),
        title_font=dict(color="var(--text-color)"),
        legend=dict(font=dict(color="var(--text-color)")),
        uniformtext_minsize=10,
        uniformtext_mode="hide"
    )

    st.plotly_chart(fig_net, use_container_width=True, key="net_talent_change")
