#st.subheader("Proyek Analisis Data: [E-Commerce Public Dataset]")
#st.write("Nama : [Nabila Risqi Rosyadi]")
#st.write("Email : [mc006d5x1344@gmail.com]")
#st.write("ID Dicoding : [Nabila Risqi Rosyadi]")

#st.subheader("Menentukan Pertanyaan Bisnis")
#st.write (f"Bagaimana dsitribusi pelanggan berdasarkan lokasi geografis, dan apakah ada pola tertentu dalam transaksi berdasarkan wilayah?")
#st.write (f"Bagaimana pengaruh ulasan pelanggan terhadap metode pembayaran dan jumlah pembelian?")


#Import Semua Packages/Library yang Digunakan")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import zipfile

# Judul Dashboard
st.title("📊 Dashboard Analisis Data E-Commerce")

st.subheader("Data Wrangling")
st.write("Gathering Data")

# Load dataset dari GitHub
@st.cache_data
def load_data():
    customers_df = pd.read_csv("https://raw.githubusercontent.com/nabilarisqi00/streamlit1/main/E-commerce-public-dataset/E-Commerce%20Public%20Dataset/customers_dataset.csv")
    orders_df = pd.read_csv("https://raw.githubusercontent.com/nabilarisqi00/streamlit1/main/E-commerce-public-dataset/E-Commerce%20Public%20Dataset/orders_dataset.csv")
    payments_df = pd.read_csv("https://raw.githubusercontent.com/nabilarisqi00/streamlit1/main/E-commerce-public-dataset/E-Commerce%20Public%20Dataset/order_payments_dataset.csv")
    reviews_df = pd.read_csv("https://raw.githubusercontent.com/nabilarisqi00/streamlit1/main/E-commerce-public-dataset/E-Commerce%20Public%20Dataset/order_reviews_dataset.csv")
    order_items_df = pd.read_csv("https://raw.githubusercontent.com/nabilarisqi00/streamlit1/main/E-commerce-public-dataset/E-Commerce%20Public%20Dataset/order_items_dataset.csv")
    geolocation_df = pd.read_csv("https://raw.githubusercontent.com/nabilarisqi00/streamlit1/main/E-commerce-public-dataset/E-Commerce%20Public%20Dataset/geolocation_dataset.zip")
    return customers_df, orders_df, payments_df, reviews_df, order_items_df, geolocation_df

customers_df, orders_df, payments_df, reviews_df, order_items_df, geolocation_df = load_data()

# Informasi dasar dataset
st.subheader("Informasi Dataset Pelanggan")
st.write(customers_df.describe(include='all'))

# Agregasi jumlah pelanggan berdasarkan negara bagian
customer_state_counts = customers_df.groupby("customer_state")["customer_id"].nunique().reset_index()
customer_state_counts = customer_state_counts.sort_values(by='customer_id', ascending=False)
st.subheader("Distribusi Jumlah Pelanggan Berdasarkan Negara Bagian")
st.dataframe(customer_state_counts.head(10))

# Pilihan interaktif untuk eksplorasi data pelanggan berdasarkan negara bagian
selected_state = st.selectbox("Pilih Negara Bagian untuk Dieksplorasi", customer_state_counts["customer_state"].unique())
filtered_customers = customers_df[customers_df["customer_state"] == selected_state]
st.write(f"Jumlah pelanggan di {selected_state}: {filtered_customers.shape[0]}")

# Visualisasi distribusi pelanggan
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=customer_state_counts, x='customer_state', y='customer_id', palette='coolwarm', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Eksplorasi Data orders_df
orders_df["order_purchase_timestamp"] = pd.to_datetime(orders_df["order_purchase_timestamp"])
orders_df["order_delivered_customer_date"] = pd.to_datetime(orders_df["order_delivered_customer_date"])
orders_df["order_estimated_delivery_date"] = pd.to_datetime(orders_df["order_estimated_delivery_date"])
orders_df["delivery_time"] = (orders_df["order_delivered_customer_date"] - orders_df["order_purchase_timestamp"]).dt.days
st.subheader("Ringkasan Waktu Pengiriman")
st.write(orders_df[["delivery_time"]].describe())

# Gabungkan data orders_df dengan customers_df
orders_customers_df = pd.merge(orders_df, customers_df, on='customer_id', how='left')

# Agregasi jumlah order berdasarkan kota dan negara bagian
order_state_counts = orders_customers_df.groupby("customer_state")["order_id"].nunique().reset_index()
st.subheader("Jumlah Order Berdasarkan Negara Bagian")
st.dataframe(order_state_counts)

# Visualisasi jumlah order per negara bagian
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=order_state_counts, x='customer_state', y='order_id', palette='viridis', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Eksplorasi hubungan ulasan pelanggan terhadap metode pembayaran
orders_payments_reviews_df = pd.merge(orders_df, payments_df, on='order_id', how='left')
orders_payments_reviews_df = pd.merge(orders_payments_reviews_df, reviews_df, on='order_id', how='left')

# Agregasi rata-rata skor ulasan berdasarkan metode pembayaran
review_payment_agg = orders_payments_reviews_df.groupby("payment_type").agg({"review_score": "mean", "payment_value": "mean"}).reset_index()
st.subheader("Rata-rata Skor Ulasan Berdasarkan Metode Pembayaran")
st.dataframe(review_payment_agg)

# Visualisasi hubungan metode pembayaran dengan skor ulasan
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=review_payment_agg, x='payment_type', y='review_score', palette='coolwarm', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Visualisasi hubungan jumlah pembayaran dengan skor ulasan
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=orders_payments_reviews_df, x='payment_value', y='review_score', alpha=0.5, ax=ax)
st.pyplot(fig)

st.subheader("Ringkasan Statistik Pembayaran dan Ulasan")
st.write(orders_payments_reviews_df[['payment_value', 'review_score']].describe())
