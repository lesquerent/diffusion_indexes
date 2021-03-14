import os
import pickle

from sklearn import decomposition

from annex import constants as const
from indexes_forcasting.functions.data_processing import create_stocks_df_period
import annex
from ml_models import pca_model


def save_model(my_model, file_name):  # ex : file_name = "trained_model.pickle"
    base_dir = '/'
    file_path = base_dir + file_name
    if os.path.exists(file_path):
        print("Model already exists")

    else:
        with open(file_path, "wb") as file:
            pickle.dump(my_model, file)
            print('Trained Model Saved')


def open_model(file_name):
    base_dir = 'ml_models\\saved_trained_models'
    # base_dir = 'saved_trained_models'
    file_path = os.path.join(base_dir, file_name)
    print('file path : {}'.format(file_path))
    if os.path.exists(file_path):
        print("Loading Trained Model")
        model = pickle.load(open(file_path, "rb"))

    else:
        print('No model with this name, check this and retry')
        model = None
    return model


def make_prediction(data_returns, data_prices, nb_of_forecast=1):
    # PCA
    pc_pca = pca_model.create_principal_components_array(data_returns)
    array_of_principal_components = pc_pca[0]
    pca = pc_pca[1]

    # VAR
    results = open_model('var_model_v1.pickle')
    lag_order = results.k_ar
    array_of_forecast_pc = results.forecast(array_of_principal_components[-lag_order:], nb_of_forecast)

    forecast_return = pca.inverse_transform(array_of_forecast_pc)
    # print(forecast_return)

    # Prices prediction
    forecast_prices = data_prices * (1 + forecast_return)

    # Index prediction
    model = open_model('linear_model_v1.pickle')
    predictions = model.predict(forecast_prices)

    return predictions[-nb_of_forecast]


def views_prediction(period='6mo'):
    # DataFrame containing CAC40 stock returns, with NaN suppression per line
    _dict_of_tickers = annex.constants.tickers_CAC40_dict
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
    # DataFrame containing CAC40 stock returns, with NaN suppression per line
    dict_of_tickers = annex.constants.tickers_CAC40_dict
    cac40_stocks_returns = create_stocks_df_period(dict_of_tickers, period='6mo')

    # Removal of values from the CAC40 index
    cac40_stocks_returns = cac40_stocks_returns.drop(['CAC40'], axis=1)

    # DataFrame containing CAC40 stock returns, with NaN suppression per line
    cac40_stocks_prices = create_stocks_df_period(const.tickers_CAC40_dict, period='1d', data_type='prices')

    # Removal of values from the CAC40 index
    cac40_stocks_prices = cac40_stocks_prices.drop(['CAC40'], axis=1)

    cac40_forecast = make_prediction(cac40_stocks_returns, cac40_stocks_prices, 1)
    print('Cac40 forecast : {}'.format(cac40_forecast))
