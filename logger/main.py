import sys
import os
from collections import Counter


def parse_log_line(line: str) -> dict:
    parts = line.split(" ", 3)
    date_time = parts[0] + " " + parts[1]
    level = parts[2]
    message = parts[3] if len(parts) > 3 else ""
    return {"date_time": date_time, "level": level, "message": message.strip()}


def load_logs(file_path: str) -> list:
    logs = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                logs.append(parse_log_line(line.strip()))
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)
    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    return [log for log in logs if log["level"].lower() == level.lower()]


def count_logs_by_level(logs: list) -> dict:
    levels = [log["level"] for log in logs]
    return dict(Counter(levels))


def display_log_counts(counts: dict):
    print(f"{'Рівень логування':<20} | {'Кількість'}")
    print("-" * 30)
    for level in ["INFO", "DEBUG", "ERROR", "WARNING"]:
        print(f"{level:<20} | {counts.get(level, 0)}")


def main():
    if len(sys.argv) < 2:
        print("Будь ласка, вкажіть шлях до файлу логів.")
        sys.exit(1)

    log_file_path = sys.argv[1]
    level_filter = sys.argv[2].lower() if len(sys.argv) > 2 else None

    if not os.path.exists(log_file_path):
        print(f"Файл {log_file_path} не знайдено.")
        sys.exit(1)

    logs = load_logs(log_file_path)

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level_filter:
        print(f"\nДеталі логів для рівня '{level_filter.upper()}':")
        filtered_logs = filter_logs_by_level(logs, level_filter)
        for log in filtered_logs:
            print(f"{log['date_time']} - {log['message']}")


if __name__ == "__main__":
    main()
