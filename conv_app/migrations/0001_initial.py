# Generated by Django 3.2.8 on 2021-10-25 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrenciesData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, unique=True, verbose_name='Время')),
                ('rates_data', models.TextField(verbose_name='Пары')),
            ],
        ),
    ]