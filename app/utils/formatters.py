class Formatters:
    @staticmethod
    def number(value: float) -> str:
        if value is None:
            return "N/A"
        return f"{value:,.0f}"

    @staticmethod
    def percentage(value: float) -> str:
        if value is None:
            return "N/A"
        return f"{value:.1f}%"

    @staticmethod
    def date(value) -> str:
        if value is None:
            return "N/A"
        return value.strftime("%Y-%m-%d")