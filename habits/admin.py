from django.contrib import admin

from habits.models import Habit

# Register your models here.


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    fields = (
        'time',
        'lead_time_in_seconds',
        'place',
        'periodicity',
        'deed',
        'reward',
        'is_enjoyable_habit',
        'is_published',
        'connected_enjoyable_habit',
        'user',
    )
