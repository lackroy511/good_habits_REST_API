from django.db import models

# Create your models here.


class ConnectedChats(models.Model):

    class Meta:
        verbose_name = 'подключенный чат'
        verbose_name_plural = 'подключенные чаты'

    tg_chat_id = models.PositiveIntegerField(
        verbose_name='id чата телеграм',
        unique=True,
    )
