from django.db import models

# Create your models here.


class ProcessedMessage(models.Model):
    
    class Meta:
        verbose_name = 'обработанное сообщение '
        verbose_name_plural = 'обработанные сообщения'
        
    message_data = models.JSONField(
        verbose_name='данные сообщения',
        unique=True,
        )

    def __str__(self) -> str:
        return self.message_data
