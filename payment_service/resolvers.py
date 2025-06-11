from ariadne import QueryType, MutationType
from database import get_db_connection

query = QueryType()
mutation = MutationType()

@query.field("payments")
def resolve_payments(*_):
    conn = get_db_connection()
    payments = conn.execute("SELECT * FROM payments").fetchall()
    return [dict(row) for row in payments]

def generate_transaction_id(conn, status):
    count = conn.execute("SELECT COUNT(*) FROM payments WHERE payment_status = ?", (status,)).fetchone()[0] + 1
    prefix = {
        "pending": "PDG",
        "paid": "PAID",
        "failed": "FLD",
        "expired": "EXP"
    }.get(status, "UNK")
    return f"{prefix}{count:03d}"

@mutation.field("addPayment")
def resolve_add_payment(_, info, order_id, payment_method, amount, payment_status, transaction_id=None):
    conn = get_db_connection()
    transaction_id = generate_transaction_id(conn, payment_status)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO payments (order_id, payment_method, amount, payment_status, transaction_id) VALUES (?, ?, ?, ?, ?)",
        (order_id, payment_method, amount, payment_status, transaction_id)
    )
    conn.commit()
    new_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM payments WHERE id = ?", (new_id,)).fetchone()
    return dict(row)

resolvers = [query, mutation]
