# Generated by Django 4.1 on 2022-09-12 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0005_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='message',
            field=models.TextField(max_length=120),
        ),
    ]
