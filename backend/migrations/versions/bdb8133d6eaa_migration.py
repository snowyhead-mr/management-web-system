"""migration

Revision ID: bdb8133d6eaa
Revises: a6918f64152c
Create Date: 2025-01-14 23:39:03.480284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'bdb8133d6eaa'
down_revision: Union[str, None] = 'a6918f64152c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('positions', sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('positions', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('positions', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.alter_column('positions', 'position_code',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=8),
               type_=sqlmodel.sql.sqltypes.AutoString(length=10),
               nullable=False)
    op.alter_column('positions', 'title',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50),
               type_=sqlmodel.sql.sqltypes.AutoString(length=100),
               nullable=False)
    op.drop_index('ix_positions_position_code', table_name='positions')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_positions_position_code', 'positions', ['position_code'], unique=True)
    op.alter_column('positions', 'title',
               existing_type=sqlmodel.sql.sqltypes.AutoString(length=100),
               type_=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50),
               nullable=True)
    op.alter_column('positions', 'position_code',
               existing_type=sqlmodel.sql.sqltypes.AutoString(length=10),
               type_=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=8),
               nullable=True)
    op.drop_column('positions', 'updated_at')
    op.drop_column('positions', 'created_at')
    op.drop_column('positions', 'description')
    # ### end Alembic commands ###
