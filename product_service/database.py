import sqlite3

DATABASE_NAME = 'product_service.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create raw_materials table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS raw_materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_transaction_id INTEGER,
            livestock_type TEXT CHECK(livestock_type IN ('sapi', 'ayam', 'kambing', 'domba')) NOT NULL,
            quantity INTEGER NOT NULL,
            received_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_material_id INTEGER,
            name TEXT NOT NULL,
            unit TEXT,
            quantity INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (raw_material_id) REFERENCES raw_materials(id)
                ON DELETE SET NULL ON UPDATE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("Tables 'raw_materials' and 'products' created or already exist.")

if __name__ == "__main__":
    init_db()
    print("Product database initialized.")
