from typing import Callable, Generator
import re
from decimal import Decimal

NUM_PATTERN = r"\d+\.\d+"
NUM_FORMAT = "0.00"


def sum_profit(text: str, callback: Generator[str, None, None]) -> Decimal:
    numbers = [Decimal(num).quantize(Decimal(NUM_FORMAT)) for num in callback(text)]

    return sum(numbers)


def generator_numbers(text: str) -> Generator[str, None, None]:
    for str in text.split():
        if re.fullmatch(NUM_PATTERN, str):
            yield str.strip()


text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")
