
import pandas as pd

# 1. Membaca dataset
df = pd.read_csv("sales_data_indonesia.csv")

# 2. Menghitung pendapatan kotor
df["Gross_Revenue"] = (
    df["Quantity"] * df["Unit_Price"]
)

# 3. Menghitung nilai diskon
df["Discount_Amount"] = (
    df["Gross_Revenue"] * df["Discount"]
)

# 4. Menghitung pendapatan bersih
df["Net_Revenue"] = (
    df["Gross_Revenue"] - df["Discount_Amount"]
)

# 5. Menghitung total modal
df["Total_Cost"] = (
    df["Quantity"] * df["Unit_Cost"]
)

# 6. Menghitung keuntungan
df["Profit"] = (
    df["Net_Revenue"] - df["Total_Cost"]
)

# 7. Menghitung profit margin
df["Profit_Margin"] = (
    df["Profit"] / df["Net_Revenue"] * 100
)

# 8. Menampilkan ringkasan bisnis
print("=" * 50)
print("NUSANTARA RETAIL - BUSINESS ANALYSIS")
print("=" * 50)

print("Total Transaksi:", len(df))

print("Gross Revenue: Rp",
      f"{df['Gross_Revenue'].sum():,.0f}")

print("Total Diskon: Rp",
      f"{df['Discount_Amount'].sum():,.0f}")

print("Net Revenue: Rp",
      f"{df['Net_Revenue'].sum():,.0f}")

print("Total Cost: Rp",
      f"{df['Total_Cost'].sum():,.0f}")

print("Total Profit: Rp",
      f"{df['Profit'].sum():,.0f}")

print("Average Profit Margin:",
      f"{df['Profit_Margin'].mean():.2f}%")

print("\nContoh hasil perhitungan:")

print(df[[
    "Product",
    "Quantity",
    "Gross_Revenue",
    "Discount_Amount",
    "Net_Revenue",
    "Profit"
]].head())

# 9. Menghitung margin keseluruhan bisnis
overall_profit_margin = (
    df["Profit"].sum() /
    df["Net_Revenue"].sum()
) * 100

print("\nOverall Profit Margin:",
      f"{overall_profit_margin:.2f}%")

# 10. Menyimpan dataset hasil analisis
df.to_csv(
    "sales_data_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nDataset hasil analisis berhasil disimpan!")
