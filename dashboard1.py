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
# Buka ZIP dan baca CSV di dalamnya
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    # Pastikan untuk mengganti 'geolocation_dataset.csv' dengan nama file yang benar di dalam ZIP
    with zip_ref.open('geolocation_dataset.csv') as file:
        geolocation_df = pd.read_csv(file)
        
# Path ke File CSV
customer_df = pd.read_csv("E-commerce-public-dataset/E-Commerce Public Dataset/customers_dataset.csv")
order_reviews_df = pd.read_csv("E-commerce-public-dataset/E-Commerce Public Dataset/order_reviews_dataset.csv")
order_payments_df = pd.read_csv("E-commerce-public-dataset/E-Commerce Public Dataset/order_payments_dataset.csv")
order_items_df = pd.read_csv("E-commerce-public-dataset/E-Commerce Public Dataset/order_items_dataset.csv")

# Menampilkan data dalam bentuk tabel
st.subheader("Preview Dataset")
st.write("Customer Dataset")
st.write(customer_df.head())
st.write("Geolocation Dataset")
st.write(geolocation_df.head())
st.write("Order Reviews Dataset")
st.write(order_reviews_df.head())
st.write("Order Payments Dataset")
st.write(order_payments_df.head())
st.write("Order Items Dataset")
st.write(order_items_df.head())

st.write("Insight :Pada kode di atas, saya memasukkan data yang ingin diolah dan dianalisis. Untuk menjawab pertanyaan no.1, saya menggunakan beberapa dataset di antaranya customers_dataset dan geolocation_dataset.Sedangkan untuk menjawab pertanyaan nomor 2, saya menggunakan dataset di antaranya order_reviews_dataset, order_payments_dataset, dan order_items_dataset.")

st.subheader("Assessing Data")
st.subheader("CEK MISSING VALUES")

missval_customer_df = customer_df.isnull().sum()
missval_geolocation_df = geolocation_df.isnull().sum()
missval_order_reviews_df = order_reviews_df.isnull().sum()
missval_order_payments_df = order_payments_df.isnull().sum()
missval_order_items_df = order_items_df.isnull().sum()

# Menampilkan jumlah missing values
st.write("Missing Values in Customer Dataset:")
st.write(missval_customer_df)
st.write("Missing Values in Geolocation Dataset:")
st.write(missval_geolocation_df)
st.write("Missing Values in Order Reviews Dataset:")
st.write(missval_order_reviews_df)
st.write("Missing Values in Order Payments Dataset:")
st.write(missval_order_payments_df)
st.write("Missing Values in Order Items Dataset:")
st.write(missval_order_items_df)
st.write("**Insight**: Proses ini digunakan untuk menormalisasikan data dengan menghitung jumlah missing value terlebih dahulu sebelum melakukan proses preparation data.")

st.subheader(" Mengecek Data Duplikat")
# Cek data duplikat
dp_customer_count = customer_df.duplicated().sum()
dp_geolocation_count = geolocation_df.duplicated().sum()
dp_order_reviews_count = order_reviews_df.duplicated().sum()
dp_order_payments_count = order_payments_df.duplicated().sum()
dp_order_items_count = order_items_df.duplicated().sum()

st.write(f"Duplicate Count in Customer Dataset: {dp_customer_count}")
st.write(f"Duplicate Count in Geolocation Dataset: {dp_geolocation_count}")
st.write(f"Duplicate Count in Order Reviews Dataset: {dp_order_reviews_count}")
st.write(f"Duplicate Count in Order Payments Dataset: {dp_order_payments_count}")
st.write(f"Duplicate Count in Order Items Dataset: {dp_order_items_count}")
st.write("Di tahapan ini, saya memeriksa apakah masih terdapat duplikasi data atau tidak untuk menghindari redundansi data.")

### Cleaning Data
st.subheader("Cleaning Data")
st.write("Menghapus baris yang masih ada missing value dan isi dengan mean")

# Fungsi mengisi missing values dengan mean
def fill_missing_with_mean(df):
    for column in df.columns:
        if df[column].dtype in ['float64', 'int64']:
            mean_value = df[column].mean()
            df[column].fillna(mean_value, inplace=True)
    return df

# Mengecek missing values sebelum cleaning
st.write("Missing Values Sebelum Cleaning")
st.write("Customer Dataset:", customer_df.isnull().sum())
st.write("Geolocation Dataset:", geolocation_df.isnull().sum())
st.write("Order Reviews Dataset:", order_reviews_df.isnull().sum())
st.write("Order Payments Dataset:", order_payments_df.isnull().sum())
st.write("Order Items Dataset:", order_items_df.isnull().sum())

# Mengisi missing values
customer_df = fill_missing_with_mean(customer_df)
geolocation_df = fill_missing_with_mean(geolocation_df)
order_reviews_df = fill_missing_with_mean(order_reviews_df)
order_payments_df = fill_missing_with_mean(order_payments_df)
order_items_df = fill_missing_with_mean(order_items_df)

# Mengecek missing values setelah cleaning
st.write("✅ Missing Values Setelah Cleaning")
st.write("Customer Dataset:", customer_df.isnull().sum())
st.write("Geolocation Dataset:", geolocation_df.isnull().sum())
st.write("Order Reviews Dataset:", order_reviews_df.isnull().sum())
st.write("Order Payments Dataset:", order_payments_df.isnull().sum())
st.write("Order Items Dataset:", order_items_df.isnull().sum())

st.write("Insight : Pada tahap ini, missing value pada semua kolom diisi dengan nilai mean untuk membersihkan data tanpa harus menghapus baris yang memiliki nilai kosong.")

st.subheader("Exploratory Data Analysis (EDA)")
st.write("No.1 Bagaimana distribusi pelanggan berdasarkan lokasi geografis, dan apakah terdapat pola tertentu dalam transaksi berdasarkan wilayah?")

# Merge customers dengan geolocation berdasarkan zip_code_prefix
customers_geo_df = pd.merge(customer_df, geolocation_df,
                            left_on='customer_zip_code_prefix',  
                            right_on='geolocation_zip_code_prefix',
                            how='left')

# Menampilkan data hasil merge
st.write("Preview Data Setelah Merge")
st.write(customers_geo_df.head())

# Hitung jumlah pelanggan berdasarkan wilayah (state)
customer_state_counts = customers_geo_df.groupby('customer_state')['customer_id'].count().reset_index()
st.write("Disini kita bisa lihat bahwa sebagian besar pelanggan berasal dari beberapa wilayah tertentu yang dapat menjadi target utama dalam strategi pemasaran")

st.write("No.2 Bagaimana pengaruh ulasan pelanggan terhadap metode pembayaran dan jumlah pembelian?")
#Menggabungkan dataset order_reviews dengan order_payments dan order_items
order_analysis_df = order_reviews_df.merge(order_payments_df, on='order_id').merge(order_items_df, on='order_id')

# Buat kategori review
order_analysis_df['review_score_category'] = pd.cut(order_analysis_df['review_score'],
                                      bins=[0, 2, 4, 5],
                                      labels=['negative', 'neutral', 'positive'],
                                      include_lowest=True)

# Hitung metode pembayaran berdasarkan kategori review
payment_review = order_analysis_df.groupby(["review_score_category", "payment_type"]).size().reset_index(name="count")

# Hitung rata-rata jumlah produk yang dibeli berdasarkan kategori review
avg_items_per_review = order_analysis_df.groupby("review_score_category")["order_item_id"].count().reset_index()

# Menampilkan data hasil merge
st.write("Preview Data Setelah Merge")
st.write(order_analysis_df.head())
st.write("Insight : Dari data yang telah digabung bertujuan untuk menganalisis hubungan antara ulasan pelanggan, metode pembayaran, dan jumlah pembelian ")

st.subheader("Visualization & Explanatory Analysis")

# Menampilkan hasil perhitungan
st.subheader("1. Distribusi Pelanggan berdasarkan Lokasi Geografis")
st.write(customer_state_counts)

# Visualisasi menggunakan seaborn
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=customer_state_counts, x="customer_state", y="customer_id", palette="viridis", ax=ax)
plt.xticks(rotation=45)
plt.title("Distribusi Pelanggan berdasarkan Lokasi Geografis")
plt.xlabel("State")
plt.ylabel("Jumlah Pelanggan")
st.pyplot(fig)
st.write ("Insight : Wilayah tertentu memiliki jumlah pelanggan yang lebih banyak dibandingkan wilayah lainnya, hal ini menunjukkan adanya perbedaan distirbusi pelanggan berdasarkan lokasi")

# Menampilkan hasil perhitungan
st.subheader("2A. Pengaruh Ulasan Pelanggan terhadap Metode Pembayaran")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=payment_review, x="review_score_category", y="count", hue="payment_type", palette="coolwarm", ax=ax)
plt.title("Distribusi Metode Pembayaran berdasarkan Kategori Ulasan")
plt.xlabel("Kategori Ulasan")
plt.ylabel("Jumlah Transaksi")
st.pyplot(fig)

st.subheader("2B. Rata-rata Jumlah Pembelian Berdasarkan Skor Ulasan")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=avg_items_per_review, x="review_score_category", y="order_item_id", marker='o', color='b', ax=ax)
plt.title("Hubungan antara Skor Ulasan dan Rata-rata Jumlah Pembelian")
plt.xlabel("Kategori Ulasan")
plt.ylabel("Rata-rata Jumlah Pembelian")
st.pyplot(fig)
st.write(f"Insight :")
st.write(f"Disni kita bisa lihat untuk metode pembayaran tertentu lebih banyak digunakan pada transaksi dengan ulasan positif. Hal ini menunjukkan bahwa pengalaman pelanggan dpaat mempengaruhi pilihan metode pembayaran")
st.write(f"Terdapat korelasi antara skor ulasan pelanggan dan rata-rata jumlah pembelian. Pelanggan dengan ulasan positif cenderung membeli lebih banyak produk, menunjukkan bahwa kepuasan pelanggan dapat berdampak pada loyalitas pembelian")

st.subheader("Conslusion")
st.write("Berdasarkan hasil analisis data dari E-Commerce Public Dataset, berikut adalah kesimpulan dari masing-masing pertanyaan bisnisnya")

st.write("1. Distribusi Pelanggan berdasarkan Lokasi Geografis")
st.write("Hasil analisis menunjukkan bahwa distribusi pelanggan tidak merata di seluruh wilayah. Ada beberapa wilayah yang memiliki jumlah pelanggan lebih tinggi dibandingkan wilayah lainnya. Hal ini dapat disebabkan oleh faktor-faktor seperti kepadatan penduduk, daya beli masyarakat, dan infrastruktur e-commerce yang lebih berkembang di wilayah tertentu.")
st.write(f"Insight Utama: ")
st.write(f"-Beberapa wilayah seperti São Paulo, Rio de Janeiro, dan Minas Gerais memiliki jumlah pelanggan yang lebih tinggi dibandingkan wilayah lainnya.")
st.write(f"Wilayah dengan jumlah pelanggan tinggi dapat menjadi target utama dalam strategi pemasaran, seperti promosi khusus atau peningkatan layanan pengiriman.")
st.write(f"Sebaliknya, wilayah dengan jumlah pelanggan yang lebih sedikit mungkin memerlukan strategi pemasaran yang lebih agresif atau analisis lebih lanjut untuk memahami hambatan yang ada, seperti keterbatasan akses internet atau metode pembayaran yang kurang tersedia.")

st.write("2. Pengaruh Ulasan Pelanggan terhadap Metode Pembayaran")
st.write("Analisis ini bertujuan untuk memahami bagaimana ulasan pelanggan mempengaruhi metode pembayaran yang dipilih serta jumlah pembelian dalam suatu transaksi.")
st.write(f"A. Pengaruh Ulasan terhadap Metode Pembayaran")
st.write(f"Hasil visualisasi menunjukkan bahwa metode pembayaran tertentu lebih banyak digunakan pada transaksi dengan ulasan positif. Misalnya, pelanggan yang memberikan ulasan positif lebih cenderung menggunakan metode pembayaran seperti kartu kredit dan boleto.")
st.write(f"Insight Utama: ")
st.write(f"-Metode pembayaran yang lebih modern dan nyaman, seperti kartu kredit dan dompet digital, lebih sering digunakan oleh pelanggan yang memberikan ulasan positif. Hal ini menunjukkan bahwa pengalaman pembayaran yang mudah dan cepat dapat berkontribusi terhadap tingkat kepuasan pelanggan.")
st.write(f"-Sebaliknya, pelanggan dengan ulasan negatif lebih sering menggunakan metode pembayaran seperti transfer bank atau boleto, yang mungkin memiliki proses yang lebih lama dan kurang fleksibel.")
st.write(f"Hal ini menunjukkan bahwa kenyamanan dan kecepatan dalam metode pembayaran dapat mempengaruhi kepuasan pelanggan.")
st.write(f"B. Pengaruh Ulasan terhadap Jumlah Pembelian")
st.write(f"Hasil analisis menunjukkan bahwa terdapat hubungan antara skor ulasan pelanggan dan jumlah item yang dibeli dalam satu transaksi.")
st.write(f"Insight Utama: ")
st.write(f"-Pelanggan yang memberikan ulasan positif cenderung melakukan pembelian dalam jumlah yang lebih besar dibandingkan dengan pelanggan yang memberikan ulasan netral atau negatif.")
st.write(f"-Sebaliknya, pelanggan dengan ulasan negatif memiliki jumlah pembelian yang lebih sedikit, yang dapat mengindikasikan pengalaman belanja yang kurang memuaskan atau masalah dengan layanan produk.")
st.write(f"Hal ini menunjukkan bahwa kepuasan pelanggan memiliki dampak langsung terhadap jumlah produk yang dibeli, di mana pelanggan yang puas lebih cenderung melakukan pembelian ulang atau meningkatkan volume pembelian mereka.")
