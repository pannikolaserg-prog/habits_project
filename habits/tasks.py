from celery import shared_task
from django.utils import timezone
from django.conf import settings
import requests
from .models import Habit


@shared_task
def send_habit_reminders():
    now = timezone.now().time()
    today = timezone.now().date()

    # Находим привычки, время которых совпадает с текущим (с точностью до минуты)
    habits = Habit.objects.filter(
        time__hour=now.hour,
        time__minute=now.minute,
        periodicity__gte=1,
        periodicity__lte=7,
    )

    for habit in habits:
        # Проверяем, что сегодня день выполнения (по периодичности)
        days_since_creation = (today - habit.user.date_joined.date()).days
        if days_since_creation % habit.periodicity == 0:
            send_telegram_notification(habit)


def send_telegram_notification(habit):
    user = habit.user
    if not user.telegram_chat_id:
        return

    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        return

    message = (
        f"Напоминание о привычке:\n"
        f"Действие: {habit.action}\n"
        f"Место: {habit.place}\n"
        f"Время: {habit.time}\n"
        f"Длительность: {habit.duration} сек."
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": user.telegram_chat_id,
        "text": message,
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception:
        pass
