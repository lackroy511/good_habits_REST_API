from django.db import models

# Create your models here.


class Habit(models.Model):

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'

    EVERY_DAY = 1
    EVERY_TWO_DAYS = 2
    EVERY_THREE_DAYS = 3
    EVERY_FOUR_DAYS = 4
    EVERY_FIVE_DAYS = 5
    EVERY_SIX_DAYS = 6
    EVERY_SEVEN_DAYS = 7

    PERIODICITY_CHOICES = (
        (EVERY_DAY, 'каждый день'),
        (EVERY_TWO_DAYS, 'каждые два дня'),
        (EVERY_THREE_DAYS, 'каждые три дня'),
        (EVERY_FOUR_DAYS, 'каждые четыре дня'),
        (EVERY_FIVE_DAYS, 'каждые пять дней'),
        (EVERY_SIX_DAYS, 'каждые шесть дней'),
        (EVERY_SEVEN_DAYS, 'каждые семь дней'),
    )

    time = models.TimeField(
        auto_now=False, auto_now_add=False, verbose_name='время выполнения',
    )
    lead_time_in_seconds = models.PositiveIntegerField(
        verbose_name='время на выполнения в секундах',
    )
    place = models.CharField(
        max_length=150, verbose_name='место выполнения привычки',
    )
    periodicity = models.CharField(
        max_length=50, choices=PERIODICITY_CHOICES,
    )
    deed = models.CharField(
        max_length=150, verbose_name='действие привычки',
    )
    reward = models.CharField(
        max_length=150, verbose_name='вознаграждение', null=True, blank=True,
    )
    is_enjoyable_habit = models.BooleanField(
        default=False, verbose_name='это приятная привычка',
    )
    is_published = models.BooleanField(
        default=False, verbose_name='опубликовано',
    )
    connected_enjoyable_habit = models.OneToOneField(
        'self',
        verbose_name='приятная привычка',
        related_name='enjoyable_habit',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'users.User',
        verbose_name='Владелец',
        related_name='habits',
        on_delete=models.CASCADE,
    )
    
    
