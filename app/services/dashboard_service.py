# app/services/dashboard_service.py
import pandas as pd
from app.database.query_manager import QueryManager


class DashboardService:
    def __init__(self):
        self.query_manager = QueryManager()

    def get_price_index_data(self):
        """
        Get price index data with all necessary columns for filtering
        """
        query = """
                SELECT
                    date, price_value, category, region
                FROM price_indices
                ORDER BY date \
                """

        df = self.query_manager.execute_query(query)

        # Ensure date column is datetime
        df['date'] = pd.to_datetime(df['date'])

        return df

    def get_metadata(self):
        """
        Get metadata about the available data
        """
        query = """
                SELECT MIN(date)                as min_date, \
                       MAX(date)                as max_date, \
                       COUNT(DISTINCT region)   as region_count, \
                       COUNT(DISTINCT category) as category_count, \
                       COUNT(*)                 as total_records
                FROM price_indices \
                """

        return self.query_manager.execute_query(query)