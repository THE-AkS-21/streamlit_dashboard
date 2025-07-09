# app/database/models.py
from sqlalchemy import Column, Integer, Float, String, Date, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = MetaData()

class PriceIndex(Base):
    __tablename__ = 'price_indices'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    price_value = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    region = Column(String(50), nullable=False)