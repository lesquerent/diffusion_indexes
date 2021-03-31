import datetime

import numpy as np
import sklearn
from sklearn import decomposition

from sklearn.linear_model import LinearRegression
from statsmodels.tsa.api import VAR
import pandas as pd
import matplotlib.pyplot as plt
from annex.constants import tickers_cac40_dict_2
from data_processing import create_stocks_df


# ----- PCA Model Functions
from ml_models.functions import save_data


def select_component(pca_data, percent):
    """
    Returns the number of components such that percent% of the information is explained.

    Params
    ------
        pca_data : pca data
        percent : percentage of data explained

    Returns
    -------
        index : number of components required to meet the percentage

    """
    index = 0
    var = np.cumsum(np.round(pca_data.explained_variance_ratio_, decimals=3) * 100)
    while var[index] < percent:
        index += 1
    return index


def create_pca_model(data_set):
    # Compute the mean of the data set
    mu = np.mean(data_set, axis=0)

    # Create PCA
    pca = sklearn.decomposition.PCA()
    pca.fit(data_set)

    nb_components = select_component(pca, 95)

    array_of_principal_components = pd.DataFrame(pca.transform(data_set)[:, :nb_components])

    return array_of_principal_components, pca, nb_components, mu


def inverse_pca(forecast_pc, pca, nb_components, mu):
    data_reconstructed = np.dot(forecast_pc, pca.components_[:nb_components, :])
    data_reconstructed += mu
    return data_reconstructed


# ----- VAR Model Creation Function
def create_var_model(training_set):
    var_model = VAR(training_set)
    lag_order = var_model.select_order()
    lag_order_selected = lag_order.selected_orders['aic']
    var_model_results = var_model.fit(lag_order_selected)
    return var_model_results


def forecasting_pc(var_model, data_set, nb_of_predictions=1):
    lag_order = var_model.k_ar
    forecast_pc = var_model.forecast(data_set.values[-lag_order - nb_of_predictions + 1:], nb_of_predictions)
    return forecast_pc


# ----- Multiple linear regression model creation functions
def create_linear_model(x_training_set, y_training_set):
    multiple_linear_reg_model = LinearRegression()
    multiple_linear_reg_model.fit(x_training_set, y_training_set)
    return multiple_linear_reg_model


# ----- Prediction
def make_predictions(nb_of_days_future, data_stocks_prices, data_stocks_returns, data_index_value, data_index_returns):
    df_index_forecast_based_on_prices_forecast = pd.DataFrame(columns=['^FCHI Predictions Based on prices forecast'])
    df_index_forecast_based_on_prices_forecast.index = pd.DatetimeIndex(
        df_index_forecast_based_on_prices_forecast.index)

    df_index_forecast_based_on_returns_forecast = pd.DataFrame(columns=['^FCHI Predictions Based on returns forecast'])
    df_index_forecast_based_on_returns_forecast.index = pd.DatetimeIndex(
        df_index_forecast_based_on_returns_forecast.index)

    date_past = data_stocks_prices.index[-1]
    _df_stocks_prices = data_stocks_prices[:date_past]
    _df_stocks_returns = data_stocks_returns[:date_past]
    _df_index_value = data_index_value[:date_past]
    _df_index_returns = data_index_returns[:date_past]

    pca_model = create_pca_model(_df_stocks_returns)

    df_of_principal_components = pca_model[0]

    var_model = create_var_model(df_of_principal_components)

    # Forecasting PC
    forecast_pc = forecasting_pc(var_model, df_of_principal_components, nb_of_days_future)

    # Reconstruct all components
    stocks_returns_estimators = inverse_pca(forecast_pc, pca_model[1], pca_model[2], pca_model[3])

    # Forecasting prices
    stocks_returns_estimators_p1 = stocks_returns_estimators + 1
    stocks_returns_estimators_cumprod = stocks_returns_estimators_p1

    last_prices_known = _df_stocks_prices.loc[date_past, :].values.reshape(1, -1)
    forecast_prices = last_prices_known * stocks_returns_estimators_cumprod

    # Forecasting CAC40 index based on :
    # - Forecast prices
    ml_model_prices = create_linear_model(_df_stocks_prices, _df_index_value)
    index_forecast_based_on_prices_forecast = ml_model_prices.predict(forecast_prices)

    # - Forecast returns
    ml_model_returns = create_linear_model(_df_stocks_returns, _df_index_returns)
    index_returns_estimators = ml_model_returns.predict(stocks_returns_estimators)
    index_returns_estimators_p1 = 1 + index_returns_estimators
    index_returns_estimators_cumprod = index_returns_estimators_p1

    last_index_value_known = _df_index_value.loc[_df_stocks_prices.index[-1]]
    index_forecast_based_on_returns_forecast = last_index_value_known * index_returns_estimators_cumprod

    futures_date = date_past
    # If the futures_date is in the weekend

    for i in range(len(index_forecast_based_on_prices_forecast)):
        futures_date += datetime.timedelta(days=1)
        while futures_date.weekday() >= 5:
            futures_date += datetime.timedelta(days=1)

        df_index_forecast_based_on_prices_forecast.loc[futures_date] = index_forecast_based_on_prices_forecast[i]

        df_index_forecast_based_on_returns_forecast.loc[futures_date] = index_forecast_based_on_returns_forecast[i]

    return df_index_forecast_based_on_prices_forecast, df_index_forecast_based_on_returns_forecast


# ----- Back test
def make_past_prediction_v5(nb_days_in_the_past, nb_of_pred_by_turn, df_stocks_prices_, df_stocks_returns_,
                            df_index_value_, df_index_returns_):
    # ----- DattaFrame results init
    prediction_based_on_prices = pd.DataFrame()
    prediction_based_on_returns = pd.DataFrame()

    for i in range(nb_days_in_the_past // nb_of_pred_by_turn):
        # ----- Training set init
        _last_date = df_stocks_prices_.index[-(nb_days_in_the_past - (nb_of_pred_by_turn * i))]
        df_s_v = df_stocks_prices_[:_last_date]
        df_s_r = df_stocks_returns_[:_last_date]

        df_i_v = df_index_value_[:_last_date]
        df_i_r = df_index_returns_[:_last_date]

        pred = make_predictions(nb_of_pred_by_turn, df_s_v, df_s_r, df_i_v, df_i_r)

        pred_based_on_prices = pred[0]
        pred_based_on_returns = pred[1]

        prediction_based_on_prices = prediction_based_on_prices.append(pred_based_on_prices)
        prediction_based_on_returns = prediction_based_on_returns.append(pred_based_on_returns)

    return prediction_based_on_prices, prediction_based_on_returns


if __name__ == '__main__':
    # Create CAC40 stocks dataFrames
    last_date = '2021-03-30'
    tickers_cac40_dict = tickers_cac40_dict_2
    df_prices_returns = create_stocks_df(tickers_cac40_dict, last_date)
    df_stocks_prices = df_prices_returns[0]
    df_stocks_returns = df_prices_returns[1]

    # Create CAC40 index dataFrames
    df_index_value = df_stocks_prices['^FCHI']
    df_index_returns = df_stocks_returns['^FCHI']

    del df_stocks_prices['^FCHI']
    del df_stocks_returns['^FCHI']
    nb_days = 30
    nb_pred = 5
    pred_test = make_past_prediction_v5(nb_days, nb_pred, df_stocks_prices, df_stocks_returns, df_index_value,
                                        df_index_returns)
    pred_test_prices = pred_test[0]
    pred_test_returns = pred_test[1]

    # Plot
    fig, ax = plt.subplots()
    ax.plot(pred_test_prices.index, pred_test_prices.values, label='Predictions based on forecast stocks prices')
    ax.plot(pred_test_returns.index, pred_test_returns.values, label='Predictions based on forecast index returns')
    ax.plot(df_index_value[-nb_days:].index, df_index_value[-nb_days:].values, label='True values')
    ax.legend(loc='best', shadow=True)
    plt.title('Prediction and true value of the CAC40 index for the 30 last days')
    plt.xlabel('Date')
    plt.ylabel('Index value')
    plt.show()

    save_data(pred_test_prices, 'df_history_of_forecast_prices.pickle')
    save_data(pred_test_returns, 'df_history_of_forecast_returns.pickle')

