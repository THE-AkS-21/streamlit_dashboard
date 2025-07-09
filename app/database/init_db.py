# app/database/init_db.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from app.config.settings import DATABASE_URL
from app.database.models import Base, PriceIndex


def init_database():
    """Initialize database with sample data"""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    # Generate sample data
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=365),
        end=datetime.now(),
        freq='D'
    )

    categories = ['Electronics', 'Food', 'Clothing', 'Housing']
    regions = ['North', 'South', 'East', 'West']

    data = []
    for date in dates:
        for category in categories:
            for region in regions:
                price = 100 + np.random.normal(0, 10)
                data.append({
                    'date': date,
                    'price_value': price,
                    'category': category,
                    'region': region
                })

    df = pd.DataFrame(data)
    df.to_sql('price_indices', engine, if_exists='replace', index=False)


if __name__ == "__main__":
    init_database()