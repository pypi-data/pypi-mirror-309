import datetime

from americansouth.usage_calculator import UsageCalculator


def test_calc_daily_limit():
    calculator = UsageCalculator()

    # Test normal case
    limit = calculator.calc_daily_limit(
        amount=100.0,
        total=400.0,
        hours_remaining=240.0,  # 10 days
    )
    assert round(limit, 2) == 30.0  # (400-100)/10 = 30GB per day

    # Test zero days remaining
    limit = calculator.calc_daily_limit(amount=100.0, total=400.0, hours_remaining=0.0)
    assert limit == 0.0


def test_calc_hours_remaining():
    calculator = UsageCalculator()
    current = datetime.datetime(2024, 11, 15, tzinfo=datetime.timezone.utc)
    next_billing = datetime.datetime(2024, 12, 1, tzinfo=datetime.timezone.utc)

    hours = calculator.calc_hours_remaining(current, next_billing)
    assert hours == 384.0  # 16 days * 24 hours
