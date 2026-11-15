
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# FUNGSI FORMAT RUPIAH
# ==========================================

def format_rupiah(value):

    if abs(value) >= 1_000_000_000:
        return f"Rp {value / 1_000_000_000:.2f} M"

    elif abs(value) >= 1_000_000:
        return f"Rp {value / 1_000_000:.2f} Jt"

    elif abs(value) >= 1_000:
        return f"Rp {value / 1_000:.1f} Rb"

    else:
        return f"Rp {value:,.0f}"


# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Nusantara Retail Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# CUSTOM DASHBOARD DESIGN
# ==========================================

st.markdown("""
<style>

/* Background utama */
.stApp {
    background-color: #0E1117;
}

/* Area konten */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Judul utama */
h1 {
    color: #38BDF8 !important;
    font-weight: 800 !important;
}

/* Subjudul */
h2, h3 {
    color: #F8FAFC !important;
    font-weight: 700 !important;
}

/* Kartu KPI */
[data-testid="stMetric"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 12px;
}

/* Label KPI */
[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
}

/* Angka KPI */
[data-testid="stMetricValue"] {
    color: #38BDF8 !important;
    font-weight: 800 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #334155;
}

/* Tombol */
.stDownloadButton button {
    background-color: #0284C7;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 18px;
}

/* Efek hover tombol */
.stDownloadButton button:hover {
    background-color: #0369A1;
    color: white;
    border: none;
}

/* Garis pemisah */
hr {
    border-color: #334155 !important;
}

/* Tabel */
[data-testid="stDataFrame"] {
    border: 1px solid #334155;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. MEMUAT DATASET
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv("sales_data_processed.csv")

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    return df


df = load_data()

# ==========================================
# 3. JUDUL DASHBOARD
# ==========================================

st.title("📊 Nusantara Retail")
st.subheader("Sales Analytics Dashboard")

st.markdown(
    "Dashboard analisis penjualan, pendapatan, "
    "keuntungan, dan performa bisnis retail Indonesia."
)

st.divider()

# ==========================================
# 4. INFORMASI DATASET
# ==========================================

st.caption(
    f"Periode Data: {df['Order_Date'].min():%d %B %Y} "
    f"- {df['Order_Date'].max():%d %B %Y}"
)

st.caption(f"Total Transaksi: {len(df):,}")

# ==========================================
# 5. SIDEBAR FILTER
# ==========================================

st.sidebar.title("🔎 Filter Data")
st.sidebar.markdown("Atur data yang ingin dianalisis.")

# Filter tanggal
date_range = st.sidebar.date_input(
    "Pilih Periode Transaksi",
    value=(
        df["Order_Date"].min().date(),
        df["Order_Date"].max().date()
    ),
    min_value=df["Order_Date"].min().date(),
    max_value=df["Order_Date"].max().date()
)

# Filter kategori
selected_categories = st.sidebar.multiselect(
    "Pilih Kategori",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

# Filter kota
selected_cities = st.sidebar.multiselect(
    "Pilih Kota",
    options=sorted(df["City"].unique()),
    default=sorted(df["City"].unique())
)

# Filter saluran penjualan
selected_channels = st.sidebar.multiselect(
    "Pilih Sales Channel",
    options=sorted(df["Sales_Channel"].unique()),
    default=sorted(df["Sales_Channel"].unique())
)

# ==========================================
# 6. PROSES FILTER DATA
# ==========================================

filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Order_Date"].dt.date >= start_date) &
        (filtered_df["Order_Date"].dt.date <= end_date)
    ]

filtered_df = filtered_df[
    (filtered_df["Category"].isin(selected_categories)) &
    (filtered_df["City"].isin(selected_cities)) &
    (filtered_df["Sales_Channel"].isin(selected_channels))
]



# ==========================================
# 7. KPI UTAMA
# ==========================================

total_revenue = filtered_df["Net_Revenue"].sum()
total_profit = filtered_df["Profit"].sum()
total_transactions = len(filtered_df)

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue != 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
    label="Total Revenue",
    value=format_rupiah(total_revenue)
)

with col2:
    st.metric(
    label="Total Profit",
    value=format_rupiah(total_profit)
)

with col3:
    st.metric(
        label="Total Transactions",
        value=f"{total_transactions:,}"
    )

with col4:
    st.metric(
        label="Profit Margin",
        value=f"{profit_margin:.2f}%"
    )

# ==========================================
# 8. MONTHLY REVENUE TREND
# ==========================================

st.divider()

st.subheader("📈 Monthly Revenue Trend")

# Mengelompokkan pendapatan berdasarkan bulan
monthly_sales = (
    filtered_df
    .groupby(filtered_df["Order_Date"].dt.to_period("M"))["Net_Revenue"]
    .sum()
)

# Mengubah format bulan menjadi string
monthly_sales.index = monthly_sales.index.astype(str)

# Membuat grafik
fig, ax = plt.subplots(figsize=(14, 5))

fig.patch.set_facecolor("#0E1117")
ax.set_facecolor("#0E1117")

monthly_sales.plot(
    kind="line",
    ax=ax,
    color="#38BDF8",
    linewidth=2.5,
    marker="o",
    markersize=7
)

# Memberikan label pendapatan
for x, y in enumerate(monthly_sales.values):
    ax.annotate(
        format_rupiah(y),
        (x, y),
        textcoords="offset points",
        xytext=(0, 12),
        ha="center",
        color="white",
        fontsize=8
    )

# Mengatur tampilan grafik
ax.set_title(
    "Monthly Revenue Performance",
    color="white",
    fontsize=14,
    pad=20
)

ax.set_xlabel("Month", color="white")
ax.set_ylabel("Revenue (IDR)", color="white")

ax.tick_params(colors="white")
ax.grid(
    True,
    linestyle="--",
    alpha=0.2
)

for spine in ax.spines.values():
    spine.set_color("#334155")

plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig)

plt.close(fig)

# ==========================================
# 9. REVENUE BY CATEGORY
# ==========================================

st.divider()

st.subheader("📊 Revenue by Category")

# Menghitung total pendapatan setiap kategori
category_sales = (
    filtered_df
    .groupby("Category")["Net_Revenue"]
    .sum()
    .sort_values(ascending=True)
)

# Membuat grafik batang horizontal
fig, ax = plt.subplots(figsize=(12, 5))

fig.patch.set_facecolor("#0E1117")
ax.set_facecolor("#0E1117")

category_sales.plot(
    kind="barh",
    ax=ax,
    color="#38BDF8",
    width=0.6
)

# Menampilkan angka pendapatan
ax.bar_label(
    ax.containers[0],
    labels=[
    format_rupiah(value)
    for value in category_sales.values
],
    padding=5,
    color="white",
    fontsize=9
)

# Mengatur tampilan grafik
ax.set_title(
    "Revenue Performance by Category",
    color="white",
    fontsize=14,
    pad=20
)

ax.set_xlabel("Revenue (IDR)", color="white")
ax.set_ylabel("Product Category", color="white")

ax.tick_params(colors="white")

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.2
)

ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_color("#334155")

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)

# ==========================================
# 10. TOP 5 BEST-SELLING PRODUCTS
# ==========================================

st.divider()

st.subheader("🏆 Top 5 Best-Selling Products")

# Menghitung pendapatan setiap produk
top_products = (
    filtered_df
    .groupby("Product")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .sort_values(ascending=True)
)

# Membuat grafik batang horizontal
fig, ax = plt.subplots(figsize=(12, 5))

fig.patch.set_facecolor("#0E1117")
ax.set_facecolor("#0E1117")

top_products.plot(
    kind="barh",
    ax=ax,
    color="#38BDF8",
    width=0.6
)

# Menampilkan angka pendapatan
ax.bar_label(
    ax.containers[0],
    labels=[
    format_rupiah(value)
    for value in top_products.values
],
    padding=5,
    color="white",
    fontsize=9
)

# Mengatur tampilan grafik
ax.set_title(
    "Top 5 Products by Revenue",
    color="white",
    fontsize=14,
    pad=20
)

ax.set_xlabel("Revenue (IDR)", color="white")
ax.set_ylabel("Product Name", color="white")

ax.tick_params(colors="white")

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.2
)

ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_color("#334155")

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)

# ==========================================
# 11. SALES PERFORMANCE BY CITY
# ==========================================

st.divider()

st.subheader("🌍 Sales Performance by City")

# Menghitung pendapatan setiap kota
city_sales = (
    filtered_df
    .groupby("City")["Net_Revenue"]
    .sum()
    .sort_values(ascending=True)
)

# Membuat grafik batang horizontal
fig, ax = plt.subplots(figsize=(12, 6))

fig.patch.set_facecolor("#0E1117")
ax.set_facecolor("#0E1117")

city_sales.plot(
    kind="barh",
    ax=ax,
    color="#38BDF8",
    width=0.6
)

# Menampilkan angka pendapatan
ax.bar_label(
    ax.containers[0],
    labels=[
    format_rupiah(value)
    for value in category_sales.values
],
    padding=5,
    color="white",
    fontsize=9
)

# Mengatur tampilan grafik
ax.set_title(
    "Revenue Performance by City",
    color="white",
    fontsize=14,
    pad=20
)

ax.set_xlabel("Revenue (IDR)", color="white")
ax.set_ylabel("City", color="white")

ax.tick_params(colors="white")

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.2
)

ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_color("#334155")

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)

# ==========================================
# 12. ONLINE VS OFFLINE SALES PERFORMANCE
# ==========================================

st.divider()

st.subheader("🛒 Online vs Offline Sales Performance")

# Menghitung pendapatan berdasarkan channel
channel_sales = (
    filtered_df
    .groupby("Sales_Channel")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
)

# Membuat grafik batang
fig, ax = plt.subplots(figsize=(10, 5))

fig.patch.set_facecolor("#0E1117")
ax.set_facecolor("#0E1117")

channel_sales.plot(
    kind="bar",
    ax=ax,
    color=["#38BDF8", "#818CF8"],
    width=0.5
)

# Menampilkan angka pendapatan
ax.bar_label(
    ax.containers[0],
    labels=[
        f"Rp {value:,.0f}"
        for value in channel_sales.values
    ],
    padding=5,
    color="white",
    fontsize=10
)

# Mengatur tampilan grafik
ax.set_title(
    "Revenue by Sales Channel",
    color="white",
    fontsize=14,
    pad=20
)

ax.set_xlabel("Sales Channel", color="white")
ax.set_ylabel("Revenue (IDR)", color="white")

ax.tick_params(colors="white", rotation=0)

ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.2
)

ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_color("#334155")

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)

# ==========================================
# 13. PROFIT BY CATEGORY
# ==========================================

st.divider()

st.subheader("💰 Profit by Category")

# Menghitung keuntungan setiap kategori
category_profit = (
    filtered_df
    .groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=True)
)

# Membuat grafik batang horizontal
fig, ax = plt.subplots(figsize=(12, 5))

fig.patch.set_facecolor("#0E1117")
ax.set_facecolor("#0E1117")

category_profit.plot(
    kind="barh",
    ax=ax,
    color="#22C55E",
    width=0.6
)

# Menampilkan angka keuntungan
ax.bar_label(
    ax.containers[0],
    labels=[
    format_rupiah(value)
    for value in category_sales.values
],
    padding=5,
    color="white",
    fontsize=9
)

# Mengatur tampilan grafik
ax.set_title(
    "Profit Performance by Category",
    color="white",
    fontsize=14,
    pad=20
)

ax.set_xlabel("Profit (IDR)", color="white")
ax.set_ylabel("Product Category", color="white")

ax.tick_params(colors="white")

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.2
)

ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_color("#334155")

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)

# ==========================================
# 14. PRODUCT PERFORMANCE TABLE
# ==========================================

st.divider()

st.subheader("📋 Product Performance Analysis")

# Menghitung performa setiap produk
product_performance = (
    filtered_df
    .groupby("Product")
    .agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Revenue=("Net_Revenue", "sum"),
        Total_Profit=("Profit", "sum")
    )
    .reset_index()
)

# Menghitung profit margin setiap produk
product_performance["Profit_Margin"] = (
    product_performance["Total_Profit"] /
    product_performance["Total_Revenue"].replace(0, float("nan"))
) * 100

# Mengurutkan berdasarkan pendapatan terbesar
product_performance = product_performance.sort_values(
    by="Total_Revenue",
    ascending=False
)

# Menampilkan tabel
# Membuat salinan khusus untuk tampilan tabel
product_display = product_performance.copy()

# Mengubah format nilai Rupiah
product_display["Total_Revenue"] = product_display["Total_Revenue"].apply(format_rupiah)
product_display["Total_Profit"] = product_display["Total_Profit"].apply(format_rupiah)

# Format persentase keuntungan
product_display["Profit_Margin"] = product_display["Profit_Margin"].apply(
    lambda x: f"{x:.2f}%"
)
st.dataframe(
    product_display,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# 15. BUSINESS INSIGHTS
# ==========================================

st.divider()

st.subheader("💡 Business Insights")

if not filtered_df.empty:

    # Produk dengan pendapatan tertinggi
    best_product = (
        filtered_df.groupby("Product")["Net_Revenue"]
        .sum()
        .idxmax()
    )

    # Kategori dengan keuntungan tertinggi
    best_category = (
        filtered_df.groupby("Category")["Profit"]
        .sum()
        .idxmax()
    )

    # Kota dengan pendapatan tertinggi
    best_city = (
        filtered_df.groupby("City")["Net_Revenue"]
        .sum()
        .idxmax()
    )

    # Bulan dengan pendapatan tertinggi
    monthly_insight = (
        filtered_df
        .groupby(filtered_df["Order_Date"].dt.to_period("M"))["Net_Revenue"]
        .sum()
    )

    best_month = monthly_insight.idxmax().strftime("%B %Y")

    # Menghitung nilai pendapatan dan keuntungan tertinggi
    best_product_revenue = (
        filtered_df.groupby("Product")["Net_Revenue"]
        .sum().max()
    )

    best_category_profit = (
        filtered_df.groupby("Category")["Profit"]
        .sum().max()
    )

    best_city_revenue = (
        filtered_df.groupby("City")["Net_Revenue"]
        .sum().max()
    )

    best_month_revenue = monthly_insight.max()

    
# Menampilkan empat kartu insight
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🏆 Top Revenue Product",
        value=best_product,
        delta=format_rupiah(best_product_revenue),
        delta_color="off"
    )

with col2:
    st.metric(
        label="💰 Top Profit Category",
        value=best_category,
        delta=format_rupiah(best_category_profit),
        delta_color="off"
    )

with col3:
    st.metric(
        label="🌍 Top Revenue City",
        value=best_city,
        delta=format_rupiah(best_city_revenue),
        delta_color="off"
    )

with col4:
    st.metric(
        label="📅 Top Revenue Month",
        value=best_month,
        delta=format_rupiah(best_month_revenue),
        delta_color="off"
    )




# ==========================================
# 16. DOWNLOAD SALES REPORT
# ==========================================

st.divider()

st.subheader("📥 Download Sales Report")

st.markdown(
    "Unduh data transaksi berdasarkan filter "
    "yang sedang kamu pilih."
)

if not filtered_df.empty:

    # Ringkasan data yang akan diunduh
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Transaksi",
            value=f"{len(filtered_df):,}"
        )

    with col2:
        st.metric(
            label="Total Revenue",
            value=format_rupiah(filtered_df["Net_Revenue"].sum())
        )

    with col3:
        st.metric(
            label="Total Profit",
            value=format_rupiah(filtered_df["Profit"].sum())
        )

    # Mengubah data hasil filter menjadi CSV
    csv_data = filtered_df.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    # Membuat nama file berdasarkan periode laporan
    start_date = filtered_df["Order_Date"].min().strftime("%Y%m%d")
    end_date = filtered_df["Order_Date"].max().strftime("%Y%m%d")

    file_name = (
        f"Nusantara_Retail_Report_{start_date}_{end_date}.csv"
    )

    # Tombol download
    st.download_button(
        label="📥 Download CSV Report",
        data=csv_data,
        file_name=file_name,
        mime="text/csv",
        use_container_width=True
    )

else:
    st.warning(
        "Tidak ada data yang tersedia untuk diunduh. "
        "Silakan ubah filter terlebih dahulu."
    )


