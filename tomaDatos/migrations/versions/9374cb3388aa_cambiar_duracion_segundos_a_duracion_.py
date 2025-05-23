"""cambiar duracion_segundos a duracion_minutos como float

Revision ID: 9374cb3388aa
Revises: 74ff4614ccbe
Create Date: 2025-04-21 16:55:07.646299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9374cb3388aa'
down_revision = '74ff4614ccbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('paradas', schema=None) as batch_op:
        batch_op.alter_column('duracion_minutos',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)

    with op.batch_alter_table('registro_produccion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('suma_segundos_alistamiento', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('suma_segundos_programado', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('suma_segundos_calidad', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('suma_segundos_averias', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('suma_segundos_organizacional', sa.Integer(), nullable=True))
        batch_op.drop_column('suma_minutos_alistamiento')
        batch_op.drop_column('suma_minutos_programado')
        batch_op.drop_column('suma_minutos_averias')
        batch_op.drop_column('suma_minutos_calidad')
        batch_op.drop_column('suma_minutos_organizacional')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('registro_produccion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('suma_minutos_organizacional', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('suma_minutos_calidad', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('suma_minutos_averias', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('suma_minutos_programado', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('suma_minutos_alistamiento', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('suma_segundos_organizacional')
        batch_op.drop_column('suma_segundos_averias')
        batch_op.drop_column('suma_segundos_calidad')
        batch_op.drop_column('suma_segundos_programado')
        batch_op.drop_column('suma_segundos_alistamiento')

    with op.batch_alter_table('paradas', schema=None) as batch_op:
        batch_op.alter_column('duracion_minutos',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
