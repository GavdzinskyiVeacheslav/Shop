from model.models import Photo
from utils import db


def get(photo_id):
    row = db.db_statement(
        statement_type='Row',
        sql=f"""
            SELECT id, good_id, width, height
            FROM photos
            WHERE id = %s
        """,
        params=(
            photo_id,
        )
    )

    if not row:
        return None

    photo_model = Photo()
    photo_model.__dict__.update(row)
    return photo_model


def create(photo: Photo):
    last_insert_id = db.db_statement(
        statement_type='Insert',
        sql=f"""
            INSERT INTO photos
            (good_id, width, height)
            VALUES (%s, %s, %s)
        """,
        params=([getattr(photo, field) for field in ['good_id', 'width', 'height']]),
    )
    return last_insert_id if last_insert_id else 0


def update(photo: Photo):
    affected = db.db_statement(
        statement_type='Execute',
        sql=f"""
            UPDATE photos SET
            good_id = %s, 
            width = %s,
            height = %s
        """,
        params=([getattr(photo, field) for field in ['good_id', 'width', 'height']]),
    )
    return affected


def delete(photo_id):
    affected = db.db_statement(
        statement_type='Execute',
        sql=f"""
            DELETE FROM photos
            WHERE id = %s
        """,
        params=(
            photo_id,
        ),
    )
    return affected


def all_photos_ids():
    rows = db.db_statement(
        statement_type='List',
        sql=f"""
            SELECT id
            FROM photos
            ORDER BY id DESC 
        """,
        params=()
    )
    return [row['id'] for row in rows]
