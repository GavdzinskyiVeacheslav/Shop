from model.models import Order
from utils import db


def get(order_id):
    row = db.db_statement(
        statement_type='Row',
        sql=f"""
            SELECT id, name, description
            FROM orders
            WHERE id = %s
        """,
        params=(
            order_id,
        )
    )

    if not row:
        return None

    order_model = Order()
    order_model.__dict__.update(row)
    return order_model


def create(order: Order):
    last_insert_id = db.db_statement(
        statement_type='Insert',
        sql=f"""
            INSERT INTO orders
            (name, description)
            VALUES (%s, %s)
        """,
        params=([getattr(order, field) for field in ['name', 'description']]),
    )
    return last_insert_id if last_insert_id else 0


def update(order: Order):
    affected = db.db_statement(
        statement_type='Execute',
        sql=f"""
            UPDATE orders SET
            name        = %s, 
            description = %s
            WHERE id    = %s
        """,
        params=([getattr(order, field) for field in ['name', 'description']]),
    )
    return affected


def delete(order_id):
    affected = db.db_statement(
        statement_type='Execute',
        sql=f"""
            DELETE FROM orders
            WHERE id = %s
        """,
        params=(
            order_id,
        ),
    )
    return affected


def all_orders_ids():
    rows = db.db_statement(
        statement_type='List',
        sql=f"""
            SELECT id
            FROM orders
            ORDER BY id DESC 
        """,
        params=()
    )
    return [Order(**row) for row in rows]
