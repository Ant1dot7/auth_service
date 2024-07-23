"""Empty message.

Revision ID: 98433862dfa1
Revises: 82e08418ffb2
Create Date: 2024-07-23 07:53:20.230749

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "98433862dfa1"
down_revision: str | None = "82e08418ffb2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_role",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("role", sa.String(length=30), nullable=False),
            sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_role_role"), "user_role", ["role"], unique=True)
    op.add_column("user", sa.Column("role_id", sa.Integer(), nullable=False))
    op.create_foreign_key(None, "user", "user_role", ["role_id"], ["id"])
    # ### end Alembic commands ###
    roles = [
        {"id": 1, "role": "superuser"},
        {"id": 2, "role": "admin"},
        {"id": 3, "role": "employee"},
        {"id": 4, "role": "customer"},
    ]
    op.bulk_insert(
        sa.table(
            "user_role",
                     sa.column("id", sa.Integer),
                     sa.column("role", sa.String(length=30)),
        ),
        roles,
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user", type_="foreignkey")
    op.drop_column("user", "role_id")
    op.drop_index(op.f("ix_user_role_role"), table_name="user_role")
    op.drop_table("user_role")
    # ### end Alembic commands ###
