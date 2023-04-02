from pytz import timezone
from os import environ

TIMEZONE = timezone('Asia/Irkutsk')
EMAIL_USER = environ.get('EMAIL_USER')
EMAIL_PASSWORD = environ.get('EMAIL_PASSWORD')
EMAIL_HOST = environ.get('EMAIL_HOST')
SITE_URL = environ.get('SITE_URL', 'http://localhost:5000')
