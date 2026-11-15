
import pandas as pd

# Membaca dataset
df = pd.read_csv("sales_data_indonesia.csv")

# Mengubah kolom tanggal menjadi datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

print("=" * 50)
print("PEMERIKSAAN KUALITAS DATA")
print("=" * 50)

# 1. Ukuran dataset
print("\n1. UKURAN DATASET")
print("Jumlah baris dan kolom:", df.shape)

# 2. Pemeriksaan data kosong
print("\n2. DATA KOSONG")
print(df.isnull().sum())

# 3. Pemeriksaan duplikat
print("\n3. DATA DUPLIKAT")
print("Jumlah duplikat:", df.duplicated().sum())
print("Order ID duplikat:", df["Order_ID"].duplicated().sum())

# 4. Statistik deskriptif
print("\n4. STATISTIK DESKRIPTIF")
print(df[[
    "Quantity",
    "Unit_Price",
    "Unit_Cost",
    "Discount"
]].describe())

# 5. Pemeriksaan nilai kategori
print("\n5. JUMLAH KATEGORI")
print(df["Category"].value_counts())

# 6. Pemeriksaan rentang tanggal
print("\n6. PERIODE TRANSAKSI")
print("Tanggal awal:", df["Order_Date"].min())
print("Tanggal akhir:", df["Order_Date"].max())

# 7. Pemeriksaan logika bisnis
print("\n7. VALIDASI LOGIKA BISNIS")

print("Quantity <= 0:", (df["Quantity"] <= 0).sum())
print("Harga <= 0:", (df["Unit_Price"] <= 0).sum())
print("Modal <= 0:", (df["Unit_Cost"] <= 0).sum())
print("Diskon di luar 0-20%:", (
    (df["Discount"] < 0) | (df["Discount"] > 0.20)
).sum())

print("\nPEMERIKSAAN SELESAI")
