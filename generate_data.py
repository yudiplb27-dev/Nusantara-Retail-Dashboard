
import pandas as pd
import random
from datetime import datetime, timedelta

# =====================================
# 1. PENGATURAN DATASET
# =====================================

random.seed(42)

TOTAL_TRANSACTIONS = 2000
TOTAL_CUSTOMERS = 500

# =====================================
# 2. DATA PRODUK
# Format: Kategori, Harga Jual, Modal
# =====================================

products = {
    "Beras Premium 5kg": ("Sembako", 78000, 65000),
    "Minyak Goreng 2L": ("Sembako", 36000, 29000),
    "Gula Pasir 1kg": ("Sembako", 18000, 14500),
    "Kopi Lokal 200gr": ("Makanan & Minuman", 32000, 22000),
    "Teh Celup 50pcs": ("Makanan & Minuman", 18000, 12000),
    "Susu UHT 1L": ("Makanan & Minuman", 21000, 16500),
    "Sabun Mandi": ("Perawatan Diri", 12000, 8000),
    "Shampoo 170ml": ("Perawatan Diri", 28000, 19000),
    "Pasta Gigi": ("Perawatan Diri", 16000, 10500),
    "Deterjen 1kg": ("Rumah Tangga", 25000, 18000),
    "Pembersih Lantai": ("Rumah Tangga", 17000, 11500),
    "Tisu 250 sheets": ("Rumah Tangga", 14000, 9000),
    "Headset Bluetooth": ("Elektronik", 125000, 85000),
    "Mouse Wireless": ("Elektronik", 85000, 55000),
    "Keyboard Wireless": ("Elektronik", 175000, 120000),
    "Botol Minum": ("Perlengkapan", 45000, 28000),
    "Tas Belanja": ("Perlengkapan", 25000, 14000),
}

# =====================================
# 3. DATA WILAYAH INDONESIA
# =====================================

locations = {
    "Malang": "Jawa Timur",
    "Surabaya": "Jawa Timur",
    "Bandung": "Jawa Barat",
    "Jakarta": "DKI Jakarta",
    "Semarang": "Jawa Tengah",
    "Yogyakarta": "DI Yogyakarta",
    "Denpasar": "Bali",
    "Medan": "Sumatera Utara",
    "Makassar": "Sulawesi Selatan",
    "Palembang": "Sumatera Selatan",
}

# =====================================
# 4. MEMBUAT DATA PELANGGAN
# =====================================

customers = [
    f"CUST-{i:04d}"
    for i in range(1, TOTAL_CUSTOMERS + 1)
]

# =====================================
# 5. MEMBUAT TRANSAKSI
# =====================================

transactions = []

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

date_range = (end_date - start_date).days

product_names = list(products.keys())

for i in range(1, TOTAL_TRANSACTIONS + 1):

    # Tanggal transaksi
    order_date = start_date + timedelta(
        days=random.randint(0, date_range)
    )

    # Produk dan informasi harga
    product = random.choice(product_names)

    category, unit_price, unit_cost = products[product]

    # Jumlah barang
    quantity = random.choices(
        [1, 2, 3, 4, 5],
        weights=[40, 30, 15, 10, 5]
    )[0]

    # Diskon transaksi
    discount = random.choices(
        [0, 0.05, 0.10, 0.15, 0.20],
        weights=[45, 25, 18, 9, 3]
    )[0]

    # Wilayah pelanggan
    city = random.choice(list(locations.keys()))
    province = locations[city]

    # Metode pembayaran
    payment_method = random.choice([
        "Transfer Bank",
        "E-Wallet",
        "COD",
        "Kartu Debit",
        "Kartu Kredit"
    ])

    # Saluran penjualan
    sales_channel = random.choices(
        ["Online", "Offline"],
        weights=[65, 35]
    )[0]

    # ID pelanggan
    customer_id = random.choice(customers)

    transactions.append({
        "Order_ID": f"ORD-{i:05d}",
        "Order_Date": order_date,
        "Customer_ID": customer_id,
        "Product": product,
        "Category": category,
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Unit_Cost": unit_cost,
        "Discount": discount,
        "Payment_Method": payment_method,
        "City": city,
        "Province": province,
        "Sales_Channel": sales_channel
    })

# =====================================
# 6. MEMBUAT DATAFRAME
# =====================================

df = pd.DataFrame(transactions)
# Mengurutkan berdasarkan tanggal dan merapikan indeks
df = df.sort_values("Order_Date").reset_index(drop=True)

# =====================================
# 7. MENYIMPAN DATASET
# =====================================

df.to_csv(
    "sales_data_indonesia.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Dataset berhasil dibuat!")
print("Jumlah transaksi:", len(df))
print("Jumlah pelanggan:", df["Customer_ID"].nunique())
print("Jumlah produk:", df["Product"].nunique())
print("Periode:", df["Order_Date"].min(), "-", df["Order_Date"].max())

print("\nContoh data:")
print(df.head())

print("\nInformasi dataset:")
print(df.info())
