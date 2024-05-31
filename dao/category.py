from model.models import Category
from utils import db


def get(category_id):
    row = db.db_statement(
        statement_type='Row',
        sql=f"""
            SELECT id, name, description, folder
            FROM categories
            WHERE id = %s
        """,
        params=(
            category_id,
        )
    )
    if not row:
        return None
    category_model = Category()
    category_model.__dict__.update(row)
    return category_model


def create(category: Category):
    last_insert_id = db.db_statement(
        statement_type='Insert',
        sql=f"""
            INSERT INTO categories
            (name, description, folder)
            VALUES (%s, %s, %s) 
        """,
        params=([getattr(category, field) for field in ['name', 'description', 'folder']]),
    )
    return last_insert_id if last_insert_id else 0


def update(category: Category):
    affected = db.db_statement(
        statement_type='Execute',
        sql=f"""
            UPDATE categories SET
            name            = %s, 
            description     = %s, 
            folder          = %s
            WHERE id        = %s
        """,
        params=([getattr(category, field) for field in ['name', 'description', 'folder', 'id']]),
    )
    return affected


def delete(category_id):
    affected = db.db_statement(
        statement_type='Execute',
        sql=f"""
            DELETE FROM categories
            WHERE id = %s
        """,
        params=(
            category_id,
        ),
    )
    return affected


def all_categories():
    rows = db.db_statement(
        statement_type='List',
        sql=f"""
            SELECT id, name, description, folder
            FROM categories
            ORDER BY id 
        """,
        params=()
    )
    return [Category(**row) for row in rows]


def get_by_category_name(category_name):
    row = db.db_statement(
        statement_type='Row',
        sql=f"""
            SELECT id, name, description, folder
            FROM categories 
            WHERE name = %s 
        """,
        params=(
            category_name,
        )
    )
    if not row:
        return None
    category_model = Category()
    category_model.__dict__.update(row)
    return category_model


def get_category_by_folder(category_folder=''):
    row = db.db_statement(
        statement_type='Row',
        sql=f"""
            SELECT id, name, description, folder
            FROM categories 
            WHERE folder = %s 
        """,
        params=(
            category_folder,
        )
    )
    if not row:
        return None
    category_model = Category()
    category_model.__dict__.update(row)
    return category_model
