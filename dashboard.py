import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache_data
def load_data():
    orders_df = pd.read_csv("orders_dataset.csv")
    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
    orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'], errors='coerce')
    orders_df['delivery_time'] = (orders_df['order_delivered_customer_date'] - orders_df['order_purchase_timestamp']).dt.days
    return orders_df

orders_df = load_data()

# Streamlit App Title
st.title("Order Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
status_filter = st.sidebar.multiselect(
    "Select Order Status",
    options=orders_df["order_status"].unique(),
    default=orders_df["order_status"].unique()
)

# Filtered data
filtered_data = orders_df[orders_df["order_status"].isin(status_filter)]

# Show raw data toggle
if st.sidebar.checkbox("Tampilkan Data Murni"):
    st.write(filtered_data)
    
# Order Status Distribution
st.subheader("Status distribusi order")
fig, ax = plt.subplots()
sns.countplot(data=filtered_data, x='order_status', order=filtered_data['order_status'].value_counts().index, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Delivery Time Distribution
st.subheader("Distribusi waktu pengiriman (hari)")
fig, ax = plt.subplots()
sns.histplot(filtered_data['delivery_time'].dropna(), bins=30, kde=True, ax=ax)
st.pyplot(fig)

# Delivery Time per Order Status
st.subheader("Rata-rata waktu pengiriman tiap order")
avg_delivery_time = filtered_data.groupby('order_status')['delivery_time'].mean().dropna()
st.bar_chart(avg_delivery_time)

# Top 5 Customers with Most Orders
st.subheader("Top 5 customer berdasarkan jumlah order")
top_customers = filtered_data['customer_id'].value_counts().head(5)
st.bar_chart(top_customers)

# Footer
st.markdown("### Created with Streamlit")