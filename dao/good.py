from model.models import Good
from utils import db


def get(good_id):
    row = db.db_statement(
        statement_type='Row',
        sql=f"""
            SELECT id, name, description, category_id, section_id, add_date, price, existence
            FROM goods
            WHERE id = %s
        """,
        params=(
            good_id,
        )
    )

    if not row:
        return None

    good_model = Good()
    good_model.__dict__.update(row)
    return good_model


def create(good: Good):
    last_insert_id = db.db_statement(
        statement_type='Insert',
        sql=f"""
            INSERT INTO goods
            (name, description, category_id, section_id, add_date, price, existence)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        params=([getattr(good, field) for field in ['name', 'description', 'category_id',
                                                    'section_id', 'add_date', 'price', 'existence']]),
    )
    return last_insert_id if last_insert_id else 0


def update(good: Good):
    affected = db.db_statement(
        statement_type='Execute',
        sql=f"""
            UPDATE goods SET
            name        = %s, 
            description = %s,
            category_id = $s,
            section_id = $s,
            add_date = $s,
            price = $s,
            existence = $s
            WHERE id    = %s
        """,
        params=([getattr(good, field) for field in ['name', 'description', 'category_id', 'section_id',
                                                    'add_date', 'price', 'existence']]),
    )
    return affected


def delete(good_id):
    affected = db.db_statement(
        statement_type='Execute',
        sql=f"""
            DELETE FROM goods
            WHERE id = %s
        """,
        params=(
            good_id,
        ),
    )
    return affected


def all_goods_ids():
    rows = db.db_statement(
        statement_type='List',
        sql=f"""
            SELECT id
            FROM goods
            ORDER BY id DESC 
        """,
        params=()
    )
    return [row['id'] for row in rows]
