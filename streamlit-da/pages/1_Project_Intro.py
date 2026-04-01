import streamlit as st

st.set_page_config(page_title="Samsung Sales Dashboard", layout="wide")

st.title("📊 Samsung Global Sales Data Analysis Dashboard")

st.markdown("### Interactive Data Visualization Project")

st.divider()

# Introduction
st.header("📌 Introduction")

st.write("""
This project analyzes Samsung global sales data to understand product performance,
revenue trends, and customer purchasing behavior. The dashboard uses interactive
visualizations to present insights from the dataset.
""")

# Overview
st.header("📊 Project Overview")

st.write("""
This dashboard allows users to explore:

- Sales performance by product
- Revenue trends over different years
- Top performing countries
- Customer purchase behavior
""")

# Objectives
st.header("🎯 Project Objectives")

st.markdown("""
- Analyze global Samsung product sales
- Identify top-performing products
- Understand revenue distribution by country
- Study yearly sales trends
- Provide business insights using visual analytics
""")

# Technologies
st.header("🛠 Technologies & Libraries")

st.markdown("""
- Python
- Streamlit
- Plotly Express
- Pandas
- NumPy
""")