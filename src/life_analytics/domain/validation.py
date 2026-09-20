from datetime import datetime


def is_valid_rating(rating: float) -> bool:
    return 1 <= rating <= 5


def is_valid_category(category: str, valid_categories: set[str] | None = None) -> bool:
    if not category.strip():
        return False

    if valid_categories is None:
        return True

    return category in valid_categories


def is_valid_time(time: str) -> bool:
    try:
        datetime.strptime(time, "%H:%M")
        return True
    except ValueError:
        return False


def is_valid_datetime(datetime_value: str) -> bool:
    try:
        datetime.strptime(datetime_value, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False
