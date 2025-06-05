from ariadne import QueryType, MutationType
from database import get_db_connection

query = QueryType()
mutation = MutationType()

@query.field("ping")
def resolve_ping(_, info):
    return "pong"

@query.field("users")
def resolve_users(_, info):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, email, phone, address, created_at FROM users")
    rows = c.fetchall()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3],
            "address": row[4],
            "created_at": row[5]
        })
    return users

@mutation.field("addUser")
def resolve_add_user(_, info, name, email, phone=None, address=None):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (name, email, phone, address, created_at)
        VALUES (?, ?, ?, ?, DATE('now'))
        RETURNING id, name, email, phone, address, created_at
    """, (name, email, phone, address))
    new_user = c.fetchone()
    conn.commit()
    conn.close()

    return {
        "id": new_user[0],
        "name": new_user[1],
        "email": new_user[2],
        "phone": new_user[3],
        "address": new_user[4],
        "created_at": new_user[5]
    }


@mutation.field("editUser")
def resolve_edit_user(_, info, id, name, email, phone=None, address=None):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE users SET name = ?, email = ?, phone = ?, address = ?
        WHERE id = ?
        RETURNING id, name, email, phone, address, created_at
    """, (name, email, phone, address, id))
    updated_user = c.fetchone()
    conn.commit()
    conn.close()

    if updated_user:
        return {
            "id": updated_user[0],
            "name": updated_user[1],
            "email": updated_user[2],
            "phone": updated_user[3],
            "address": updated_user[4],
            "created_at": updated_user[5]
        }
    return None


@mutation.field("deleteUser")
def resolve_delete_user(_, info, id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        DELETE FROM users
        WHERE id = ?
        RETURNING id, name, email, phone, address, created_at
    """, (id,))
    deleted_user = c.fetchone()
    conn.commit()
    conn.close()

    if deleted_user:
        return {
            "id": deleted_user[0],
            "name": deleted_user[1],
            "email": deleted_user[2],
            "phone": deleted_user[3],
            "address": deleted_user[4],
            "created_at": deleted_user[5]
        }
    return None

resolvers = [query, mutation]
