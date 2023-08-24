from rest_framework import serializers

from habits.models import Habit
from habits.validators import (ConnectedEnjoyableHabitIsEnjoyableHabit,
                               DurationChecker, IsEnjoyableHabit,
                               OnlyConnectedEnjoyableHabitOrReward)


class HabitGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = (
            'pk',
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


class HabitCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = (
            'pk',
            'time',
            'duration_in_seconds',
            'place',
            'periodicity',
            'deed',
            'reward',
            'is_enjoyable_habit',
            'is_published',
            'connected_enjoyable_habit',
        )
        validators = (
            OnlyConnectedEnjoyableHabitOrReward(),
            DurationChecker(),
            ConnectedEnjoyableHabitIsEnjoyableHabit(),
            IsEnjoyableHabit(),
        )
