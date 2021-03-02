import datetime
import os
import pytz


# Айди организации. Находится в профиле рекера.
ORG_ID = os.environ.get('ORG_ID')

# Токен приложения трекера.
YANDEX_TOKEN = os.environ.get('YANDEX_TOKEN')

# Токен вашего телеграмм бота.
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# Задаем таймзону и время, чтобы отфильтровать новые задачи за последние 20 минут.
tz = pytz.timezone("Europe/Moscow")
twenty_min_past = datetime.datetime.now(tz) - datetime.timedelta(minutes=20)

# Фиксируем формат времени.
time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
