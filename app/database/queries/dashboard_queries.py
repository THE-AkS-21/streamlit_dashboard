class DashboardQueries:

    MONTHLY_ORDERS_WITH_SKU = """
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

    MONTHLY_ORDERS_NO_SKU = """
    WITH daily_orders AS (
        SELECT 
            valuationdate::date as order_date,
            SUM(units) as total_units
        FROM bsc.centraldsrdumpv2 
        WHERE valuationdate::date BETWEEN CAST(:start_date AS DATE) AND CAST(:end_date AS DATE)
        GROUP BY valuationdate::date
    )
    SELECT 
        order_date as time,
        total_units as value
    FROM daily_orders
    ORDER BY time ASC
    """

    UPDATE_ORDER_VALUE = """
    UPDATE bsc.centraldsrdumpv2
    SET units = :value
    WHERE valuationdate::date = :orderdate
    AND whsku = :whsku
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
    SELECT *
    FROM bsc.centraldsrdumpv2
    WHERE valuationdate::date BETWEEN CAST(:start_date AS DATE) AND CAST(:end_date AS DATE)
    """

    GET_DASHBOARD_FILTERED_CHART_DATA = """
                                        WITH daily_orders \
                                                 AS (SELECT valuationdate::date as order_date, SUM(units) as total_units \
                                                     FROM bsc.centraldsrdumpv2 \
                                                     WHERE valuationdate:: date BETWEEN CAST (:start_date AS DATE) AND CAST (:end_date AS DATE)
                                            {filters}
                                        GROUP BY valuationdate:: date
                                            )
                                        SELECT order_date as time,
            total_units as value
                                        FROM daily_orders
                                        ORDER BY time ASC \
                                        """

    GET_DASHBOARD_CHART_DATA = """
    SELECT *
    FROM bsc.centraldsrdumpv2
    WHERE valuationdate::date BETWEEN CAST(:start_date AS DATE) AND CAST(:end_date AS DATE)
    """


