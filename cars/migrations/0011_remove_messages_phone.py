# Generated by Django 4.1 on 2022-09-14 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0010_alter_messages_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='phone',
        ),
    ]