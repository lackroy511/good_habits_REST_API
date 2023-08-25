from django.contrib import admin
from django_celery_beat.models import PeriodicTask

from habits.models import Habit, ReminderTask

# Register your models here.


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    fields = (
        'time',
        'duration_in_seconds',
        'place',
        'periodicity',
        'deed',
        'reward',
        'is_enjoyable_habit',
        'is_published',
        'connected_enjoyable_habit',
        'user',
    )


@admin.register(ReminderTask)
class ReminderTaskAdmin(admin.ModelAdmin):
    fields = (
        'task',
        'crontab',
        'args',
        'kwargs',
    )


admin.register(PeriodicTask)
