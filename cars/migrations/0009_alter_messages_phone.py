# Generated by Django 4.1 on 2022-09-14 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0008_alter_messages_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='phone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phone_no', to='cars.userprofile'),
        ),
    ]