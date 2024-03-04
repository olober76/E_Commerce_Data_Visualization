import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='dark')

# Mengambil data
all_df = pd.read_csv('./all_df.csv')

# mengkonversi 'order_purchase_timestamp' ke datetime
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

# data untuk enam bulan terakhir
monthly_orders_df = all_df.resample(rule='M', on='order_purchase_timestamp').agg({
    'order_id': 'nunique',
    'payment_value': 'sum'
})
monthly_orders_df.index = monthly_orders_df.index.strftime('%Y-%m')
monthly_orders_df = monthly_orders_df.reset_index()
monthly_orders_df.rename(columns={
    'order_id': 'order_count',
    'payment_value': 'revenue'
}, inplace=True)
last_sixmonths = monthly_orders_df.iloc[-6:]

# data untuk "Produk yang Paling Banyak Menghasilkan Revenue"
revenue_category_df = all_df.groupby(by='product_category_name_english').payment_value.sum().sort_values(ascending=True).reset_index()

# data untuk "Harga rata-rata produk per kategori"
price_bycategory = all_df.groupby(by='product_category_name_english').price.mean().sort_values(ascending=True).reset_index()

# membuat Side Tabs
tabs = ["Produk yang Paling Banyak Menghasilkan Revenue", "Harga rata-rata produk per kategori", "Performa Penjualan dan Revenue dalam Beberapa Bulan Terakhir"]
choice = st.sidebar.selectbox("Pilih Tab", tabs)

# memunculkan tampilan berdasarkan sidetab yang kamu pilih
if choice == "Performa Penjualan dan Revenue dalam Beberapa Bulan Terakhir":
    st.title("Performa Penjualan dan Revenue dalam Beberapa Bulan Terakhir")

    # memplotting graph untuk order count
    plt.figure(figsize=(10, 5))
    plt.plot(last_sixmonths['order_purchase_timestamp'], last_sixmonths["order_count"], marker='o', linewidth=2, color="#72BCD4")
    plt.title("Jumlah Pembelian 6 Bulan terakhir  (2018)", loc="center", fontsize=20)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Pembelian')
    st.pyplot()

    # memplotting graph untuk revenue
    plt.figure(figsize=(10, 5))
    plt.plot(last_sixmonths['order_purchase_timestamp'], last_sixmonths["revenue"], marker='o', linewidth=2, color="#72BCD4")
    plt.title("Pendapatan 6 Bulan Terakhir (2018)", loc="center", fontsize=20)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlabel('Tanggal')
    plt.ylabel('Pendapatan (dalam satuan Juta)')
    st.pyplot()

# memunculkan tampilan berdasarkan sidetab yang kamu pilih
elif choice == "Produk yang Paling Banyak Menghasilkan Revenue":
    st.title("Produk yang Paling Banyak Menghasilkan Revenue")
    st.subheader("Top 5 Categories by Revenue:")
    st.write(revenue_category_df.head(5))
    
    # memplot graphik
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(x="payment_value", y="product_category_name_english", data=revenue_category_df.sort_values(by='payment_value', ascending=False).head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel('In million')
    ax[0].set_title("Best Performing Category", loc="center", fontsize=15)
    ax[0].tick_params(axis ='y', labelsize=12)

    sns.barplot(x="payment_value", y="product_category_name_english", data=revenue_category_df.sort_values(by="payment_value", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Performing Category", loc="center", fontsize=15)
    ax[1].tick_params(axis='y', labelsize=12)

    plt.suptitle("Best and Worst Performing Category by Revenue", fontsize=20)

    # memunculkan plot di streamlit
    st.pyplot(fig)

elif choice == "Harga rata-rata produk per kategori":
    st.title("Harga rata-rata produk per kategori")
    st.subheader("Top 5 Categories by Average Product Price:")
    st.write(price_bycategory.head(5))
    
    # memplot graph
    plt.figure(figsize=(10,5))
    colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y='product_category_name_english',
        x='price',
        data=price_bycategory.head(5).sort_values(by="price", ascending=False),
        palette=colors_
    )
    plt.title('Average product price per category', loc='center', fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='x', labelsize=12)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
