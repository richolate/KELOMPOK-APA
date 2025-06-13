from ariadne import QueryType, MutationType
from database import get_db_connection
import requests

query = QueryType()
mutation = MutationType()

@query.field("ping")
def resolve_ping(_, info):
    return "pong"

@query.field("vendors")
def resolve_vendors(_, info):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, contact_info FROM vendors")
    rows = c.fetchall()
    conn.close()

    vendors = []
    for row in rows:
        vendors.append({
            "id": row[0],
            "name": row[1],
            "contact_info": row[2]
        })
    return vendors

@query.field("vendorTransactions")
def resolve_vendor_transactions(_, info, vendor_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT vt.id, vt.vendor_id, vt.livestock_type, vt.total, vt.status, vt.transaction_date, v.name
        FROM vendor_transactions vt
        JOIN vendors v ON vt.vendor_id = v.id
        WHERE vt.vendor_id = ?
    """, (vendor_id,))
    rows = c.fetchall()
    conn.close()

    transactions = []
    for row in rows:
        transactions.append({
            "id": row[0],
            "vendor_id": row[1],
            "livestock_type": row[2],
            "total": row[3],
            "status": row[4],
            "transaction_date": row[5],
            "vendor_name": row[6]
        })
    return transactions

@query.field("vendorTransactionsAll")
def resolve_vendor_transactions_all(_, info):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT vt.*, v.name as vendor_name
        FROM vendor_transactions vt
        LEFT JOIN vendors v ON vt.vendor_id = v.id
    """)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row["id"],
            "vendor_id": row["vendor_id"],
            "vendor_name": row["vendor_name"],
            "livestock_type": row["livestock_type"],
            "total": row["total"],
            "status": row["status"],
            "transaction_date": row["transaction_date"]
        }
        for row in rows
    ]

@mutation.field("addVendorTransaction")
def resolve_add_vendor_transaction(_, info, vendor_id, livestock_type, total):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vendor_transactions (vendor_id, livestock_type, total)
        VALUES (?, ?, ?)
        RETURNING id, vendor_id, livestock_type, total, status, transaction_date
    """, (vendor_id, livestock_type, total))
    transaction = cursor.fetchone()

    cursor.execute("SELECT name FROM vendors WHERE id = ?", (vendor_id,))
    vendor = cursor.fetchone()
    vendor_name = vendor["name"] if vendor else None

    conn.commit()
    conn.close()

    return {
        "id": transaction["id"],
        "vendor_id": transaction["vendor_id"],
        "livestock_type": transaction["livestock_type"],
        "total": transaction["total"],
        "status": transaction["status"],
        "transaction_date": transaction["transaction_date"],
        "vendor_name": vendor_name
    }

@mutation.field("updateTransactionStatus")
def resolve_update_transaction_status(_, info, transaction_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vendor_transactions WHERE id = ?", (transaction_id,))
    transaction = cursor.fetchone()

    if not transaction:
        conn.close()
        return None

    cursor.execute("""
        UPDATE vendor_transactions SET status = ?
        WHERE id = ?
        RETURNING *
    """, (status, transaction_id))
    updated = cursor.fetchone()

    # 🔎 Tambahkan log debug di sini
    print(">> Status akan diupdate ke:", status)
    print(">> Data transaksi:", dict(updated))

    if status.lower() == "sudah":
        mutation = """
        mutation($vendor_transaction_id: Int, $livestock_type: String!, $quantity: Int!) {
            addRawMaterial(vendor_transaction_id: $vendor_transaction_id, livestock_type: $livestock_type, quantity: $quantity) {
                id
            }
        }
        """
        variables = {
            "vendor_transaction_id": updated["id"],
            "livestock_type": updated["livestock_type"].lower(),
            "quantity": updated["total"]
        }

        try:
            print(">> Mengirim request ke product_service...")
            response = requests.post(
                "http://product_service:8003/graphql",
                json={"query": mutation, "variables": variables},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            print(">> Response product_service:", response.text)  # Tambahkan ini untuk debug
        except Exception as e:
            print("[ERROR]: Gagal sinkron ke product_service:", e)

    cursor.execute("SELECT name FROM vendors WHERE id = ?", (updated["vendor_id"],))
    vendor = cursor.fetchone()
    vendor_name = vendor["name"] if vendor else None

    conn.commit()
    conn.close()

    return {
        "id": updated["id"],
        "vendor_id": updated["vendor_id"],
        "livestock_type": updated["livestock_type"],
        "total": updated["total"],
        "status": updated["status"],
        "transaction_date": updated["transaction_date"],
        "vendor_name": vendor_name
    }
resolvers = [query, mutation]
