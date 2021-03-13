from sklearn import decomposition
from sklearn.linear_model import LinearRegression

import annex.constants as const
from indexes_forcasting.functions.data_processing import create_stocks_df
from models.pca import select_component
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt


def create_forecast_return_array(dict_of_tickers, history_period='6mo'):
    """
    Parameters
    ----------
    dict_of_tickers : dict
        Dictionary containing key = Stock, value=ticker.
    history_period : str
        Corresponds to the period required to recover the prices.
        valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        Default: '3mo'
    Returns
    -------
    principal_component_array : np.array
        Array containing the main components for the selected period
    """

    # DataFrame containing CAC40 stock returns, with NaN suppression per line
    CAC40_Stocks_returns = create_stocks_df(dict_of_tickers, history_period)

    # Removal of values from the CAC40 index
    cac40_stocks_returns = CAC40_Stocks_returns.drop(['CAC40'], axis=1)

    # PCA with sklearn module
    pca = decomposition.PCA(n_components=40).fit(cac40_stocks_returns)

    # Select_component, function that calculates the number of components such that x% of the information is explained
    nb_component = select_component(pca, 95)
    print(nb_component)

    array_of_principal_components = decomposition.PCA(n_components=nb_component).fit(cac40_stocks_returns)

    array_of_principal_components = array_of_principal_components.transform(cac40_stocks_returns)

    print(array_of_principal_components.shape)

    model = VAR(array_of_principal_components)

    # x = model.select_order()
    #
    # print(x.summary())

    results = model.fit(ic='aic')
    lag_order = results.k_ar
    print('lag order : {}'.format(lag_order))
    print(array_of_principal_components)
    array_of_forecast_pc = results.forecast(array_of_principal_components[-lag_order:], 1)

    forecast_return = pca.inverse_transform(array_of_forecast_pc)

    # print(forecast_return)

    return array_of_forecast_pc

def make_prediction(period):
    forecast_return_ = create_forecast_return_array(const.tickers_CAC40_dict)
    # print(forecast_return_)
    #
    # print(forecast_return_.shape)

    # DataFrame containing CAC40 stock returns, with NaN suppression per line
    CAC40_Stocks_prices = create_stocks_df(const.tickers_CAC40_dict, period, data_type='prices')

    # Removal of values from the CAC40 index
    cac40_stocks_prices = CAC40_Stocks_prices.drop(['CAC40'], axis=1)

    forecast_prices = cac40_stocks_prices * (1 + forecast_return_)

    # print(forecast_prices)
    #
    # print(cac40_stocks_prices)

    # CAC40 index linear reg
    df_price = create_stocks_df(const.tickers_CAC40_dict, period, data_type='prices', remove_nan_by='row')
    df_index = df_price['CAC40']
    df_price = df_price.drop(['CAC40'], axis=1)
    # Model

    model = LinearRegression()
    model.fit(df_price, df_index)
    model.score(df_price, df_index)

    predictions = model.predict(forecast_prices)
    # plt.plot(df_index.index, predictions)
    # plt.show()
    return predictions[-1]

def main1():
    forecast_return_ = create_forecast_return_array(const.tickers_CAC40_dict)
    # print(forecast_return_)
    #
    # print(forecast_return_.shape)

    # DataFrame containing CAC40 stock returns, with NaN suppression per line
    CAC40_Stocks_prices = create_stocks_df(const.tickers_CAC40_dict, '2y', data_type='prices')

    # Removal of values from the CAC40 index
    cac40_stocks_prices = CAC40_Stocks_prices.drop(['CAC40'], axis=1)

    forecast_prices = cac40_stocks_prices * (1 + forecast_return_)

    # print(forecast_prices)
    #
    # print(cac40_stocks_prices)

    # CAC40 index linear reg
    df_price = create_stocks_df(const.tickers_CAC40_dict, "2y", data_type='prices', remove_nan_by='row')
    df_index = df_price['CAC40']
    df_price = df_price.drop(['CAC40'], axis=1)
    # Model

    model = LinearRegression()
    model.fit(df_price, df_index)
    model.score(df_price, df_index)

    predictions = model.predict(forecast_prices)
    # plt.plot(df_index.index, predictions)
    # plt.show()
    print(predictions[-1])


def main2():
    df_price = create_stocks_df(const.tickers_CAC40_dict, "6mo", data_type='prices', remove_nan_by='row')
    df_price = df_price.drop(['CAC40'], axis=1)

    print(df_price.iloc[df_price.shape[0] - 1, :])


if __name__ == "__main__":
    # main1()
    cac_prediction_6mo = int(round(make_prediction('6mo')))
    cac_prediction_2y = int(round(make_prediction('2y')))
    cac_prediction_1y = int(round(make_prediction('1y')))

    print('La prevision du CAC40 pour ce soir est {} se basant sur les données des 6 derniers mois.'.format(cac_prediction_6mo))
    print('La prevision du CAC40 pour ce soir est {} se basant sur les données des 12 derniers mois.'.format(cac_prediction_1y))
    print('La prevision du CAC40 pour ce soir est {} se basant sur les données des 24 derniers mois.'.format(cac_prediction_2y))