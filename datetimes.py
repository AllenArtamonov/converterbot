import math
import os
import logging

from telegram import InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram_bot_pagination import InlineKeyboardPaginator
import numpy as np

list_rates = [['AED', 3.67], ['AFN', 90.41], ['ALL', 105.07], ['AMD', 477.28], ['ANG', 1.8], ['AOA', 597.02], ['ARS', 99.45], ['AUD', 1.33], ['AWG', 1.8], ['AZN', 1.7], ['BAM', 1.68], ['BBD', 2.02], ['BDT', 85.62], ['BGN', 1.68], ['BHD', 0.38], ['BIF', 1989.27], ['BMD', 1.0], ['BND', 1.35], ['BOB', 6.9], ['BRL', 5.57], ['BSD', 1.0], ['BTC', 0.0], ['BTN', 74.98], ['BWP', 11.21], ['BYN', 2.41], ['BYR', 19600.0], ['BZD', 2.02], ['CAD', 1.24], ['CDF', 2012.0], ['CHF', 0.92], ['CLF', 0.03], ['CLP', 805.58], ['CNY', 6.38], ['COP', 3767.3], ['CRC', 629.6], ['CUC', 1.0], ['CUP', 26.5], ['CVE', 94.87], ['CZK', 22.12], ['DJF', 178.02], ['DKK', 6.4], ['DOP', 56.34], ['DZD', 136.78], ['EGP', 15.73], ['ERN', 15.0], ['ETB', 47.35], ['EUR', 0.86], ['FJD', 2.07], ['FKP', 0.73], ['GBP', 0.72], ['GEL', 3.14], ['GGP', 0.73], ['GHS', 6.1], ['GIP', 0.73], ['GMD', 52.0], ['GNF', 9640.5], ['GTQ', 7.74], ['GYD', 209.13], ['HKD', 7.78], ['HNL', 24.1], ['HRK', 6.48], ['HTG', 101.0], ['HUF', 314.66], ['IDR', 14123.75], ['ILS', 3.2], ['IMP', 0.73], ['INR', 75.0], ['IQD', 1458.92], ['IRR', 42250.01], ['ISK', 129.12], ['JEP', 0.73], ['JMD', 153.81], ['JOD', 0.71], ['JPY', 114.12], ['KES', 111.1], ['KGS', 84.79], ['KHR', 4070.97], ['KMF', 424.3], ['KPW', 900.0], ['KRW', 1166.79], ['KWD', 0.3], ['KYD', 0.83], ['KZT', 425.83], ['LAK', 10192.25], ['LBP', 1511.9], ['LKR', 201.49], ['LRD', 155.25], ['LSL', 14.76], ['LTL', 2.95], ['LVL', 0.6], ['LYD', 4.54], ['MAD', 9.06], ['MDL', 17.53], ['MGA', 3982.29], ['MKD', 53.01], ['MMK', 1864.89], ['MNT', 2850.93], ['MOP', 8.01], ['MRO', 357.0], ['MUR', 42.89], ['MVR', 15.45], ['MWK', 815.46], ['MXN', 20.15], ['MYR', 4.15], ['MZN', 63.83], ['NAD', 14.71], ['NGN', 410.49], ['NIO', 35.23], ['NOK', 8.32], ['NPR', 119.99], ['NZD', 1.39], ['OMR', 0.38], ['PAB', 1.0], ['PEN', 3.98], ['PGK', 3.51], ['PHP', 50.74], ['PKR', 175.29], ['PLN', 3.96], ['PYG', 6902.66], ['QAR', 3.64], ['RON', 4.26], ['RSD', 101.15], ['RUB', 69.43], ['RWF', 1018.3], ['SAR', 3.75], ['SBD', 8.03], ['SCR', 12.95], ['SDG', 440.49], ['SEK', 8.59], ['SGD', 1.35], ['SHP', 1.38], ['SLL', 10780.0], ['SOS', 586.0], ['SRD', 21.47], ['STD', 20697.99], ['SVC', 8.75], ['SYP', 1256.97], ['SZL', 14.72], ['THB', 33.13], ['TJS', 11.25], ['TMT', 3.51], ['TND', 2.82], ['TOP', 2.24], ['TRY', 9.48], ['TTD', 6.79], ['TWD', 27.78], ['TZS', 2302.0], ['UAH', 26.42], ['UGX', 3556.81], ['USD', 1.0], ['UYU', 43.89], ['UZS', 10683.13], ['VEF', 213830274074.31], ['VND', 22758.51], ['VUV', 112.3], ['WST', 2.58], ['XAF', 564.35], ['XAG', 0.04], ['XAU', 0.0], ['XCD', 2.7], ['XDR', 0.71], ['XOF', 564.36], ['XPF', 103.23], ['YER', 250.25], ['ZAR', 14.75], ['ZMK', 9001.2], ['ZMW', 17.15], ['ZWL', 322.0]]

a = np.vstack(list_rates)
count_of_pages = math.ceil(len(list_rates) / 10)
# b = a.split
print(type(a))

updater.idle()


# def graph_chart(update: Update, context: CallbackContext):
def graph_chart(currency):
    """Getting data about rates for last 7 days and rendering chart with this data for any currency"""
    # currency = context.args[0]
    h_data = []
    get_h_dates()
    # try:
    for h_date in h_dates:
        h_params = dict(access_key=settings.API_KEY, symbols='USD,' + str(currency).upper())
        historical_resp = requests.get(url=api_url + str(h_date), params=h_params)
        converted_resp = historical_resp.json()['rates'][currency.upper()] / historical_resp.json()['rates']['USD']
        h_data.append(float(Decimal(converted_resp).quantize(Decimal("1.00"))))
    # except (IndexError, ValueError):
    #     update.message.reply_text('Usage: /history <necessary_currency> ')
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
    pylab.show()
    # update.message.text(h_data)

graph_chart('uah')




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
            print('Connection error')
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