from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


powder_lots = Table('powder_lots', metadata,
    Column('code', String(64), primary_key=True),
    Column('material', String(160), nullable=False),
    Column('scent', String(64), nullable=False),
    Column('declaration', JSON, nullable=False),
    Column('moisture', Float, nullable=False),
    Column('batch_grams', Integer, nullable=False),
    Column('reserved_grams', Integer, nullable=False),
    CheckConstraint('moisture between 4 and 20'),
    CheckConstraint('reserved_grams between 0 and batch_grams'),
    CheckConstraint('batch_grams >= 0'),
)
