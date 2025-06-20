"""Initial schema setup

Revision ID: debf689e5030
Revises: 
Create Date: 2025-05-18 20:04:26.649319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'debf689e5030'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('quote_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('company', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('pickup_location', sa.String(length=200), nullable=False),
    sa.Column('pickup_lat', sa.Float(), nullable=True),
    sa.Column('pickup_lng', sa.Float(), nullable=True),
    sa.Column('dropoff_location', sa.String(length=200), nullable=False),
    sa.Column('dropoff_lat', sa.Float(), nullable=True),
    sa.Column('dropoff_lng', sa.Float(), nullable=True),
    sa.Column('estimated_distance', sa.Float(), nullable=True),
    sa.Column('cargo_description', sa.Text(), nullable=False),
    sa.Column('preferred_date', sa.Date(), nullable=True),
    sa.Column('additional_notes', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('reviewed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shipment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tracking_id', sa.String(length=20), nullable=False),
    sa.Column('quote_request_id', sa.Integer(), nullable=True),
    sa.Column('customer_name', sa.String(length=100), nullable=False),
    sa.Column('priority', sa.String(length=20), nullable=True),
    sa.Column('pickup_date', sa.DateTime(), nullable=True),
    sa.Column('pickup_time', sa.String(length=10), nullable=True),
    sa.Column('vehicle_plate', sa.String(length=20), nullable=True),
    sa.Column('pickup_status', sa.String(length=20), nullable=True),
    sa.Column('pickup_notes', sa.Text(), nullable=True),
    sa.Column('alternative_contact_name', sa.String(length=100), nullable=True),
    sa.Column('alternative_contact_phone', sa.String(length=20), nullable=True),
    sa.Column('alternative_contact_email', sa.String(length=120), nullable=True),
    sa.Column('pickup_location', sa.String(length=200), nullable=False),
    sa.Column('pickup_lat', sa.Float(), nullable=True),
    sa.Column('pickup_lng', sa.Float(), nullable=True),
    sa.Column('dropoff_location', sa.String(length=200), nullable=False),
    sa.Column('dropoff_lat', sa.Float(), nullable=True),
    sa.Column('dropoff_lng', sa.Float(), nullable=True),
    sa.Column('current_location', sa.String(length=200), nullable=True),
    sa.Column('current_lat', sa.Float(), nullable=True),
    sa.Column('current_lng', sa.Float(), nullable=True),
    sa.Column('cargo_description', sa.Text(), nullable=False),
    sa.Column('cargo_type', sa.String(length=50), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('weight_unit', sa.String(length=10), nullable=True),
    sa.Column('length', sa.Float(), nullable=True),
    sa.Column('width', sa.Float(), nullable=True),
    sa.Column('height', sa.Float(), nullable=True),
    sa.Column('dimension_unit', sa.String(length=10), nullable=True),
    sa.Column('volume', sa.Float(), nullable=True),
    sa.Column('special_handling', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('transport_method', sa.String(length=50), nullable=True),
    sa.Column('estimated_delivery', sa.DateTime(), nullable=True),
    sa.Column('actual_delivery', sa.DateTime(), nullable=True),
    sa.Column('delivery_window_start', sa.DateTime(), nullable=True),
    sa.Column('delivery_window_end', sa.DateTime(), nullable=True),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.Column('currency', sa.String(length=10), nullable=True),
    sa.Column('is_insured', sa.Boolean(), nullable=True),
    sa.Column('insurance_provider', sa.String(length=100), nullable=True),
    sa.Column('insurance_policy_number', sa.String(length=50), nullable=True),
    sa.Column('insurance_coverage_amount', sa.Float(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('internal_notes', sa.Text(), nullable=True),
    sa.Column('tags', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['quote_request_id'], ['quote_request.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tracking_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shipment')
    op.drop_table('quote_request')
    op.drop_table('admin')
    # ### end Alembic commands ###
