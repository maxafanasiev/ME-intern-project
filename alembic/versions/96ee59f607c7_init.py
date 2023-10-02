"""init

Revision ID: 96ee59f607c7
Revises: 
Create Date: 2023-09-28 23:24:02.546636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96ee59f607c7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_email', sa.String(length=255), nullable=False),
    sa.Column('user_firstname', sa.String(length=100), nullable=True),
    sa.Column('user_lastname', sa.String(length=100), nullable=True),
    sa.Column('user_status', sa.String(length=100), nullable=True),
    sa.Column('user_city', sa.String(length=50), nullable=True),
    sa.Column('user_phone', sa.String(length=20), nullable=True),
    sa.Column('user_links', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('user_avatar', sa.String(), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('refresh_token', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_email')
    )
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=255), nullable=False),
    sa.Column('company_title', sa.String(length=100), nullable=True),
    sa.Column('company_description', sa.String(), nullable=True),
    sa.Column('company_city', sa.String(length=50), nullable=True),
    sa.Column('company_phone', sa.String(length=50), nullable=True),
    sa.Column('company_links', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('company_avatar', sa.String(), nullable=True),
    sa.Column('is_visible', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company_admins',
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('company_members',
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('company_members')
    op.drop_table('company_admins')
    op.drop_table('companies')
    op.drop_table('users')
    # ### end Alembic commands ###