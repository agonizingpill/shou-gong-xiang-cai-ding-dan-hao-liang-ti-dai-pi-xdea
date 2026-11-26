from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


scent_orders = Table('scent_orders', metadata,
    Column('code', String(64), primary_key=True),
    Column('title', String(160), nullable=False),
    Column('grams', Integer, nullable=False),
    Column('scent', String(64), nullable=False),
    Column('declaration', JSON, nullable=False),
    Column('dryer', String(64), nullable=False),
    Column('state', String(160), nullable=False),
    Column('hold_reason', String(160), nullable=True),
    CheckConstraint('grams between 80 and 1200'),
    CheckConstraint("state in ('待耗量','待配料','已冻结','已制单','已核销')"),
)
