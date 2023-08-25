import json
import random

from django_celery_beat.models import CrontabSchedule, PeriodicTask

from habits.models import ReminderTask


def create_reminder_task(habit) -> None:
    
    kwargs = {
        'tg_chat_id': habit.user.tg_chat_id,
        'place': habit.place,
        'time': str(habit.time),
        'deed': habit.deed,
        'duration_in_seconds': habit.duration_in_seconds,
        
        'reward': habit.reward,
        'connected_enjoyable_habit': habit.connected_enjoyable_habit,
    }

    schedule = CrontabSchedule.objects.get_or_create(
        minute=str(habit.time.minute),
        hour=str(habit.time.hour),
        day_of_week=f'*/{habit.periodicity}',
        day_of_month='*',
        month_of_year='*',
    )
    
    ReminderTask.objects.create(
        name=''.join([str(random.choice(range(0, 10))) for n in range(0, 12)]),
        task='habits.tasks.send_reminder',
        crontab=schedule[0],
        kwargs=json.dumps(kwargs),
        habit=habit,
    )
