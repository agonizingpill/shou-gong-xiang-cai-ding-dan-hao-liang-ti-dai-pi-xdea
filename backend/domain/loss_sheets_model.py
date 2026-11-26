from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


loss_sheets = Table('loss_sheets', metadata,
    Column('code', String(64), primary_key=True),
    Column('order_ref', String(64), ForeignKey('scent_orders.code'), nullable=False),
    Column('primary_lot', String(64), ForeignKey('powder_lots.code'), nullable=False),
    Column('need_g', Integer, nullable=False),
    Column('loss_g', Float, nullable=False),
    Column('features', JSON, nullable=False),
    CheckConstraint('need_g between 80 and 1600'),
    CheckConstraint('loss_g >= 0'),
)
