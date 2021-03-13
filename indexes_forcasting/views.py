from django.shortcuts import render
from django.http import HttpResponse

from .functions import value_functions, get_stock_functions
from test_files import sandbox

# Create your views here.


def home(request):
    ticker_cac = "%5EFCHI"

    previous_closure = value_functions.last_closure_value(ticker_cac)
    actual_value = value_functions.real_time_value(ticker_cac)
    forecast_value = int(round(sandbox.make_prediction('6mo')))

    context = {
        'previous_index': previous_closure,
        'current_index': actual_value,
        'forcast_indexes': forecast_value,
    }

    return render(request, 'indexes_forcasting/home/home.html', context)


def line_chartCAC40(request):
    return render(request, 'indexes_forcasting/chart/line_chart.html')


def pie_chart(request):
    labels = ['cac40', 'S&P500', 'NEXT20']
    data = ['120', '170', '50']
    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, 'indexes_forcasting/chart/line_chart.html', context)


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
    data3.append(5610)
    context = {
        'labels': labels,
        'data1': data1,
        'data2': data2,
        'data3': data3,
    }
    return render(request, 'indexes_forcasting/chart/line_chart3.html', context)
