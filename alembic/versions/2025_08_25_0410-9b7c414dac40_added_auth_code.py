"""added auth code

Revision ID: 9b7c414dac40
Revises: 
Create Date: 2025-08-25 04:10:29.164432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  # Add SQLModel import


# revision identifiers, used by Alembic.
revision: str = '9b7c414dac40'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true())
    )
    op.add_column(
        'users',
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.false())
    )

    # create enum explicitly
    userrole_enum = sa.Enum('USER', 'SELLER', 'ADMIN', name='userrole')
    userrole_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'users',
        sa.Column('role', userrole_enum, nullable=False, server_default='USER')
    )
    op.add_column(
        'users',
        sa.Column('refresh_token', sqlmodel.sql.sqltypes.AutoString(), nullable=True)
    )

    # make phone optional
    op.alter_column('users', 'phone_number',
        existing_type=sa.VARCHAR(),
        nullable=True
    )
    op.drop_index(op.f('ix_users_email'), table_name='users')

    # cleanup defaults
    op.alter_column('users', 'is_active', server_default=None)
    op.alter_column('users', 'is_verified', server_default=None)
    op.alter_column('users', 'role', server_default=None)



def downgrade() -> None:
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.alter_column('users', 'phone_number',
        existing_type=sa.VARCHAR(),
        nullable=False
    )
    op.drop_column('users', 'refresh_token')
    op.drop_column('users', 'role')
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'is_active')

    # drop enum type
    userrole_enum = sa.Enum('USER', 'SELLER', 'ADMIN', name='userrole')
    userrole_enum.drop(op.get_bind(), checkfirst=True)
