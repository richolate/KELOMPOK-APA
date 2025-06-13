from database import init_db, get_db_connection

def seed_raw_materials_and_products():
    init_db()
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("DELETE FROM raw_materials")
    c.execute("DELETE FROM products")

    c.execute("INSERT INTO raw_materials (vendor_transaction_id, livestock_type, quantity) VALUES (?, ?, ?)",
              (1, "sapi", 1))
    raw_material_id = c.lastrowid

    products = [
        (raw_material_id, "Daging Sapi Tenderloin", "bungkus", 10),
        (raw_material_id, "Daging Sapi Sirloin", "bungkus", 5)
    ]

    c.executemany("INSERT INTO products (raw_material_id, name, unit, quantity) VALUES (?, ?, ?, ?)", products)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_raw_materials_and_products()
