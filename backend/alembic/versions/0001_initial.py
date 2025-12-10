"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2024-05-05
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def timestamps():
    return [
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        'part_categories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('true')),
        *timestamps(),
    )

    op.create_table(
        'tractor_models',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('brand', sa.String(length=100), nullable=False),
        sa.Column('model_name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('true')),
        *timestamps(),
    )

    op.create_table(
        'suppliers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('contact_person', sa.String(length=255)),
        sa.Column('phone', sa.String(length=50)),
        sa.Column('email', sa.String(length=255)),
        sa.Column('gst_number', sa.String(length=50)),
        sa.Column('address_line1', sa.String(length=255)),
        sa.Column('address_line2', sa.String(length=255)),
        sa.Column('city', sa.String(length=100)),
        sa.Column('state', sa.String(length=100)),
        sa.Column('pincode', sa.String(length=20)),
        sa.Column('notes', sa.Text),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('true')),
        *timestamps(),
    )

    op.create_table(
        'customers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50)),
        sa.Column('email', sa.String(length=255)),
        sa.Column('gst_number', sa.String(length=50)),
        sa.Column('address_line1', sa.String(length=255)),
        sa.Column('address_line2', sa.String(length=255)),
        sa.Column('city', sa.String(length=100)),
        sa.Column('state', sa.String(length=100)),
        sa.Column('pincode', sa.String(length=20)),
        sa.Column('notes', sa.Text),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('true')),
        *timestamps(),
    )

    user_role_enum = sa.Enum('ADMIN', 'STAFF', name='userrole')
    # user_role_enum.create(op.get_bind(), checkfirst=True)
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(length=100), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', user_role_enum, nullable=False, server_default='STAFF'),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('true')),
        *timestamps(),
    )

    op.create_table(
        'parts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('part_code', sa.String(length=100), nullable=False, unique=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('part_categories.id')),
        sa.Column('unit_of_measure', sa.String(length=50)),
        sa.Column('purchase_price', sa.Numeric(12, 2)),
        sa.Column('selling_price', sa.Numeric(12, 2)),
        sa.Column('mrp', sa.Numeric(12, 2)),
        sa.Column('tax_rate_percent', sa.Numeric(5, 2)),
        sa.Column('min_stock_level', sa.Integer, server_default='0'),
        sa.Column('current_stock', sa.Integer, server_default='0'),
        sa.Column('location_rack', sa.String(length=50)),
        sa.Column('location_shelf', sa.String(length=50)),
        sa.Column('location_box', sa.String(length=50)),
        sa.Column('primary_supplier_id', sa.Integer, sa.ForeignKey('suppliers.id')),
        sa.Column('barcode_value', sa.String(length=255), unique=True),
        sa.Column('image_url', sa.String(length=255)),
        sa.Column('notes', sa.Text),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('true')),
        *timestamps(),
    )

    op.create_table(
        'parts_compatible_models',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('part_id', sa.Integer, sa.ForeignKey('parts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('tractor_model_id', sa.Integer, sa.ForeignKey('tractor_models.id', ondelete='CASCADE'), nullable=False),
        *timestamps(),
        sa.UniqueConstraint('part_id', 'tractor_model_id', name='uq_part_model'),
    )

    op.create_table(
        'part_suppliers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('part_id', sa.Integer, sa.ForeignKey('parts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('supplier_id', sa.Integer, sa.ForeignKey('suppliers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('supplier_part_code', sa.String(length=100)),
        sa.Column('last_purchase_price', sa.Numeric(12, 2)),
        sa.Column('usual_lead_time_days', sa.Integer),
        sa.Column('is_preferred', sa.Boolean, server_default=sa.text('false')),
        *timestamps(),
        sa.UniqueConstraint('part_id', 'supplier_id', name='uq_part_supplier'),
    )

    op.create_table(
        'purchase_invoices',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('invoice_number', sa.String(length=100), nullable=False, unique=True),
        sa.Column('invoice_date', sa.Date, nullable=False),
        sa.Column('supplier_id', sa.Integer, sa.ForeignKey('suppliers.id'), nullable=False),
        sa.Column('subtotal', sa.Numeric(14, 2), server_default='0'),
        sa.Column('total_tax', sa.Numeric(14, 2), server_default='0'),
        sa.Column('total_amount', sa.Numeric(14, 2), server_default='0'),
        sa.Column('payment_mode', sa.String(length=50)),
        sa.Column('payment_status', sa.String(length=50)),
        sa.Column('notes', sa.Text),
        *timestamps(),
    )

    op.create_table(
        'purchase_invoice_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('purchase_invoice_id', sa.Integer, sa.ForeignKey('purchase_invoices.id', ondelete='CASCADE'), nullable=False),
        sa.Column('part_id', sa.Integer, sa.ForeignKey('parts.id'), nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('unit_price', sa.Numeric(12, 2), nullable=False),
        sa.Column('discount_amount', sa.Numeric(12, 2), server_default='0'),
        sa.Column('tax_rate_percent', sa.Numeric(5, 2), nullable=False),
        sa.Column('tax_amount', sa.Numeric(12, 2), server_default='0'),
        sa.Column('line_total', sa.Numeric(14, 2), nullable=False),
        *timestamps(),
    )

    op.create_table(
        'sales_invoices',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('invoice_number', sa.String(length=100), nullable=False, unique=True),
        sa.Column('invoice_date', sa.Date, nullable=False),
        sa.Column('customer_id', sa.Integer, sa.ForeignKey('customers.id')),
        sa.Column('subtotal', sa.Numeric(14, 2), server_default='0'),
        sa.Column('total_tax', sa.Numeric(14, 2), server_default='0'),
        sa.Column('total_amount', sa.Numeric(14, 2), server_default='0'),
        sa.Column('payment_mode', sa.String(length=50)),
        sa.Column('payment_status', sa.String(length=50)),
        sa.Column('notes', sa.Text),
        *timestamps(),
    )

    op.create_table(
        'sales_invoice_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('sales_invoice_id', sa.Integer, sa.ForeignKey('sales_invoices.id', ondelete='CASCADE'), nullable=False),
        sa.Column('part_id', sa.Integer, sa.ForeignKey('parts.id'), nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('unit_price', sa.Numeric(12, 2), nullable=False),
        sa.Column('discount_amount', sa.Numeric(12, 2), server_default='0'),
        sa.Column('tax_rate_percent', sa.Numeric(5, 2), nullable=False),
        sa.Column('tax_amount', sa.Numeric(12, 2), server_default='0'),
        sa.Column('line_total', sa.Numeric(14, 2), nullable=False),
        *timestamps(),
    )

    adjustment_enum = sa.Enum('DAMAGE', 'CUSTOMER_RETURN', 'SUPPLIER_RETURN', 'MANUAL_CORRECTION', name='adjustmenttype')
    # adjustment_enum.create(op.get_bind(), checkfirst=True)
    op.create_table(
        'stock_adjustments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('part_id', sa.Integer, sa.ForeignKey('parts.id'), nullable=False),
        sa.Column('adjustment_type', adjustment_enum, nullable=False),
        sa.Column('quantity_change', sa.Integer, nullable=False),
        sa.Column('reason', sa.Text),
        sa.Column('created_by_user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        *timestamps(),
    )

    movement_enum = sa.Enum('PURCHASE', 'SALE', 'ADJUSTMENT', name='stockmovementtype')
    # movement_enum.create(op.get_bind(), checkfirst=True)
    op.create_table(
        'stock_movements',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('part_id', sa.Integer, sa.ForeignKey('parts.id'), nullable=False),
        sa.Column('movement_type', movement_enum, nullable=False),
        sa.Column('source_id', sa.Integer),
        sa.Column('quantity_change', sa.Integer, nullable=False),
        sa.Column('balance_after', sa.Integer, nullable=False),
        *timestamps(),
    )


def downgrade() -> None:
    op.drop_table('stock_movements')
    op.drop_table('stock_adjustments')
    op.drop_table('sales_invoice_items')
    op.drop_table('sales_invoices')
    op.drop_table('purchase_invoice_items')
    op.drop_table('purchase_invoices')
    op.drop_table('part_suppliers')
    op.drop_table('parts_compatible_models')
    op.drop_table('parts')
    op.drop_table('users')
    op.drop_table('customers')
    op.drop_table('suppliers')
    op.drop_table('tractor_models')
    op.drop_table('part_categories')
    sa.Enum(name='stockmovementtype').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='adjustmenttype').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='userrole').drop(op.get_bind(), checkfirst=True)
