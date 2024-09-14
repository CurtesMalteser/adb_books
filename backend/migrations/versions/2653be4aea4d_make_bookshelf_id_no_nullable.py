"""Make BookShelf id no nullable

Revision ID: 2653be4aea4d
Revises: 1cd4dcb367cb
Create Date: 2024-09-14 09:57:14.970686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2653be4aea4d'
down_revision = '1cd4dcb367cb'
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Ensure the sequence is associated with the 'id' column
    op.execute('''
        DO $$ 
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'book_shelves_id_seq') THEN
                CREATE SEQUENCE book_shelves_id_seq OWNED BY book_shelves.id;
            END IF;
        END $$;
    ''')

    # Step 2: Explicitly associate the sequence with the 'id' column
    op.execute('ALTER SEQUENCE book_shelves_id_seq OWNED BY book_shelves.id')

    # Step 3: Backfill 'id' column with unique values using the sequence
    op.execute('''
        UPDATE book_shelves 
        SET id = nextval('book_shelves_id_seq')
        WHERE id IS NULL;
    ''')

    with op.batch_alter_table('book_shelves', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=False)

def downgrade():
    with op.batch_alter_table('book_shelves', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    # Remove the sequence if necessary
    op.execute('DROP SEQUENCE IF EXISTS book_shelves_id_seq')
