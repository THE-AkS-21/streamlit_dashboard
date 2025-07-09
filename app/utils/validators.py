class FilterValidator:
    @staticmethod
    def validate_date_range(start_date: date, end_date: date) -> bool:
        return start_date <= end_date

    @staticmethod
    def validate_selection(items: List[str], allowed_items: List[str]) -> bool:
        return all(item in allowed_items for item in items)