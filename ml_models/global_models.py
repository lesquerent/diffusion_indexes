import os
import pickle
import annex.constants as const
from data_processing import create_stocks_df_period, create_stocks_df_date
from ml_models import pca_model
from ml_models.functions import open_model


def make_prediction(data_returns, data_prices, var_model_name_file, linear_model_name_file, nb_of_forecast=1):
    # PCA
    pc_pca = pca_model.create_principal_components_array(data_returns)
    array_of_principal_components = pc_pca[0]
    pca = pc_pca[1]

    # VAR
    results = open_model(var_model_name_file)
    lag_order = results.k_ar
    array_of_forecast_pc = results.forecast(array_of_principal_components[-lag_order:], nb_of_forecast)

    forecast_return = pca.inverse_transform(array_of_forecast_pc)
    # print(forecast_return)

    # Prices prediction
    forecast_prices = data_prices * (1 + forecast_return)

    # Index prediction
    model = open_model(linear_model_name_file)
    predictions = model.predict(forecast_prices)

    return predictions[-nb_of_forecast]


def views_prediction(period='6mo'):
    # DataFrame containing CAC40 stock returns, with NaN suppression per line
    _dict_of_tickers = const.tickers_CAC40_dict
    _cac40_stocks_returns = create_stocks_df_period(_dict_of_tickers, period=period)

    # Removal of values from the CAC40 index
    _cac40_stocks_returns = _cac40_stocks_returns.drop(['CAC40'], axis=1)

    # DataFrame containing CAC40 stock returns, with NaN suppression per line
    _cac40_stocks_prices = create_stocks_df_period(const.tickers_CAC40_dict, period='1d', data_type='prices')

    # Removal of values from the CAC40 index
    _cac40_stocks_prices = _cac40_stocks_prices.drop(['CAC40'], axis=1)
    _cac40_forecast = make_prediction(_cac40_stocks_returns, _cac40_stocks_prices, 1)
    print('Cac40 forecast : {}'.format(_cac40_forecast))
    return int(round(_cac40_forecast))


if __name__ == '__main__':
    cac40_stocks_returns = open_model('cac40_stocks_returns_20_01_01_21_15_03.pickle')

    # Removal of values from the CAC40 index
    cac40_stocks_returns = cac40_stocks_returns.drop(['CAC40'], axis=1)

    # DataFrame containing CAC40 stock returns, with NaN suppression per line
    cac40_stocks_prices = open_model('cac40_stocks_prices_20_01_01_21_15_03.pickle')

    # Removal of values from the CAC40 index
    cac40_stocks_prices = cac40_stocks_prices.drop(['CAC40'], axis=1)

    cac40_forecast = make_prediction(cac40_stocks_returns, cac40_stocks_prices, 'var_model_v2_1y.pickle', 'linear_model_v2_1y.pickle', 1)
    print('Cac40 forecast : {}'.format(cac40_forecast))
