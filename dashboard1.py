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

st.set_page_config(page_title="Dashboard E-Commerce", layout="wide")
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


# Sidebar untuk filter interaktif
st.sidebar.header("Filter Data")
selected_state = st.sidebar.selectbox("Pilih Negara Bagian", customers_df["customer_state"].unique())

df_filtered_customers = customers_df[customers_df["customer_state"] == selected_state]
df_filtered_orders = order_df.merge(df_filtered_customers, on='customer_id', how='inner')
df_filtered_payments = payment_df.merge(df_filtered_orders, on='order_id', how='inner')
df_filtered_reviews = review_df.merge(df_filtered_orders, on='order_id', how='inner')

st.sidebar.write(f"Jumlah pelanggan di {selected_state}: {df_filtered_customers.shape[0]}")

# Distribusi jumlah pelanggan berdasarkan negara bagian
st.subheader("Distribusi Jumlah Pelanggan Berdasarkan Negara Bagian")
customer_state_counts = customers_df.groupby("customer_state")["customer_id"].nunique().reset_index()
customer_state_counts = customer_state_counts.sort_values(by='customer_id', ascending=False)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=customer_state_counts, x='customer_state', y='customer_id', palette='coolwarm', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Eksplorasi waktu pengiriman
order_df["order_purchase_timestamp"] = pd.to_datetime(order_df["order_purchase_timestamp"])
order_df["order_delivered_customer_date"] = pd.to_datetime(order_df["order_delivered_customer_date"])

df_filtered_orders["order_purchase_timestamp"] = pd.to_datetime(df_filtered_orders["order_purchase_timestamp"], errors='coerce')
df_filtered_orders["order_delivered_customer_date"] = pd.to_datetime(df_filtered_orders["order_delivered_customer_date"], errors='coerce')

df_filtered_orders["delivery_time"] = (df_filtered_orders["order_delivered_customer_date"] - df_filtered_orders["order_purchase_timestamp"]).dt.days

st.subheader("Ringkasan Waktu Pengiriman di " + selected_state)
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df_filtered_orders["delivery_time"], bins=20, kde=True, color='blue', ax=ax)
ax.set_title("Distribusi Waktu Pengiriman di " + selected_state)
st.pyplot(fig)

# Hubungan metode pembayaran dengan ulasan
df_filtered_review_payment = df_filtered_payments.merge(df_filtered_reviews, on='order_id', how='left')
review_payment_agg = df_filtered_review_payment.groupby("payment_type").agg({"review_score": "mean", "payment_value": "mean"}).reset_index()

st.subheader("Rata-rata Skor Ulasan Berdasarkan Metode Pembayaran di " + selected_state)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=review_payment_agg, x="payment_type", y="review_score", palette='viridis', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Scatter plot hubungan jumlah pembayaran dengan skor ulasan
st.subheader("Hubungan Jumlah Pembayaran dengan Skor Ulasan di " + selected_state)
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_filtered_review_payment, x='payment_value', y='review_score', alpha=0.5, color='purple', ax=ax)
ax.set_title("Scatter Plot: Pembayaran vs Ulasan di " + selected_state)
st.pyplot(fig)

st.subheader("Ringkasan Statistik Pembayaran dan Ulasan di " + selected_state)
st.write(df_filtered_review_payment[['payment_value', 'review_score']].describe())
