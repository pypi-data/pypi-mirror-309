from americansouth.data_processor import DataProcessor


def test_process_data_basic(sample_data_file):
    processor = DataProcessor(str(sample_data_file))
    records = processor.process_data()

    assert len(records) == 2
    assert records[0][1] == 79.13  # amount
    assert records[1][1] == 85.33  # amount


def test_process_data_daily_usage(complex_data_file):
    processor = DataProcessor(str(complex_data_file))
    records = processor.process_data()

    # Check amounts are correctly ordered
    amounts = [record[1] for record in records]
    assert amounts == [50.0, 75.0, 100.0]

    # Check daily usage calculation
    prev_amount = 0
    daily_usages = []
    for record in records:
        amount = record[1]
        daily_usages.append(amount - prev_amount)
        prev_amount = amount

    assert daily_usages == [50.0, 25.0, 25.0]
