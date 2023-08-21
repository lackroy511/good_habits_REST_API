from django.contrib import admin

from habits.models import Habit

# Register your models here.


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    fields = ('pk', 'deed', 'time', 'periodicity')
