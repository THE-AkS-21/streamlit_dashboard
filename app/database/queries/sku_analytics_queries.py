class SkuAnalyticsQueries:
    FETCH_SKU_CHANNEL_PNL_PAGINATION = """
    SELECT * 
    FROM bsc.get_channel_sku_pnl_pagination(
        CAST(:start_date AS DATE),
        CAST(:end_date AS DATE),
        :limit,
        :page_no
    )
    """
