from celery import shared_task

from habits.models import Habit
from telegram_conn.services.tg_api import TelegramAPI


@shared_task
def send_reminder(
        tg_chat_id,
        place,
        time,
        deed,
        duration_in_seconds,
        reward,
        connected_enjoyable_habit):
    
    enj_habit = None
    if connected_enjoyable_habit:
        enj_habit = Habit.objects.get(pk=str(connected_enjoyable_habit))
        
    text = f'''
    Напоминание:
    
    Место: {place}
    Время: {time}
    Действие: {deed}
    Время на выполнение: {duration_in_seconds} секунд
    
    После выполнения:
    Вознаграждение: {reward if reward else 'Не указано'}
    Приятная привычка: {enj_habit.deed if enj_habit else 'Не указано'}
    '''
    
    TelegramAPI.send_message(text, tg_chat_id)
