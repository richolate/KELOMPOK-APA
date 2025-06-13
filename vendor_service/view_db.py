import sqlite3

conn = sqlite3.connect("vendor_service.db")
cursor = conn.cursor()

print("=== Data dari tabel vendors ===")
cursor.execute("SELECT * FROM vendors")
vendors = cursor.fetchall()
for row in vendors:
    print(row)

print("\n=== Data dari tabel vendor_transactions ===")
cursor.execute("SELECT * FROM vendor_transactions")
transactions = cursor.fetchall()
for row in transactions:
    print(row)

conn.close()
