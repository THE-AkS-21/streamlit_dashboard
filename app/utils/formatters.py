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

    @staticmethod
    def format_indian_number(value):
        abs_val = abs(value)
        if abs_val >= 10_000_000:
            return f"{value / 10_000_000:.2f} Cr"
        elif abs_val >= 100_000:
            return f"{value / 100_000:.2f} L"
        else:
            return f"{value:,.0f}"
