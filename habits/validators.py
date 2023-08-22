from typing import Any, OrderedDict

from rest_framework import serializers


class OnlyConnectedEnjoyableHabitOrReward:

    def __call__(self, fields: OrderedDict) -> None:

        reward = dict(fields).get('reward')
        connected_enjoyable_habit = \
            dict(fields).get('connected_enjoyable_habit')

        if reward and connected_enjoyable_habit:
            raise serializers.ValidationError(
                'You should only choose a reward or a enjoyable habit.',
            )


class DurationChecker:

    def __call__(self, fields: OrderedDict) -> None:

        duration_in_seconds = dict(fields).get('duration_in_seconds')

        if duration_in_seconds > 120:
            raise serializers.ValidationError(
                'Duration must be less than 120 seconds.',
            )


class ConnectedEnjoyableHabitIsEnjoyableHabit:

    def __call__(self, fields: OrderedDict) -> None:

        connected_enjoyable_habit = \
            dict(fields).get('connected_enjoyable_habit')

        if connected_enjoyable_habit:
            if not connected_enjoyable_habit.is_enjoyable_habit:
                raise serializers.ValidationError(
                    'Connected_enjoyable_habit must be enjoyable habit.',
                )


class IsEnjoyableHabit:

    def __call__(self, fields: OrderedDict) -> None:

        is_enjoyable_habit = dict(fields).get('is_enjoyable_habit')
        reward = dict(fields).get('reward')
        connected_enjoyable_habit = \
            dict(fields).get('connected_enjoyable_habit')

        if is_enjoyable_habit and reward and connected_enjoyable_habit or \
                is_enjoyable_habit and reward or \
                is_enjoyable_habit and connected_enjoyable_habit:
            
            raise serializers.ValidationError(
                'Enjoyable_habit must be without' +
                'reward and connected enjoyable habit.',
            )
