# Generated by Django 3.2.5 on 2024-08-15 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0011_meal_is_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='is_available',
        ),
        migrations.AddField(
            model_name='restaurantmeal',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='Наличие товара'),
        ),
    ]
