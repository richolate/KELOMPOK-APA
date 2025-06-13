import sqlite3

conn = sqlite3.connect("product_service.db")
cursor = conn.cursor()

print("-- Raw Materials --")
for row in cursor.execute("SELECT * FROM raw_materials"):
    print(row)

print("\n-- Products --")
for row in cursor.execute("SELECT * FROM products"):
    print(row)

conn.close()
