"""fisst

Revision ID: 91090880d564
Revises: b45cc996c41d
Create Date: 2022-12-25 23:06:22.582428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91090880d564'
down_revision = 'b45cc996c41d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loai_mon',
    sa.Column('maloai', sa.Integer(), nullable=False),
    sa.Column('tenloai', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('maloai')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loai_mon')
    # ### end Alembic commands ###
