from django.contrib import admin

from telegram_conn.models import ProcessedMessage

# Register your models here.


@admin.register(ProcessedMessage)
class ProcessedMessageAdmin(admin.ModelAdmin):
    
    fields = ('message_data',)
