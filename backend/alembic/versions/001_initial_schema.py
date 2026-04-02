"""Initial database schema migration.

This migration creates the initial database schema with all required tables.

Revision ID: 001_initial_schema
Revises: 
Create Date: 2024-03-26 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial schema."""
    
    # Create enum types
    op.execute("CREATE TYPE user_role AS ENUM ('admin', 'auditor', 'finance')")
    op.execute("CREATE TYPE risk_level AS ENUM ('Low', 'Medium', 'High')")
    op.execute("CREATE TYPE report_type AS ENUM ('transaction_summary', 'fraud_analysis', 'risk_assessment', 'vendor_analysis', 'compliance')")
    op.execute("CREATE TYPE alert_type AS ENUM ('high_fraud_score', 'high_risk_score', 'duplicate_transaction', 'missing_invoice', 'unusual_vendor', 'weekend_odd_time')")
    
    # organizations table
    op.create_table(
        'organizations',
        sa.Column('organization_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('industry', sa.String(100), nullable=True),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('currency', sa.String(3), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('organization_id'),
        sa.UniqueConstraint('name'),
        sa.Index('ix_organizations_name', 'name'),
    )
    
    # users table
    op.create_table(
        'users',
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('organization_id', sa.String(36), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('password_hash', sa.String(255), nullable=True),
        sa.Column('role', postgresql.ENUM('admin', 'auditor', 'finance', name='user_role'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.organization_id'], ),
        sa.UniqueConstraint('email'),
        sa.Index('ix_users_email', 'email'),
        sa.Index('ix_users_organization_id', 'organization_id'),
    )
    
    # vendors table
    op.create_table(
        'vendors',
        sa.Column('vendor_id', sa.String(36), nullable=False),
        sa.Column('organization_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('industry', sa.String(100), nullable=True),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('risk_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('vendor_id'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.organization_id'], ),
        sa.Index('ix_vendors_name', 'name'),
        sa.Index('ix_vendors_organization_id', 'organization_id'),
    )
    
    # transactions table
    op.create_table(
        'transactions',
        sa.Column('transaction_id', sa.String(36), nullable=False),
        sa.Column('organization_id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=True),
        sa.Column('vendor_id', sa.String(36), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(3), nullable=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('payment_method', sa.String(50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('transaction_date', sa.DateTime(), nullable=True),
        sa.Column('anomaly_flag', sa.Integer(), nullable=False, default=0),
        sa.Column('fraud_score', sa.Float(), nullable=True),
        sa.Column('risk_score', sa.Float(), nullable=True),
        sa.Column('risk_level', postgresql.ENUM('Low', 'Medium', 'High', name='risk_level'), nullable=True),
        sa.Column('duplicate_flag', sa.Integer(), nullable=False, default=0),
        sa.Column('missing_invoice_flag', sa.Integer(), nullable=False, default=0),
        sa.Column('unusual_vendor_flag', sa.Integer(), nullable=False, default=0),
        sa.Column('weekend_or_odd_time_flag', sa.Integer(), nullable=False, default=0),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('transaction_id'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.organization_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.ForeignKeyConstraint(['vendor_id'], ['vendors.vendor_id'], ),
        sa.Index('ix_transactions_organization_id', 'organization_id'),
        sa.Index('ix_transactions_user_id', 'user_id'),
        sa.Index('ix_transactions_vendor_id', 'vendor_id'),
    )
    
    # documents table
    op.create_table(
        'documents',
        sa.Column('document_id', sa.String(36), nullable=False),
        sa.Column('transaction_id', sa.String(36), nullable=True),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=True),
        sa.Column('file_type', sa.String(50), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('ocr_text', sa.Text(), nullable=True),
        sa.Column('ocr_confidence', sa.Float(), nullable=True),
        sa.Column('processed_flag', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('document_id'),
        sa.ForeignKeyConstraint(['transaction_id'], ['transactions.transaction_id'], ),
    )
    
    # reports table
    op.create_table(
        'reports',
        sa.Column('report_id', sa.String(36), nullable=False),
        sa.Column('organization_id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=True),
        sa.Column('report_type', postgresql.ENUM('transaction_summary', 'fraud_analysis', 'risk_assessment', 'vendor_analysis', 'compliance', name='report_type'), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('file_name', sa.String(255), nullable=True),
        sa.Column('file_path', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('report_id'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.organization_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.Index('ix_reports_organization_id', 'organization_id'),
    )
    
    # alerts table
    op.create_table(
        'alerts',
        sa.Column('alert_id', sa.String(36), nullable=False),
        sa.Column('transaction_id', sa.String(36), nullable=False),
        sa.Column('alert_type', postgresql.ENUM('high_fraud_score', 'high_risk_score', 'duplicate_transaction', 'missing_invoice', 'unusual_vendor', 'weekend_odd_time', name='alert_type'), nullable=False),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('severity', sa.String(20), nullable=True),
        sa.Column('resolved_flag', sa.Boolean(), nullable=False, default=False),
        sa.Column('resolved_by', sa.String(36), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('alert_id'),
        sa.ForeignKeyConstraint(['transaction_id'], ['transactions.transaction_id'], ),
        sa.Index('ix_alerts_transaction_id', 'transaction_id'),
    )
    
    # audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('log_id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('organization_id', sa.String(36), nullable=False),
        sa.Column('action_type', sa.String(100), nullable=False),
        sa.Column('target_table', sa.String(100), nullable=True),
        sa.Column('target_id', sa.String(36), nullable=True),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('log_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.organization_id'], ),
        sa.Index('ix_audit_logs_user_id', 'user_id'),
        sa.Index('ix_audit_logs_organization_id', 'organization_id'),
    )


def downgrade() -> None:
    """Drop all tables and types."""
    op.drop_table('audit_logs')
    op.drop_table('alerts')
    op.drop_table('reports')
    op.drop_table('documents')
    op.drop_table('transactions')
    op.drop_table('vendors')
    op.drop_table('users')
    op.drop_table('organizations')
    
    op.execute("DROP TYPE alert_type")
    op.execute("DROP TYPE report_type")
    op.execute("DROP TYPE risk_level")
    op.execute("DROP TYPE user_role")
