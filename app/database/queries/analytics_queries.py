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
    FETCH_SKU_CHANNEL_PNL_PAGINATION = """
        SELECT *
        FROM bsc.get_channel_sku_pnl_pagination(
            CAST(:start_date AS DATE),
            CAST(:end_date AS DATE),
            :limit,
            :page_no
        )
        """
    FETCH_CATEGORY_PNL_PAGINATION = """
        SELECT *
        FROM bsc.get_category_pnl_pagination(
                CAST(:start_date AS DATE),
                CAST(:end_date AS DATE),
                :limit,
                :page_no
             ) \
        """
    FETCH_PLATFORM_CORRESPONDING_PNL_PAGINATION = """
        SELECT *
        FROM bsc.get_platform_corresponding_pnl_pagination(
                CAST(:start_date AS DATE),
                CAST(:end_date AS DATE),
                :limit,
                :page_no \
             )\
    """
    FETCH_PLATFORM_MONTHLY_PNL_PAGINATION = """
        SELECT *
        FROM bsc.get_platform_monthly_pnl_pagination(
                :limit,
                :page_no \
             ) \
        """
