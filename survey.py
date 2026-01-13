import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def render(df, df_raw, selected_year):
    st.markdown("## 📊 Survey & Feedback Analytics")

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

    st.markdown("<div class='metric-label'>Survey Participation Rate</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{participation_rate:.1f}%</div>", unsafe_allow_html=True)

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
    st.markdown(f"#### Engagement Ratings Breakdown ({selected_year})")

    # Standardized blue color palette
    rating_colors = {
        "Outstanding": "#ADD8E6",
        "Average": "#00008B",
        "Needs Improvement": "#87CEEB"
    }

    fig_stacked = go.Figure()

    for rating in ["Outstanding", "Average", "Needs Improvement"]:
        fig_stacked.add_trace(go.Bar(
            y=pivot_df.index,
            x=pivot_df[rating],
            name=rating,
            orientation="h",
            marker_color=rating_colors[rating],
            text=pivot_df[rating].round(0).astype(str) + "%",
            textposition="inside"
        ))

    row_count = len(pivot_df.index)
    chart_height = max(300, 40 * row_count)

    fig_stacked.update_layout(
        barmode="stack",
        xaxis=dict(title="Percentage", ticksuffix="%", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
        yaxis=dict(title="Dimensions", automargin=True, tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
        height=chart_height,
        margin=dict(l=20, r=100, t=20, b=80),
        legend_title="Rating Type",
        font=dict(color="var(--text-color)"),
        legend=dict(font=dict(color="var(--text-color)"))
    )

    st.plotly_chart(fig_stacked, use_container_width=True)

    # -----------------------------
    # Driver Analysis - Combined Row
    # -----------------------------
    st.markdown("#### Driver Analysis")
    
    # Create two columns for resignation and promotion analysis
    analysis_col1, analysis_col2 = st.columns(2)
    
    # -----------------------------
    # LEFT COLUMN: Driver Analysis by Resignation
    # -----------------------------
    with analysis_col1:
        st.markdown("##### By Resignation")
        
        # Prepare data
        df_analysis = df_raw.copy()
        
        # Create binary resignation flag
        df_analysis["Resigned"] = df_analysis["Resignee Checking"].apply(
            lambda x: 0 if str(x).strip().upper() == "ACTIVE" else 1
        )
        
        # Select features for analysis
        features = ["Tenure", "Position/Level", "Generation", "Gender", "Promotion & Transfer"]
        
        # Encode categorical variables
        le = LabelEncoder()
        df_encoded = df_analysis[features + ["Resigned"]].copy()
        
        for col in ["Position/Level", "Generation", "Gender"]:
            if col in df_encoded.columns:
                df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
        
        # Remove NaN values
        df_encoded = df_encoded.dropna()
        
        X = df_encoded[features]
        y = df_encoded["Resigned"]
        
        # Train Random Forest to get feature importance
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X, y)
        
        # Get feature importance
        importance_df = pd.DataFrame({
            "Driver": features,
            "Importance": rf.feature_importances_
        }).sort_values("Importance", ascending=False)
        
        importance_df["Importance %"] = (importance_df["Importance"] * 100).round(1)
        
        # Display metrics
        st.markdown(f"<div class='metric-label'>Top Driver: {importance_df.iloc[0]['Driver']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{importance_df.iloc[0]['Importance %']}%</div>", unsafe_allow_html=True)
        
        # Driver Importance Chart
        fig = go.Figure(data=go.Bar(
            x=importance_df["Importance %"],
            y=importance_df["Driver"],
            orientation="h",
            marker_color="#00008B",
            text=importance_df["Importance %"].apply(lambda x: f"{x}%"),
            textposition="outside"
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(title="Importance (%)", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            yaxis=dict(title="", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            font=dict(color="var(--text-color)"),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation Chart
        corr_matrix = df_encoded[features + ["Resigned"]].corr()["Resigned"].drop("Resigned").sort_values(ascending=False)
        
        fig_corr = go.Figure(data=go.Bar(
            x=corr_matrix.values,
            y=corr_matrix.index,
            orientation="h",
            marker_color=["#00008B" if x > 0 else "#B22222" for x in corr_matrix.values],
            text=[f"{x:.3f}" for x in corr_matrix.values],
            textposition="outside"
        ))
        
        fig_corr.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(title="Correlation", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            yaxis=dict(title="", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            font=dict(color="var(--text-color)")
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)

    # -----------------------------
    # RIGHT COLUMN: Driver Analysis by Promotion
    # -----------------------------
    with analysis_col2:
        st.markdown("##### By Promotion")
        
        # Prepare data for promotion analysis
        df_promo = df_raw[df_raw["Resignee Checking"].str.strip().str.upper() == "ACTIVE"].copy()
        
        # Create binary promotion flag
        def to_promo_flag(x):
            s = str(x).strip().upper()
            if s in {"1", "YES", "TRUE"}:
                return 1
            return 0
        
        df_promo["Promoted"] = df_promo["Promotion & Transfer"].apply(to_promo_flag)
        
        # Select features for promotion analysis
        promo_features = ["Tenure", "Position/Level", "Generation", "Gender"]
        
        # Encode categorical variables
        le_promo = LabelEncoder()
        df_promo_encoded = df_promo[promo_features + ["Promoted"]].copy()
        
        for col in ["Position/Level", "Generation", "Gender"]:
            if col in df_promo_encoded.columns:
                df_promo_encoded[col] = le_promo.fit_transform(df_promo_encoded[col].astype(str))
        
        # Remove NaN values
        df_promo_encoded = df_promo_encoded.dropna()
        
        X_promo = df_promo_encoded[promo_features]
        y_promo = df_promo_encoded["Promoted"]
        
        # Train Random Forest to get feature importance
        rf_promo = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_promo.fit(X_promo, y_promo)
        
        # Get feature importance
        importance_promo_df = pd.DataFrame({
            "Driver": promo_features,
            "Importance": rf_promo.feature_importances_
        }).sort_values("Importance", ascending=False)
        
        importance_promo_df["Importance %"] = (importance_promo_df["Importance"] * 100).round(1)
        
        # Display metrics
        st.markdown(f"<div class='metric-label'>Top Driver: {importance_promo_df.iloc[0]['Driver']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{importance_promo_df.iloc[0]['Importance %']}%</div>", unsafe_allow_html=True)
        
        # Driver Importance Chart
        fig_promo = go.Figure(data=go.Bar(
            x=importance_promo_df["Importance %"],
            y=importance_promo_df["Driver"],
            orientation="h",
            marker_color="#2E8B57",
            text=importance_promo_df["Importance %"].apply(lambda x: f"{x}%"),
            textposition="outside"
        ))
        
        fig_promo.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(title="Importance (%)", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            yaxis=dict(title="", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            font=dict(color="var(--text-color)"),
            showlegend=False
        )
        
        st.plotly_chart(fig_promo, use_container_width=True)
        
        # Correlation Chart
        corr_promo_matrix = df_promo_encoded[promo_features + ["Promoted"]].corr()["Promoted"].drop("Promoted").sort_values(ascending=False)
        
        fig_corr_promo = go.Figure(data=go.Bar(
            x=corr_promo_matrix.values,
            y=corr_promo_matrix.index,
            orientation="h",
            marker_color=["#2E8B57" if x > 0 else "#B22222" for x in corr_promo_matrix.values],
            text=[f"{x:.3f}" for x in corr_promo_matrix.values],
            textposition="outside"
        ))
        
        fig_corr_promo.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(title="Correlation", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            yaxis=dict(title="", tickfont=dict(color="var(--text-color)"), titlefont=dict(color="var(--text-color)")),
            font=dict(color="var(--text-color)")
        )
        
        st.plotly_chart(fig_corr_promo, use_container_width=True)
