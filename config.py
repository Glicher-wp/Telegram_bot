import datetime
import os
import pytz


# Айди организации. Находится в профиле рекера.
ORG_ID = "6085222"

# Токен приложения трекера.
YANDEX_TOKEN = "AgAAAABOiBK4AAbi7aj5bQOPik9gtN78U4JxHmM"

# Токен вашего телеграмм бота.
TELEGRAM_TOKEN = "1629283725:AAE8BXN2pwG_gM9v3z3FqckrDW_VrO7CiFc"

# Задаем таймзону и время, чтобы отфильтровать новые задачи за последние 20 минут.
tz = pytz.timezone("Europe/Moscow")
twenty_min_past = datetime.datetime.now(tz) - datetime.timedelta(minutes=20)

# Фиксируем формат времени.
time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
