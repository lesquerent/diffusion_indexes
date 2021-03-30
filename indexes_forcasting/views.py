from django.shortcuts import render

from ml_models.functions import open_data
from ml_models.global_models import make_predictions
from .functions import value_functions, get_stock_functions
from ml_models import global_models


# Create your views here.


def home(request):
    ticker_cac = "%5EFCHI"

    previous_closure = value_functions.last_closure_value(ticker_cac)
    actual_value = value_functions.real_time_value(ticker_cac)

    actual_value = actual_value.replace(' ', '')
    actual_value = actual_value.replace(',', '.')
    print(actual_value)
    actual_value = actual_value.split()
    print(actual_value)
    actual_value = "".join(actual_value)
    print(actual_value)
    df_stocks_prices = open_data('df_stocks_prices.pickle')
    df_stocks_returns = open_data('df_stocks_returns.pickle')
    df_index_value = open_data('df_index_value.pickle')
    df_index_returns = open_data('df_index_returns.pickle')

    predictions = make_predictions(1, df_stocks_prices, df_stocks_returns, df_index_value, df_index_returns)
    prediction_based_on_prices = predictions[0]
    prediction_based_on_returns = predictions[1]
    forecast_value_r = round(prediction_based_on_returns.values[0][0], 2)
    forecast_value_p = round(prediction_based_on_prices.values[0][0], 2)
    forecast_value = forecast_value_p
    print(forecast_value)
    id_forecast_card = 'forcast-index-neg'
    if forecast_value > float(actual_value):
        id_forecast_card = 'forcast-index-pos'

    print(forecast_value)
    context = {
        'previous_index': previous_closure,
        'current_index': actual_value,
        'forcast_index': forecast_value,
        'id': id_forecast_card,
    }

    return render(request, 'indexes_forcasting/home/home.html', context)


def line_chart(request):
    PERIOD = '1y'
    dataCAC = get_stock_functions.take_stock_value_and_date('^FCHI', PERIOD)
    dataEUROSTOXX50 = get_stock_functions.take_stock_value_and_date('^STOXX50E', PERIOD)
    dataSP500 = get_stock_functions.take_stock_value_and_date('^GSPC', PERIOD)

    labels = dataCAC[0]
    data1 = dataCAC[1]
    data2 = dataEUROSTOXX50[1]
    data3 = dataSP500[1]
    context = {
        'labels': labels,
        'data1': data1,
        'data2': data2,
        'data3': data3,
    }
    return render(request, 'indexes_forcasting/chart/line_chart2.html', context)


def line_chart3(request):
    PERIOD = '1mo'
    dataCAC = get_stock_functions.take_stock_value_and_date('^FCHI', PERIOD)
    # dataEUROSTOXX50 = get_stock_functions.take_stock_value_and_date('^STOXX50E',PERIOD)
    # dataSP500 = get_stock_functions.take_stock_value_and_date('^GSPC',PERIOD)

    labels = dataCAC[0]
    labels.append('2021-01-21')
    data1 = dataCAC[1]
    data2 = [5450, 5468, 5532, 5570, 5610, 5654, 5654, 5625, 5650, 5603, 5610, 5670, 5700, 5700, 5650, 5612, 5660, 5618,
             5625, 5630, 5618, 5610]
    data3 = dataCAC[1].copy()
    data3.append(5610)
    context = {
        'labels': labels,
        'data1': data1,
        'data2': data2,
        'data3': data3,
    }
    return render(request, 'indexes_forcasting/chart/line_chart3.html', context)


def line_chart2(request):
    PERIOD = '1mo'
    dataCAC = get_stock_functions.take_stock_value_and_date('^FCHI', PERIOD)
    # dataEUROSTOXX50 = get_stock_functions.take_stock_value_and_date('^STOXX50E',PERIOD)
    # dataSP500 = get_stock_functions.take_stock_value_and_date('^GSPC',PERIOD)

    labels = dataCAC[0]
    labels.append('2021-01-21')
    data1 = dataCAC[1]
    data2 = [5450, 5468, 5532, 5570, 5610, 5654, 5654, 5625, 5650, 5603, 5610, 5670, 5700, 5700, 5650, 5612, 5660, 5618,
             5625, 5630, 5618, 5610]
    data3 = dataCAC[1].copy()
    forecast_value = 0
    data3.append(forecast_value)
    context = {
        'labels': labels,
        'data1': data1,
        'data2': data2,
        'data3': data3,
    }
    return render(request, 'indexes_forcasting/chart/line_chart3.html', context)
