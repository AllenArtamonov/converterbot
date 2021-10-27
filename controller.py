import logging


from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
)

import requests
from datetime import date, datetime, timedelta
import pylab
import matplotlib.dates
from decimal import Decimal
import numpy as np

import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'converter.settings'

import django

django.setup()

from django.db import DatabaseError
from django.conf import settings
from conv_app.models import CurrenciesData

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

api_url = 'http://api.exchangeratesapi.io/v1/'

list_base_currency = 'USD'
converted_rates = {}
r_converted_rates = {}
list_rates = []


def start(update: Update, context: CallbackContext):
    """Starts the conversation and asks the user about continuing."""
    update.message.reply_text(
        'Hi! My name is Convert Bot.\nI want to help you to work with currencies.\n'
        'You can use this commands:\n'
        '/list  -  get rates list,\n'
        '/exchange <amount> <necessary_currency> to <base_currency>\n'
        ' - convert currency (ex. "/exchange 10 EUR to USD")\n'
        '/history <necessary_currency>  -  get currency chart\n'
        '/cancel - stop bot'
    )


def change_base_currency(base_currency=list_base_currency):
    """Gets rates data from API. Changing base currency to USD (or other)"""
    params = dict(access_key=settings.API_KEY)
    resp = requests.get(url=api_url + 'latest', params=params)
    rates_dict = dict(resp.json()['rates'])
    for keys, values in rates_dict.items():
        converted_rates[keys] = float(values / rates_dict[base_currency])


def save_currencies_data():
    """Saves data in django model, db and finally in Admin panel"""
    try:
        CurrenciesData.objects.create(
            rates_data=converted_rates
        )
        print('data was saved in db')
    except DatabaseError:
        pass


def check_db_rates():
    """Checks rates data in DB and if not - requests data from API"""
    global converted_rates, list_rates
    get_last_rates = CurrenciesData.objects.all().order_by("created_at").last()
    last_rates_datetime = get_last_rates.created_at
    last_rates_datetime_naive = last_rates_datetime.replace(tzinfo=None)
    allowable_fault = datetime.today() - timedelta(minutes=10)
    if last_rates_datetime_naive < allowable_fault:
        try:
            change_base_currency()
        except DatabaseError:
            return print('Connection error')
        save_currencies_data()
    else:
        converted_rates = eval(get_last_rates.rates_data)
        print('got data from db')
    for key, value in converted_rates.items():
        r_converted_rates[key] = float(Decimal(value).quantize(Decimal("1.00")))
    list_rates = str(np.vstack(list(map(list, r_converted_rates.items()))))


def list_view(update: Update, context: CallbackContext):
    check_db_rates()
    update.message.reply_text(str(list_rates))


exchange_result = []


def exchange(update: Update, context: CallbackContext):
    """Converts currencies in '10 USD to AMD' format"""
    global exchange_result
    con_request = context.args

    try:
        amount = float(con_request[0])
        necessary_currency = con_request[1].upper()
        base_currency = con_request[3].upper()
    except(IndexError, ValueError):
        update.message.reply_text('Usage: /exchange <amount> <necessary_currency> to <base_currency>')

    if base_currency == list_base_currency:
        check_db_rates()
        exchange_result = Decimal(amount / converted_rates[necessary_currency]).quantize(Decimal("1.00"))
    else:
        change_base_currency(base_currency)
        exchange_result = Decimal(amount / converted_rates[necessary_currency]).quantize(Decimal("1.00"))
    update.message.reply_text(str(exchange_result))


h_dates = []  # list of dates


def get_h_dates():
    """Creates list of last 7 dates"""
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    for i in range(1, 8):
        h_dates.append(start_date + timedelta(days=i))


h_data = []


def graph_chart(update: Update, context: CallbackContext):

    try:
        currency = context.args[0]

    except IndexError:
        update.message.reply_text('Usage: /history <necessary_currency>')

    get_h_dates()

    try:
        for h_date in h_dates:
            h_params = dict(access_key=settings.API_KEY, symbols='USD,' + str(currency).upper())

            try:
                historical_resp = requests.get(url=api_url + str(h_date), params=h_params)
                converted_resp = historical_resp.json()['rates'][currency.upper()] / \
                                 historical_resp.json()['rates']['USD']
                h_data.append(float(Decimal(converted_resp).quantize(Decimal("1.00"))))

            except ConnectionError:
                update.message.reply_text('API connection error')

    except (IndexError, ValueError, KeyError):
        update.message.reply_text('No exchange rate data is available for the selected currency')

    pylab.switch_backend('Agg')
    axes = pylab.subplot(1, 1, 1)
    pylab.title(f'Last 7 days for {currency.upper()} to USD rate', fontsize=16, fontname='Times New Roman')
    pylab.xlabel('Date', color='gray')
    pylab.ylabel('Rate', color='gray')
    pl_dates = matplotlib.dates.date2num(h_dates)
    pylab.plot_date(pl_dates, h_data, fmt="b-")
    axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m-%d'))
    for i in range(7):
        pylab.text(pl_dates[i], h_data[i], h_data[i])
    pylab.grid()
    pylab.savefig('graphchart.png')
    photo = open('graphchart.png', 'rb')
    update.message.reply_photo(photo=photo)
    photo.close()


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(settings.BOTTOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("list", list_view))
    dispatcher.add_handler(CommandHandler("exchange", exchange))
    dispatcher.add_handler(CommandHandler("history", graph_chart))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
