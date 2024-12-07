import sys

from .cli import parse_args
from .data_processor import DataProcessor
from .display import DisplayManager


def main() -> int:
    args = parse_args()

    processor = DataProcessor(args.data_file)
    display = DisplayManager()

    records = processor.process_data()

    display.print_headers()

    prev_amount: float = 0.0
    for record in records:
        display.print_record(record, prev_amount)
        prev_amount = record[1]

    return 0


if __name__ == "__main__":
    sys.exit(main())
