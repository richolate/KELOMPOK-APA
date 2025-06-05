from database import get_db_connection, init_db

def seed_users():
    init_db()  # pastikan tabel ada

    conn = get_db_connection()
    c = conn.cursor()

    users = [
        ("Aryva", "aryva@example.com", "082123452929", "Bandung", "2025-06-04"),
        ("Dhiya", "dhiya@example.com", "082123452928", "Jakarta", "2025-06-03")
    ]

    # Hapus data sebelumnya (opsional, kalau mau selalu mulai dari awal)
    c.execute("DELETE FROM users")

    c.executemany('''
        INSERT INTO users (name, email, phone, address, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', users)

    conn.commit()
    conn.close()
    print("Users seeded successfully.")

if __name__ == "__main__":
    seed_users()
