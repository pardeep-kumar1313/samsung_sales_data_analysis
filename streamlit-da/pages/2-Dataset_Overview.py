import streamlit as st
import pandas as pd

st.title("📊 Dataset Overview & Data Preparation")

st.divider()

df = pd.read_csv("samsung_global_sales_dataset.csv")

st.header("📁 Dataset Overview")

st.write("""
This dataset contains global sales information for Samsung products.
It includes product details, sales volume, revenue, customer demographics,
and purchasing behavior across different countries.
""")

rows, cols = df.shape

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Rows", rows)

with col2:
    st.metric("Total Columns", cols)

st.divider()    

st.header("📑 Dataset Columns Explanation")

columns_info = pd.DataFrame({
    "Column Name": [
        "product_name",
        "category",
        "country",
        "units_sold",
        "revenue_usd",
        "customer_age_group",
        "payment_method",
        "discount_pct"
    ],
    "Description": [
        "Name of Samsung product",
        "Product category",
        "Country where product was sold",
        "Total number of units sold",
        "Total revenue generated",
        "Customer age group",
        "Payment method used",
        "Discount applied on product"
    ],
    "Data Type": [
        "String",
        "Category",
        "Category",
        "Integer",
        "Float",
        "Category",
        "Category",
        "Float"
    ],
    "Example": [
        "Galaxy S23",
        "Mobile",
        "India",
        "120",
        "250000.50",
        "26-35",
        "UPI",
        "10.5"
    ],
    "Use Case": [
        "Identify product trends",
        "Category-wise analysis",
        "Country-wise sales analysis",
        "Sales volume analysis",
        "Revenue analysis",
        "Customer segmentation",
        "Payment behavior analysis",
        "Discount impact analysis"
    ]
})

st.dataframe(columns_info)   
st.divider() 

st.header("🔍 Raw Dataset Preview")

st.dataframe(df)
st.divider()

st.header("📊 Missing Values Check")

null_values = df.isnull().sum()
null_values = null_values[null_values > 0]
st.dataframe(null_values)
st.divider()

st.subheader("🛠 Handling Missing Values in Storage Column")
null_values = df.isnull().sum()
null_values = null_values[null_values > 0]
st.dataframe(null_values)

st.write("Filled missing values in 'Storage' column using mode with fillna() method.")
st.write("""
df.fillna({"storage":df["storage"].mode()[0]}, inplace=True)
""")
df.fillna({"storage":df["storage"].mode()[0]}, inplace=True)
null_values = df.isnull().sum()
null_values = null_values[null_values > 0]
st.dataframe(null_values)
st.divider()


st.subheader("🛠 Handling Missing Values in previous_device_os Column")
null_values = df.isnull().sum()
null_values = null_values[null_values > 0]
st.dataframe(null_values)
st.write("Filled missing values in 'previous_device_os' column using mode with fillna() method.")
st.write("""
df.fillna({"previous_device_os":df["previous_device_os"].mode()[0]}, inplace=True)
""")
df.fillna({"previous_device_os":df["previous_device_os"].mode()[0]}, inplace=True)
null_values = df.isnull().sum()
null_values = null_values[null_values > 0]
st.dataframe(null_values)
st.divider()

st.subheader("🛠 Handling Missing Values in customer_rating Column")
null_values = df.isnull().sum()
null_values = null_values[null_values > 0]
st.dataframe(null_values)
st.write("Filled missing values in 'customer_rating' column using mode with fillna() method.")
st.write("""
df.fillna({"customer_rating":df["customer_rating"].mode()[0]}, inplace=True)
""")
df.fillna({"customer_rating":df["customer_rating"].median()}, inplace=True)
null_values = df.isnull().sum()
null_values = null_values[null_values > 0]
st.dataframe(null_values)

"""Data Pre-Processing Section"""
st.subheader("🧹 Steps Performed During Data Cleaning")

st.markdown("""
- Identified missing values in the dataset.
- Filled the missing values to maintain data consistency.
- Verified that the dataset no longer contains null values.
- Prepared the cleaned dataset for further analysis and visualization.
""")

