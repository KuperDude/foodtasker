# Generated by Django 3.2.5 on 2024-08-14 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0009_auto_20240813_1340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='restaurant',
        ),
        migrations.CreateModel(
            name='RestaurantMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0, verbose_name='Цена')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreapp.meal')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreapp.restaurant')),
            ],
            options={
                'unique_together': {('restaurant', 'meal')},
            },
        ),
        migrations.AddField(
            model_name='meal',
            name='restaurants',
            field=models.ManyToManyField(related_name='meals', through='coreapp.RestaurantMeal', to='coreapp.Restaurant'),
        ),
    ]
