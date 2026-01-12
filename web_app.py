import streamlit as st
import pandas as pd

# Import tab modules
# import workforce
# import attrition_retention as attrition
# import career
# import survey
# import aboutus

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="ACJ Company Dashboard", layout="wide")

# -----------------------------
# Load CSS file globally
# -----------------------------
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------
# Load Excel outputs
# -----------------------------
# Main HR analysis outputs (multi-sheet workbook)
df = pd.read_excel("HR_Analysis_Output.xlsx", sheet_name=None)

# Cleaned HR dataset
df_raw = pd.read_excel("HR Cleaned Data 01.09.26.xlsx", sheet_name="Data")

# Voluntary/Involuntary attrition dataset
df_attrition = pd.read_excel("Attrition-Vol and Invol.xlsx")

# -----------------------------
# Ensure Year column exists
# -----------------------------
if "Year" not in df_raw.columns and "Calendar Year" in df_raw.columns:
    df_raw["Year"] = pd.to_datetime(df_raw["Calendar Year"]).dt.year

if "Year" not in df_attrition.columns and "Calendar Year" in df_attrition.columns:
    df_attrition["Year"] = pd.to_datetime(df_attrition["Calendar Year"]).dt.year

# -----------------------------
# App Title
# -----------------------------
st.title("ACJ Company Dashboard")

# -----------------------------
# Year selector
# -----------------------------
years = [2020, 2021, 2022, 2023, 2024, 2025]
with st.spinner("Loading data..."):
    selected_year = st.radio("Select Year", years, horizontal=True)

# -----------------------------
# Tabs
# -----------------------------
tabs = st.tabs([
    "Workforce Profile & Demographics",
    "Attrition & Retention",
    "Career Progression",
    "Survey & Feedback Analytics",
    "About Us"
])

# -----------------------------
# Call each tab's render function
# -----------------------------
with tabs[0]:
    workforce.render(df, df_raw, selected_year)

with tabs[1]:
    # Pass df_attrition into the attrition tab
    attrition.render(df, df_raw, selected_year, df_attrition)

with tabs[2]:
    career.render(df, df_raw, selected_year)

with tabs[3]:
    survey.render(df, df_raw, selected_year)

with tabs[4]:
    aboutus.render(df, df_raw, selected_year)
