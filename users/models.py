from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    username = None
    email = models.EmailField(
        max_length=254, unique=True, verbose_name='почта',
    )
    is_active = models.BooleanField(
        default=False, verbose_name='пользователь активен',
    )
    
    def __str__(self) -> str:
        return f'{self.email}'
