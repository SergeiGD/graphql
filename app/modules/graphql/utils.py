from typing import Any


def return_validation_error(validation_error: Exception):
    """
    Возврат ошибок валидации при сохранении сущности
    :param validation_error: полученные ошибки
    :return:
    """
    return {'status': {
        'success': False,
        'error': str(validation_error),
    }}


def return_not_found_error(model_name: str):
    """
    Возврат ошибки, если сушность не найдена
    :param model_name: понятное пользователю название модели
    :return:
    """
    return {'status': {
        'success': False,
        'error': f'Не найден(а) актин(ый/ая) {model_name} с таким id',
    }}


def update_fields(obj: Any, data: dict):
    """
    Автоматическое обновление полей модели, с помощью данных, полученных от инпута мутации
    :param obj: объект, который нужно обновить
    :param data: данные из инпута мутации
    :return:
    """
    for attr, value in data.items():
        setattr(obj, attr, value)
