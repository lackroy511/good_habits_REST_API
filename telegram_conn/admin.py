from django.contrib import admin

from telegram_conn.models import ConnectedChats

# Register your models here.


@admin.register(ConnectedChats)
class ConnectedChatsAdmin(admin.ModelAdmin):
    
    fields = ('tg_chat_id',)
