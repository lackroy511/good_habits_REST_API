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


class ProcessedMessage(models.Model):
    
    class Meta:
        verbose_name = 'обработанное сообщение '
        verbose_name_plural = 'обработанные сообщения'
        
    message_data = models.TextField(
        verbose_name='данные сообщения',
        unique=True,
        )

    def __str__(self) -> str:
        return self.message_data
