"""empty message

Revision ID: 3e4dc620036d
Revises: 93bdd05c523d
Create Date: 2022-01-08 15:19:56.326169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e4dc620036d'
down_revision = '93bdd05c523d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('user', sa.Integer(), nullable=True))
    op.drop_constraint('post_user_id_fkey', 'post', type_='foreignkey')
    op.create_foreign_key(None, 'post', 'user', ['user'], ['id'])
    op.drop_column('post', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.create_foreign_key('post_user_id_fkey', 'post', 'user', ['user_id'], ['id'])
    op.drop_column('post', 'user')
    # ### end Alembic commands ###
