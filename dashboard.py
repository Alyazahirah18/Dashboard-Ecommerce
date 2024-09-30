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
st.title("E-commerce Dataset Dashboard")

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

# Menghitung waktu pengiriman dalam satuan (hari)
orders_df['delivery_time'] = (orders_df['order_delivered_customer_date'] - orders_df['order_purchase_timestamp']).dt.days

# Menggabungkan order dengan order review untuk menganalisis dampak waktu pengiriman pada review pelanggan
orderreview = pd.read_csv('order_reviews_dataset.csv')
merged_df = pd.merge(orders_df[['order_id', 'delivery_time']], 
                     orderreview[['order_id', 'review_score']], 
                     on='order_id', how='inner')

# Menghapus baris yang tidak memiliki nilai
merged_df = merged_df.dropna(subset=['delivery_time', 'review_score'])

# Membuat dashboard menggunakan Streamlit
st.header('pertanyaan 1: Dashboard Analisis Waktu Pengiriman dan Skor Ulasan')

# Membuat boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(x='review_score', y='delivery_time', data=merged_df)
plt.title('Delivery Time vs. Review Score')
plt.xlabel('Review Score')
plt.ylabel('Delivery Time (days)')

# Menampilkan plot di Streamlit
st.pyplot(plt)

# Delivery Time Distribution
st.subheader("Distribusi waktu pengiriman (hari)")
fig, ax = plt.subplots()
sns.histplot(filtered_data['delivery_time'].dropna(), bins=30, kde=True, ax=ax)
st.pyplot(fig)

# Delivery Time per Order Status
st.subheader("Rata-rata waktu pengiriman tiap order")
avg_delivery_time = filtered_data.groupby('order_status')['delivery_time'].mean().dropna()
st.bar_chart(avg_delivery_time)

# Menggabungkan order item dengan order review untuk analisa hubungan
orderitem = pd.read_csv("order_items_dataset.csv")
order_item_review = pd.merge(
    orderitem[['order_id', 'price', 'freight_value']], 
    orderreview[['order_id', 'review_score']], 
    on='order_id', how='inner'
)
# Membuat dashboard menggunakan Streamlit
st.header('Pertanyaan 2: Dashboard Analisis Harga, Biaya Pengiriman, dan Skor Ulasan')

# Plotting price and freight value against review score
plt.figure(figsize=(12, 6))

# Scatter plot for price vs review score
plt.subplot(1, 2, 1)
sns.scatterplot(x='price', y='review_score', data=order_item_review, alpha=0.5)
plt.title('Harga vs. Skor Review')
plt.xlabel('Harga')
plt.ylabel('Skor Review')

# Scatter plot for freight value vs review score
plt.subplot(1, 2, 2)
sns.scatterplot(x='freight_value', y='review_score', data=order_item_review, alpha=0.5)
plt.title('Biaya Pengiriman vs. Skor Review')
plt.xlabel('Biaya Pengiriman')
plt.ylabel('Skor Review')

plt.tight_layout()

# Menampilkan plot di Streamlit
st.pyplot(plt)

# Order Status Distribution
st.subheader("Status distribusi order")
fig, ax = plt.subplots()
sns.countplot(data=filtered_data, x='order_status', order=filtered_data['order_status'].value_counts().index, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Top 5 Customers with Most Orders
st.subheader("Top 5 customer berdasarkan jumlah order")
top_customers = filtered_data['customer_id'].value_counts().head(5)
st.bar_chart(top_customers)

# Footer
st.markdown("### Created with Streamlit")