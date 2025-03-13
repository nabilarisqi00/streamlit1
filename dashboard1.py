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

# Path ke file ZIP
zip_path = "E-commerce-public-dataset/E-Commerce Public Dataset/geolocation_dataset.zip"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    with zip_ref.open('geolocation_dataset.csv') as file:
        geolocation_df = pd.read_csv(file)

geolocation_df = geolocation_df.drop(columns=['geolocation_lat', 'geolocation_lng'])

# Path ke File CSV
customers_df = pd.read_csv("E-commerce-public-dataset/E-Commerce Public Dataset/customers_dataset.csv")
review_df = pd.read_csv("E-commerce-public-dataset/E-Commerce Public Dataset/order_reviews_dataset.csv")
payment_df = pd.read_csv("E-commerce-public-dataset/E-Commerce Public Dataset/order_payments_dataset.csv")
item_df = pd.read_csv("E-commerce-public-dataset/E-Commerce Public Dataset/order_items_dataset.csv")
order_df = pd.read_csv("E-commerce-public-dataset/E-Commerce Public Dataset/orders_dataset.csv")
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
order_df["order_purchase_timestamp"] = pd.to_datetime(order_df["order_purchase_timestamp"])
order_df["order_delivered_customer_date"] = pd.to_datetime(order_df["order_delivered_customer_date"])
order_df["order_estimated_delivery_date"] = pd.to_datetime(order_df["order_estimated_delivery_date"])
order_df["delivery_time"] = (order_df["order_delivered_customer_date"] - order_df["order_purchase_timestamp"]).dt.days
st.subheader("Ringkasan Waktu Pengiriman")
st.write(order_df[["delivery_time"]].describe())

# Gabungkan data orders_df dengan customers_df
orders_customers_df = pd.merge(order_df, customers_df, on='customer_id', how='left')

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
orders_payments_reviews_df = pd.merge(order_df, payment_df, on='order_id', how='left')
orders_payments_reviews_df = pd.merge(orders_payments_reviews_df, review_df, on='order_id', how='left')

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
