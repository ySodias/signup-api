"""excluindo coluna tipo_treino

Revision ID: be4f12785b6a
Revises: ec24b1ea1b87
Create Date: 2023-04-14 22:38:25.702205

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'be4f12785b6a'
down_revision = 'ec24b1ea1b87'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tb_treino', 'modalidade')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tb_treino', 'modalidade')