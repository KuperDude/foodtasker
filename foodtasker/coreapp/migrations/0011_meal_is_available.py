# Generated by Django 3.2.5 on 2024-08-15 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0010_auto_20240814_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='Наличие товара'),
        ),
    ]
