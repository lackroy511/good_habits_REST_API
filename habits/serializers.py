from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = (
            'pk',
            'time',
            'lead_time_in_seconds',
            'place',
            'periodicity',
            'deed',
            'reward',
            'is_enjoyable_habit',
            'is_published',
            'connected_enjoyable_habit',
        )
