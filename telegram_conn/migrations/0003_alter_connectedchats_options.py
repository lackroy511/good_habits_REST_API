# Generated by Django 4.2.4 on 2023-08-23 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_conn', '0002_alter_connectedchats_tg_chat_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='connectedchats',
            options={'verbose_name': 'подключенный чат', 'verbose_name_plural': 'подключенные чаты'},
        ),
    ]
