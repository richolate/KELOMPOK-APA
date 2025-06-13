from database import get_db_connection, init_db

def seed_vendors():
    init_db()  # pastikan tabel sudah ada

    conn = get_db_connection()
    cursor = conn.cursor()

    # Hapus data lama
    cursor.execute("DELETE FROM vendor_transactions")
    cursor.execute("DELETE FROM vendors")

    # Insert vendor
    vendors = [
        ("TernaQan", "082112345678")
    ]
    cursor.executemany('''
        INSERT INTO vendors (name, contact_info)
        VALUES (?, ?)
    ''', vendors)

    # Ambil ID vendor untuk digunakan di transaksi
    cursor.execute("SELECT id FROM vendors WHERE name = 'TernaQan'")
    vendor1_id = cursor.fetchone()["id"]
    

    # Insert transaksi vendor
    # transactions = [
    #     (vendor1_id, "sapi", 10, "belum"),
    #     (vendor1_id, "sapi", 5, "sudah"),
    #     (vendor1_id, "sapi", 8, "belum")
    # ]
    # cursor.executemany('''
    #     INSERT INTO vendor_transactions (vendor_id, livestock_type, total, status)
    #     VALUES (?, ?, ?, ?)
    # ''', transactions)

    conn.commit()
    conn.close()
    print("Vendor and transactions seeded successfully.")

if __name__ == "__main__":
    seed_vendors()
