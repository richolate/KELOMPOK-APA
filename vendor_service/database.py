import sqlite3

DATABASE_NAME = 'vendor_service.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create vendors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_info TEXT
        )
    ''')

    # Create vendor_transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendor_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_id INTEGER NOT NULL,
            livestock_type TEXT CHECK(livestock_type IN ('sapi', 'ayam', 'kambing', 'domba')),
            total INTEGER NOT NULL,
            status TEXT CHECK(status IN ('belum', 'sudah')) DEFAULT 'belum',
            transaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vendor_id) REFERENCES vendors(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Tables 'vendors' and 'vendor_transactions' created or already exist.")

if __name__ == "__main__":
    init_db()
    print("Vendor database initialized.")
