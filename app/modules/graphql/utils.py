from typing import Any


def return_validation_error(validation_error: Exception):
    return {'status': {
        'success': False,
        'error': str(validation_error),
    }}


def return_not_found_error(model_name: str):
    return {'status': {
        'success': False,
        'error': f'Не найден(а) актин(ый/ая) {model_name} с таким id',
    }}


def update_fields(obj: Any, data: dict):
    for attr, value in data.items():
        setattr(obj, attr, value)
