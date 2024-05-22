from model.models import Section
from utils import db


def get(section_id):
    row = db.db_statement(
        statement_type='Row',
        sql=f"""
            SELECT id, name, category_id, description, folder
            FROM sections
            WHERE id = %s
        """,
        params=(
            section_id,
        )
    )
    if not row:
        return None
    section_model = Section()
    section_model.__dict__.update(row)
    return section_model


def create(section: Section):
    last_insert_id = db.db_statement(
        statement_type='Insert',
        sql=f"""
            INSERT INTO sections
            (name, category_id, description, folder)
            VALUES (%s, %s, %s, %s) 
        """,
        params=([getattr(section, field) for field in ['name', 'category_id', 'description', 'folder']]),
    )
    return last_insert_id if last_insert_id else 0


def update(section: Section):
    affected = db.db_statement(
        statement_type='Execute',
        sql=f"""
            UPDATE sections SET
            name            = %s, 
            category_id     = %s, 
            description     = %s, 
            folder          = %s
            WHERE id        = %s
        """,
        params=([getattr(section, field) for field in ['name', 'category_id', 'description', 'folder', 'id']]),
    )
    return affected


def delete(section_id):
    affected = db.db_statement(
        statement_type='Execute',
        sql=f"""
            DELETE FROM sections
            WHERE id = %s
        """,
        params=(
            section_id,
        ),
    )
    return affected


def all_sections():
    rows = db.db_statement(
        statement_type='List',
        sql=f"""
            SELECT id, name, category_id, description, folder 
            FROM sections
            ORDER BY id 
        """,
        params=()
    )
    return [Section(**row) for row in rows]


def list_section_by_category(category_id=0):
    where_clause = f'WHERE category_id = {category_id}' if category_id else ''
    rows = db.db_statement(
        statement_type='List',
        sql=f"""
            SELECT id, name, category_id, description, folder
            FROM sections
            {where_clause}
        """,
        params=(),
    )
    return [Section(**row) for row in rows]


def get_by_section_name(section_name):
    row = db.db_statement(
        statement_type='Row',
        sql=f"""
            SELECT id, name, category_id, description, folder
            FROM sections 
            WHERE name = %s 
        """,
        params=(
            section_name,
        )
    )
    if not row:
        return None
    section_model = Section()
    section_model.__dict__.update(row)
    return section_model
