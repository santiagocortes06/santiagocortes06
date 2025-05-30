"""Allow null values for tipo_paro_id in Parada

Revision ID: b05c329009de
Revises: 29e48a56bb4c
Create Date: 2025-04-15 16:23:38.597510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b05c329009de'
down_revision = '29e48a56bb4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('paradas', schema=None) as batch_op:
        batch_op.alter_column('tipo_paro_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('paradas', schema=None) as batch_op:
        batch_op.alter_column('tipo_paro_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
