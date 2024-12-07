import datetime
import typing

from .formatter import DataFormatter


class DisplayManager:
    def __init__(self) -> None:
        self.col_width: typing.Dict[str, int] = {
            "daily": 12,
            "budget": 12,
            "total": 12,
            "monthly": 14,
            "fetch": 22,
            "total_avail": 10,
        }
        self.formatter: DataFormatter = DataFormatter()

    def print_headers(self) -> None:
        print(
            f"{'DAILY USED':>{self.col_width['daily']}} "
            f"{'DAILY BUDGET':>{self.col_width['budget']}} "
            f"{'TOTAL USED':>{self.col_width['total']}} "
            f"{'MONTHLY BUDGET':>{self.col_width['monthly']}} "
            f"{'TOTAL':>{self.col_width['total_avail']}} "
            f"{'DATA FETCH TIME':<{self.col_width['fetch']}}"
        )
        print("-" * 92)

    def print_record(
        self,
        record: typing.Tuple[float, float, datetime.datetime, float, float],
        prev_amount: float,
    ) -> None:
        _, amount, scraped_at, daily_limit, total = record
        daily_used: float = amount - prev_amount
        remaining: float = total - amount

        daily_str: str = f"{int(daily_used)}GB"
        total_str: str = f"{int(amount)}GB"
        remaining_str: str = f"{int(remaining)}GB"
        total_avail_str: str = f"{int(total)}GB"
        fetch_time: str = self.formatter.format_time(scraped_at)

        print(
            f"{daily_str:>{self.col_width['daily']}} "
            f"{self.formatter.format_gb(daily_limit):>{self.col_width['budget']}} "
            f"{total_str:>{self.col_width['total']}} "
            f"{remaining_str:>{self.col_width['monthly']}} "
            f"{total_avail_str:>{self.col_width['total_avail']}} "
            f"{fetch_time:<{self.col_width['fetch']}}"
        )
