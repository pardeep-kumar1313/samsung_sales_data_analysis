import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.title("📊 Samsung sales analysis")
st.title("10 products by sales")

df = pd.read_csv("samsung_global_sales_dataset.csv")
df.fillna({"storage":df["storage"].mode()[0]}, inplace=True)
df.fillna({"previous_device_os":df["previous_device_os"].mode()[0]}, inplace=True)
df.fillna({"customer_rating":df["customer_rating"].median()}, inplace=True)
top_products = (
    df.groupby("product_name")["units_sold"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .index
)

df_top = df[df["product_name"].isin(top_products)]

df_price = (
    df_top.groupby(["product_name", "year"])["unit_price_usd"]
    .mean()
    .reset_index()
)

fig = px.bar(
    df_price,
    x="unit_price_usd",
    y="product_name",
    color="year",
    orientation="h",
    barmode="group",
    title="Average Unit Price by Product (Top 10 Products, Year-wise)"
)

st.plotly_chart(fig, use_container_width=True)


st.write("""
**Insights**
- The chart shows how different payment methods contribute to product sales.
- Certain payment methods generate higher units sold for specific products.

**Business Decision**
- Businesses can promote popular payment methods, offer payment-based discounts,
  and optimize the checkout process to increase conversions.
""")

st.title("Distribution of Units Sold by Product Category")
fig = px.pie(
    df,
    names='category',
    values='units_sold'
)

st.plotly_chart(fig)
st.write("""
**Insight:**  
This chart shows how total units sold are distributed across product categories. 
Some categories contribute a larger share of total sales.

**Business Decision:**  
- Focus marketing and product development on high-demand categories.  
- Maintain strong inventory for top-selling categories.  
- Analyze and improve categories with lower sales.
""")

st.title("Revenue by Category and Product")
fig = px.treemap(
    df,
    path=['category', 'product_name'],
    values='revenue_usd',
    title='Revenue by Category and Product'
)

st.plotly_chart(fig)
st.write("""
**Insight:**  
This treemap highlights how revenue is distributed across categories and individual products.

**Business Decision:**  
- Focus marketing on high-revenue products  
- Maintain inventory for top-performing categories  
- Improve strategy for products generating lower revenue
""")

fig = px.box(df, y="revenue_usd", title="Check Outliers in Revenue")
Q1 = df["revenue_usd"].quantile(0.25)
Q3 = df["revenue_usd"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
df_clean = df[(df["revenue_usd"] >= lower) & (df["revenue_usd"] <= upper)]
top_products = (
    df_clean["product_name"]
    .value_counts()
    .head(10)
    .index
)

df_top = df_clean[df_clean["product_name"].isin(top_products)]
fig = px.histogram(
    df_top,
    x="customer_age_group",
    color="product_name",
    barmode="group",
    title="Top 10 Products Purchased by Age Group"
)

st.plotly_chart(fig)

st.write("""
**Insights:**
- The chart highlights purchasing patterns of the top 10 products across different customer age groups.
- Some products are more popular among specific age segments.

**Business Decision:**
- Businesses can use this information to target marketing campaigns and optimize product inventory for different age groups.
""")

country_data = (
    df.groupby("country")
    .agg({
        "revenue_usd": "sum",
        "units_sold": "sum",
        "customer_rating": "mean",
        "payment_method": lambda x: x.mode()[0]
    })
    .reset_index()
)

fig = px.choropleth(
    country_data,
    locations="country",
    locationmode="country names",
    color="revenue_usd",
    hover_data={
        "units_sold": True,
        "customer_rating": ":.2f",
        "payment_method": True
    },
    color_continuous_scale="Viridis",
    title="Samsung Global Sales by Country"
)

fig.update_layout(
    height=600
)

st.plotly_chart(fig)
st.write("""
**Insights**
- The map highlights countries generating the highest Samsung product revenue.
- It also shows sales volume and average customer ratings for each country.

**Business Decision**
- Companies can focus marketing and distribution strategies on high-performing regions
  while expanding into emerging markets with positive customer feedback.
""")

top10_country = (
    df.groupby("country")["units_sold"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
)

filtered_df = df[df["country"].isin(top10_country)]

year_country = (
    filtered_df.groupby(["year", "country"])["units_sold"]
    .sum()
    .reset_index()
)

fig = px.line(
    year_country,
    x="year",
    y="units_sold",
    color="country",
    markers=True,
    title="Samsung Units Sold Trend by Year (Top 5 Countries)"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Units Sold",
    height=600
)

st.plotly_chart(fig)
st.write("""
**Insights**
- The chart shows yearly sales trends for Samsung products in the top 5 countries.
- It helps identify markets with growing or declining demand.

**Business Decision**
- Businesses can focus marketing efforts on high-growth countries
  and analyze declining markets to improve sales performance.
""")

country_sales = (
    df.groupby("country")["units_sold"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig = px.funnel(
    country_sales,
    x="units_sold",
    y="country",
    title="Top 5 Countries by Samsung Units Sold"
)

st.plotly_chart(fig)
st.write("""
**Insights**
- The funnel chart shows the countries contributing the highest Samsung product sales.
- It highlights the difference in sales volume between the top markets.

**Business Decision**
- Businesses should focus marketing, inventory, and sales strategies
  on high-performing countries while improving engagement in lower-ranked markets.
""")

fig = px.box(df, y="revenue_usd", title="Check Outliers in Revenue")
Q1 = df["revenue_usd"].quantile(0.25)
Q3 = df["revenue_usd"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
df_clean = df[(df["revenue_usd"] >= lower) & (df["revenue_usd"] <= upper)]
df_scatter = (
    df_clean.groupby("product_name")
    .agg({
        "revenue_usd": "sum",
        "units_sold": "sum"
    })
    .reset_index()
)
top_products = (
    df_scatter.sort_values("revenue_usd", ascending=False)
    .head(15)
)

df_scatter = df_scatter[df_scatter["product_name"].isin(top_products["product_name"])]
fig = px.scatter(
    df_scatter,
    x="units_sold",
    y="revenue_usd",
    color="product_name",
    size="revenue_usd",
    title="Revenue vs Units Sold (Top Products Only)",
)

st.plotly_chart(fig)

st.write("""
**Insights**
- The scatter plot highlights the relationship between units sold and revenue for top-performing products.
- A clear upward trend indicates that higher sales volume generally leads to higher revenue.
- Some products generate high revenue despite lower sales, suggesting premium pricing.
- A few products sell in high volume but contribute relatively less revenue, indicating lower pricing or discounts.
- Low-performing products are visible with both low sales and low revenue.

**Business Decision**
- Businesses should prioritize top-performing products by increasing marketing efforts and ensuring availability.
- Premium products should be positioned for high-value customers without heavy discounting.
- Pricing strategies for high-volume products should be optimized to improve revenue.
- Underperforming products should be re-evaluated, improved, or removed from the portfolio.
""")

top_channel = df["sales_channel"].value_counts().head(3).index

df_top = df[df["sales_channel"].isin(top_channel)]

fig = px.box(
    df_top,
    x="sales_channel",
    y="unit_price_usd",
    color="sales_channel",
    points="outliers",  
    title="Unit Price Distribution (With Outliers)"
)

st.plotly_chart(fig, key="box_with_outliers")

st.write("""
**Insights**
- The box plot shows how customer ratings are distributed across the top 5 revenue-generating categories.
- Some categories have a higher median rating, indicating better overall customer satisfaction.
- Categories with a wide spread (large box or long whiskers) show inconsistent customer experiences.
- Presence of outliers suggests that some products receive extremely high or low ratings.
- Categories with tightly grouped ratings indicate consistent product quality and customer experience.

**Business Decision**
- Focus on high-rated categories to strengthen brand reputation and customer loyalty.
- Investigate categories with low median ratings to identify quality or service issues.
- Improve consistency in categories with high variation by standardizing product quality.
- Analyze outliers to understand what drives very positive or negative customer feedback.
- Use customer feedback insights to enhance products and improve overall satisfaction.
""")

fig = px.box(df, y="unit_price_usd", title="Check Outliers in Revenue")
Q1 = df["unit_price_usd"].quantile(0.25)
Q3 = df["unit_price_usd"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
df_clean = df[(df["unit_price_usd"] >= lower) & (df["unit_price_usd"] <= upper)]

top_channel = df_clean["sales_channel"].value_counts().head(3).index
df_top = df[df["sales_channel"].isin(top_channel)]
fig = px.violin(
    df_top,
    x="sales_channel",
    y="unit_price_usd",
    color="sales_channel",
    box=True,        
    points="outliers",
    title="Price Distribution Across Sales Channels"
)

st.plotly_chart(fig)

st.write("""
**Insights**
- The violin plot shows the distribution of product prices across the top 3 sales channels.
- Some channels have a higher median price, indicating they sell more premium-priced products.
- Wide distributions suggest a mix of both low and high-priced products within the same channel.
- Narrow distributions indicate consistent pricing strategies within a channel.
- Presence of outliers shows that certain channels occasionally sell extremely high or low-priced products.

**Business Decision**
- Focus premium product strategies on channels with higher median prices to maximize revenue.
- Standardize pricing in channels with high variation to maintain consistency and customer trust.
- Leverage channels with balanced price distribution to target a wider customer base.
- Investigate outliers to identify opportunities for premium positioning or pricing corrections.
- Align sales channel strategy with product pricing to optimize overall profitability.
""")

fig = px.box(df, y="units_sold", title="Check Outliers in Revenue")
Q1 = df["units_sold"].quantile(0.25)
Q3 = df["units_sold"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
df_clean = df[(df["units_sold"] >= lower) & (df["units_sold"] <= upper)]
payment_trend = (
    df_clean.groupby(["year", "payment_method"])
    .agg({
        "units_sold": "sum",
        "revenue_usd": "sum"
    })
    .reset_index()
)

payment_trend["avg_price"] = (
    payment_trend["revenue_usd"] / payment_trend["units_sold"]
)
fig = px.area(
    payment_trend,
    x="year",
    y="units_sold",
    color="payment_method",
    line_group="payment_method",
    hover_data={
        "revenue_usd": True,
        "avg_price": ":.2f",
        "units_sold": True
    },
    title="Payment Method Usage Trend (Units + Revenue + Avg Price)"
)

st.plotly_chart(fig)
st.write("""
**Insights**
- The area chart shows how different payment methods have contributed to total units sold over time.
- Some payment methods show consistent growth, indicating increasing customer preference.
- A few methods may dominate the chart, contributing the largest share of sales.
- Fluctuations in certain payment methods suggest changing customer behavior or seasonal trends.
- The hover data reveals that some payment methods generate higher revenue per unit (higher avg_price), indicating premium transactions.

**Business Decision**
- Focus on promoting the most preferred payment methods to enhance customer convenience and sales.
- Strengthen partnerships or offers (cashbacks/discounts) on growing payment methods to accelerate adoption.
- Optimize pricing or upselling strategies for payment methods with higher average price.
- Analyze declining or fluctuating payment methods and improve user experience or incentives.
- Align marketing campaigns with popular payment trends to maximize conversions and revenue.
""")

df_clean = (
    df_top.groupby("product_name", as_index=False)
          .agg({"unit_price_usd": "mean", "units_sold": "sum"})
)

df_clean = df_clean.dropna(subset=["unit_price_usd", "units_sold"])
df_clean = df_clean[df_clean["units_sold"] > 0]
fig = px.scatter(
    df_clean,
    x="unit_price_usd",
    y="units_sold",
    color="product_name", 
    size="units_sold",
    size_max=10, 
    hover_data=["product_name"],  
    title="Units Sold vs Unit Price (Top 10 Products)"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Unit Price (USD)",
    yaxis_title="Units Sold",
    legend_title="Product Name",
)

st.plotly_chart(fig, use_container_width=True)
st.write("""
**Insights**
- The scatter plot shows a strong positive relationship between units sold and revenue.
- The presence of a trendline (OLS) confirms that revenue increases as sales volume increases.
- Most data points are clustered along the trendline, indicating consistent pricing across products.
- Some points deviate from the trendline, suggesting variations in pricing or special product categories.
- Higher units sold generally lead to higher revenue, but the slope indicates how efficiently sales convert into revenue.

**Business Decision**
- Focus on increasing sales volume to drive overall revenue growth.
- Maintain consistent pricing strategies, as the current model shows stable performance.
- Investigate outliers to identify opportunities for premium pricing or pricing corrections.
- Optimize marketing efforts to boost demand for products that align well with the trendline.
- Use the trendline insight to forecast revenue based on expected sales volume.
""")

fig = px.box(df, y="revenue_usd", title="Check Outliers in Revenue")

Q1 = df["revenue_usd"].quantile(0.25)
Q3 = df["revenue_usd"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

df_clean = df[
    (df["revenue_usd"] >= lower) &
    (df["revenue_usd"] <= upper)
]

top_products = (
    df_clean["product_name"]
    .value_counts()
    .head(10)
    .index
)

df_clean = df_clean[df_clean["product_name"].isin(top_products)]

df_3d = (
    df_clean.groupby("product_name")
    .agg({
        "units_sold": "sum",
        "revenue_usd": "sum",
        "discount_pct": "mean"
    })
    .reset_index()
)

fig = px.scatter_3d(
    df_3d,
    x="units_sold",
    y="revenue_usd",
    z="discount_pct",
    color="product_name",
    size="revenue_usd",
    hover_data=["product_name", "discount_pct"],
    title="3D Scatter: Units vs Revenue vs Discount"
)

st.plotly_chart(fig)
st.write("""
**Insights**
- The 3D scatter plot shows the relationship between units sold, revenue, and average discount across products.
- Products with high units sold and high revenue but low discount indicate strong natural demand without heavy promotions.
- Some products achieve high sales only with higher discounts, suggesting price-sensitive demand.
- A few products have high discounts but still low sales and revenue, indicating ineffective promotional strategies.
- Products positioned with moderate discounts and good revenue show a balanced pricing and sales strategy.

**Business Decision**
- Focus on promoting products that perform well without heavy discounts to maximize profit margins.
- Optimize discount strategies for price-sensitive products to improve sales without over-discounting.
- Re-evaluate products that require high discounts but still underperform and consider repositioning or discontinuation.
- Use targeted discounts instead of blanket offers to maintain profitability.
- Develop a balanced pricing strategy where discounts are used strategically to boost demand while protecting revenue.
""")

selected_country = st.selectbox(
    "Select Country",
    ["All"] + sorted(df["country"].unique().tolist())
)

selected_year = st.selectbox(
    "Select Year",
    ["All"] + sorted(df["year"].unique().tolist())
)

filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["country"] == selected_country]

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["year"] == selected_year]


country_data = (
    filtered_df.groupby("country")
    .agg({
        "revenue_usd": "sum",
        "units_sold": "sum",
        "customer_rating": "mean",
        "payment_method": lambda x: x.mode()[0] if not x.mode().empty else None
    })
    .reset_index()
)


fig = px.choropleth(
    country_data,
    locations="country",
    locationmode="country names",
    color="revenue_usd",
    hover_data={
        "units_sold": True,
        "customer_rating": ":.2f",
        "payment_method": True
    },
    color_continuous_scale="Viridis",
    title=f"Samsung Sales Map ({selected_country}, {selected_year})"
)

fig.update_layout(height=600)
fig.update_geos(fitbounds="locations", visible=False)

st.plotly_chart(fig, key="chart_1")

