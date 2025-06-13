from ariadne import QueryType, MutationType
from database import get_db_connection

query = QueryType()
mutation = MutationType()

@query.field("rawMaterials")
def resolve_raw_materials(_, info):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM raw_materials")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@query.field("products")
def resolve_products(_, info):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@mutation.field("addRawMaterial")
def resolve_add_raw_material(_, info, vendor_transaction_id=None, livestock_type="", quantity=0):
    # Validate livestock_type
    if livestock_type not in ['sapi', 'ayam', 'kambing', 'domba']:
        raise ValueError("Invalid livestock_type. Must be one of: sapi, ayam, kambing, domba")

    # Validate quantity
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")

    conn = get_db_connection()
    c = conn.cursor()

    # Check if vendor_transaction_id already exists
    if vendor_transaction_id:
        c.execute("SELECT id FROM raw_materials WHERE vendor_transaction_id = ?", (vendor_transaction_id,))
        if c.fetchone():
            conn.close()
            raise ValueError("Raw material for this vendor transaction already exists")

    # Tambahkan raw material
    c.execute('''
        INSERT INTO raw_materials (vendor_transaction_id, livestock_type, quantity)
        VALUES (?, ?, ?)
        RETURNING *
    ''', (vendor_transaction_id, livestock_type, quantity))
    row = c.fetchone()

    conn.commit()
    conn.close()
    return dict(row)

@mutation.field("addProduct")
def resolve_add_product(_, info, raw_material_id, name, unit, quantity):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO products (raw_material_id, name, unit, quantity)
        VALUES (?, ?, ?, ?)
        RETURNING *
    ''', (raw_material_id, name, unit, quantity))
    row = c.fetchone()
    conn.commit()
    conn.close()
    return dict(row)

resolvers = [query, mutation]
