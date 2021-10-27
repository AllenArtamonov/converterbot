from django.db import models


# Create your models here.

class CurrenciesData(models.Model):
    # base_currency = models.CharField(verbose_name='Базовая валюта>')
    created_at = models.DateTimeField(unique=True, verbose_name='Время', auto_now_add=True)
    rates_data = models.TextField(verbose_name='Пары')

