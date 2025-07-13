class DashboardQueries:
    MONTHLY_ORDERS = """
    WITH daily_orders AS (
        SELECT 
            valuationdate::date as order_date,
            SUM(units) as total_units
        FROM bsc.centraldsrdumpv2 
        WHERE whsku = :whsku
        AND valuationdate::date BETWEEN CAST(:start_date AS DATE) AND CAST(:end_date AS DATE)
        GROUP BY valuationdate::date
    )
    SELECT 
        order_date as time,
        total_units as value
    FROM daily_orders
    ORDER BY time ASC
    """

    DAILY_METRICS = """
    SELECT 
        SUM(units) as total_units,
        AVG(units) as avg_units,
        COUNT(DISTINCT valuationdate::date) as days_count
    FROM bsc.centraldsrdumpv2 
    WHERE whsku = :whsku
    AND valuationdate::date BETWEEN CAST(:start_date AS DATE) AND CAST(:end_date AS DATE)
    """

    GET_DASHBOARD_FILTER_METADATA = """
    SELECT DISTINCT category, \
    subcategory, \
    whsku AS sku, \
    MAX(valuationdate::date) OVER () AS last_date
    FROM bsc.centraldsrdumpv2
    ORDER BY category, subcategory, sku \
    """
