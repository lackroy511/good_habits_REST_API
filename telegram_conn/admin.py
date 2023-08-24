from django.contrib import admin

from telegram_conn.models import ConnectedChats, ProcessedMessage

# Register your models here.


@admin.register(ConnectedChats)
class ConnectedChatsAdmin(admin.ModelAdmin):
    
    fields = ('tg_chat_id',)


@admin.register(ProcessedMessage)
class ProcessedMessageAdmin(admin.ModelAdmin):
    
    fields = ('message_data',)
