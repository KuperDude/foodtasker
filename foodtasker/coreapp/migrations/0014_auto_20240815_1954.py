# Generated by Django 3.2.5 on 2024-08-15 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0013_cashier'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
