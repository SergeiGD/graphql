from datetime import datetime
from hotel_business_module.settings import settings


def serialize_datetime(value: datetime):
    return value.replace(tzinfo=settings.TIMEZONE).isoformat()


def parse_datetime_value(value: str):
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError(f'{value} не является ISO 8601 строкой')
