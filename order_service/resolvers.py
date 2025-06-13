# resolvers.py
from ariadne import QueryType, MutationType
from database import get_db_connection
from datetime import datetime

query = QueryType()
mutation = MutationType()

@query.field("orders")
def resolve_orders(_, info):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    orders = [dict(row) for row in c.fetchall()]
    conn.close()
    return orders

@query.field("orderItems")
def resolve_order_items(_, info, order_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    items = [dict(row) for row in c.fetchall()]
    conn.close()
    return items

@mutation.field("createOrder")
def resolve_create_order(_, info, user_id, items):
    conn = get_db_connection()
    c = conn.cursor()
    total_amount = sum(item["quantity"] * item["price"] for item in items)
    order_date = datetime.now().isoformat()

    c.execute(
        "INSERT INTO orders (user_id, order_date, total_amount, status) VALUES (?, ?, ?, ?)",
        (user_id, order_date, total_amount, "pending")
    )
    order_id = c.lastrowid

    for item in items:
        c.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
            (order_id, item["product_id"], item["quantity"], item["price"])
        )

    conn.commit()
    c.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    new_order = dict(c.fetchone())
    conn.close()
    return new_order

@mutation.field("updateOrderStatus")
def resolve_update_order_status(_, info, order_id, status):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "UPDATE orders SET status = ? WHERE id = ? RETURNING *",
        (status, order_id)
    )
    updated_order = c.fetchone()
    conn.commit()
    conn.close()

    if updated_order:
        return dict(updated_order)
    else:
        return None

resolvers = [query, mutation]
