
import pandas as pd

# =====================================
# 1. MEMBACA DATASET
# =====================================

df = pd.read_csv("sales_data_processed.csv")

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# =====================================
# 2. ANALISIS PRODUK
# =====================================

product_analysis = (
    df.groupby("Product")
    .agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Revenue=("Net_Revenue", "sum"),
        Total_Profit=("Profit", "sum")
    )
    .sort_values("Total_Revenue", ascending=False)
)

print("\n" + "=" * 60)
print("1. ANALISIS PERFORMA PRODUK")
print("=" * 60)

print(product_analysis.to_string())

# =====================================
# 3. ANALISIS KATEGORI
# =====================================

category_analysis = (
    df.groupby("Category")
    .agg(
        Total_Transactions=("Order_ID", "count"),
        Total_Revenue=("Net_Revenue", "sum"),
        Total_Profit=("Profit", "sum")
    )
    .sort_values("Total_Profit", ascending=False)
)

print("\n" + "=" * 60)
print("2. ANALISIS PERFORMA KATEGORI")
print("=" * 60)

print(category_analysis.to_string())

# =====================================
# 4. ANALISIS KOTA
# =====================================

city_analysis = (
    df.groupby("City")
    .agg(
        Total_Transactions=("Order_ID", "count"),
        Total_Revenue=("Net_Revenue", "sum"),
        Total_Profit=("Profit", "sum")
    )
    .sort_values("Total_Revenue", ascending=False)
)

print("\n" + "=" * 60)
print("3. ANALISIS PERFORMA KOTA")
print("=" * 60)

print(city_analysis.to_string())

# =====================================
# 5. ANALISIS BULANAN
# =====================================

df["Month"] = df["Order_Date"].dt.to_period("M")

monthly_analysis = (
    df.groupby("Month")
    .agg(
        Total_Revenue=("Net_Revenue", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Transactions=("Order_ID", "count")
    )
)

print("\n" + "=" * 60)
print("4. ANALISIS PENJUALAN BULANAN")
print("=" * 60)

print(monthly_analysis.to_string())

# =====================================
# 6. ANALISIS CHANNEL PENJUALAN
# =====================================

channel_analysis = (
    df.groupby("Sales_Channel")
    .agg(
        Total_Transactions=("Order_ID", "count"),
        Total_Revenue=("Net_Revenue", "sum"),
        Total_Profit=("Profit", "sum")
    )
)

print("\n" + "=" * 60)
print("5. ANALISIS ONLINE VS OFFLINE")
print("=" * 60)

print(channel_analysis.to_string())

# =====================================
# 7. RINGKASAN INSIGHT
# =====================================

best_product = product_analysis["Total_Revenue"].idxmax()
best_category = category_analysis["Total_Profit"].idxmax()
best_city = city_analysis["Total_Revenue"].idxmax()
best_month = monthly_analysis["Total_Revenue"].idxmax()
best_channel = channel_analysis["Total_Revenue"].idxmax()

print("\n" + "=" * 60)
print("BUSINESS INSIGHTS - NUSANTARA RETAIL")
print("=" * 60)

print("Produk dengan pendapatan tertinggi:", best_product)
print("Kategori paling menguntungkan:", best_category)
print("Kota dengan pendapatan tertinggi:", best_city)
print("Bulan dengan pendapatan tertinggi:", best_month)
print("Channel dengan pendapatan tertinggi:", best_channel)

print("\nANALISIS SELESAI!")
