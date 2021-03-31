import pandas as pd

import numpy as np
from django.shortcuts import render

from ml_models.functions import open_data, need_update, save_data, update_data
from ml_models.global_models import make_predictions
from .functions import value_functions, get_stock_functions
from annex import constants as const

# ----- Load data
df_stocks_prices = open_data('df_stocks_prices.pickle')
df_stocks_returns = open_data('df_stocks_returns.pickle')
df_index_value = open_data('df_index_value.pickle')
df_index_returns = open_data('df_index_returns.pickle')

# ----- Load history
df_history_of_forecast_prices = open_data('df_history_of_forecast_prices.pickle')
df_history_of_forecast_returns = open_data('df_history_of_forecast_returns.pickle')
# ----- Make prediction
predictions = make_predictions(1, df_stocks_prices, df_stocks_returns, df_index_value, df_index_returns)

# ----- Check update
if need_update('df_stocks_prices.pickle'):
    df_history_of_forecast_prices.loc[predictions[0].index[-1]] = predictions[0].values[-1]
    save_data(df_history_of_forecast_prices, 'df_history_of_forecast_prices.pickle')

    df_history_of_forecast_returns.loc[predictions[0].index[-1]] = predictions[1].values[-1]
    save_data(df_history_of_forecast_returns, 'df_history_of_forecast_returns.pickle')

    last_date_known = df_stocks_prices.index[-1]
    update_data(const.tickers_cac40_dict_2, 'df_stocks_prices.pickle', 'df_stocks_returns.pickle', 'df_index_value'
                                                                                                   '.pickle',
                'df_index_returns.pickle', last_date_known)


def home(request):
    ticker_cac = "%5EFCHI"

    # ----- Get info on index value
    previous_closure = value_functions.last_closure_value(ticker_cac)
    actual_value = value_functions.real_time_value(ticker_cac)

    # ----- Reformat previous close value
    previous_closure = previous_closure.replace(' ', '')
    previous_closure = previous_closure.replace(',', '.')
    previous_closure = previous_closure.split()
    previous_closure = "".join(previous_closure)

    # ----- Reformat actual value
    actual_value = actual_value.replace(' ', '')
    actual_value = actual_value.replace(',', '.')
    actual_value = actual_value.split()
    actual_value = "".join(actual_value)

    # ----- Get forecast values
    prediction_based_on_prices = predictions[0]
    prediction_based_on_returns = predictions[1]
    forecast_value_r = round(prediction_based_on_returns.values[0][0], 2)
    forecast_value_p = round(prediction_based_on_prices.values[0][0], 2)
    forecast_value = forecast_value_p

    # ----- Redefine id card base on the value of indexes
    id_forecast_card = 'forecast-index-neg'
    if float(forecast_value) > float(actual_value):
        id_forecast_card = 'forecast-index-pos'

    id_actual_card = 'forecast-index-neg'
    if float(actual_value) > float(previous_closure):
        id_actual_card = 'forecast-index-pos'

    # ---- Define context for the html page
    context = {
        'previous_index': previous_closure,
        'current_index': actual_value,
        'forecast_index': forecast_value,
        'id_forecast_card': id_forecast_card,
        'id_actual_card': id_actual_card,
    }

    return render(request, 'indexes_forcasting/home/home.html', context)


def home1(request):
    context = {}

    return render(request, 'indexes_forcasting/home/home1.html', context)


# ----- Not here
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


# ----- Not here
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
    labels = list(df_history_of_forecast_returns.index)
    labels = [elem.strftime('%Y-%m-%d') for elem in labels]
    data1 = list(np.round(df_index_value[labels[1]:labels[-1]].values, 2))
    data2 = list(np.round(df_history_of_forecast_returns.values[:, 0], 2))
    # data3 = list(np.round(df_history_of_forecast_prices.values[:, 0], 2))

    five_predictions = make_predictions(3, df_stocks_prices, df_stocks_returns, df_index_value, df_index_returns)

    df_pred_prices = five_predictions[1]

    pred_labels = df_pred_prices.index
    pred_labels = [elem.strftime('%Y-%m-%d') for elem in pred_labels]
    labels += pred_labels

    data4 = data1 + list(np.round(df_pred_prices.values[:, 0], 2))

    context = {
        'labels': labels,
        'data1': data1,
        'data2': data2,
        # 'data3': data3,
        'data4': data4,
    }
    return render(request, 'indexes_forcasting/chart/line_chart3.html', context)
