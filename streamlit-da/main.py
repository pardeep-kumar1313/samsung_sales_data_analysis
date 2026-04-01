import streamlit as st

st.set_page_config(
    page_title="Samsung Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Sidebar
st.sidebar.title("📊 Dashboard Navigation")

# Page Title
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image
df = pd.read_csv("samsung_global_sales_dataset.csv")
img = Image.open("samsung.png")

# Resize (width, height)
img = img.resize((1700, 500))  

st.image(img)
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${df['revenue_usd'].sum():,.0f}")
col2.metric("Total Sales", df["units_sold"].sum())
col3.metric("Avg Rating", round(df["customer_rating"].mean(), 2))

st.subheader("📄 Dataset Preview")
st.dataframe(df.head(10))


