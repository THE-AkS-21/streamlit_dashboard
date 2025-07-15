class AnalyticsQueries:
    FETCH_PLATFORM_PNL_PAGINATION = """
    SELECT * 
    FROM bsc.get_platform_pnl_pagination(
        CAST(:start_date AS DATE),
        CAST(:end_date AS DATE),
        :limit,
        :page_no
    )
    """
