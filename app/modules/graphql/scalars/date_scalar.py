from datetime import date


def serialize_date(value: date):
    return value.isoformat()


def parse_date_value(value: str):
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError(f'{value} не является ISO 8601 строкой')
