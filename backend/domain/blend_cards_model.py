from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


blend_cards = Table('blend_cards', metadata,
    Column('code', String(64), primary_key=True),
    Column('order_ref', String(64), ForeignKey('scent_orders.code'), nullable=False, unique=True),
    Column('sheet', String(64), ForeignKey('loss_sheets.code'), nullable=False, unique=True),
    Column('lots', JSON, nullable=False),
    Column('grams', Integer, nullable=False),
    Column('labels', JSON, nullable=False),
    Column('state', String(160), nullable=False),
    CheckConstraint("state in ('已保留','已核销')"),
    CheckConstraint('grams > 0'),
)
