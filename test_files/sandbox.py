from sklearn import decomposition
from sklearn.linear_model import LinearRegression

import annex.constants as const
from indexes_forcasting.functions.data_processing import create_stocks_df_period
from ml_models.pca_model import select_component
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt
from ml_models import global_models





def main1():
    forecast_return_ = global_models.create_forecast_return_array(const.tickers_CAC40_dict)
    # print(forecast_return_)
    #
    # print(forecast_return_.shape)

    # DataFrame containing CAC40 stock returns, with NaN suppression per line
    cac40_stocks_prices = create_stocks_df_period(const.tickers_CAC40_dict, '2y', data_type='prices')

    # Removal of values from the CAC40 index
    cac40_stocks_prices = cac40_stocks_prices.drop(['CAC40'], axis=1)

    forecast_prices = cac40_stocks_prices * (1 + forecast_return_)

    # CAC40 index linear reg
    df_price = create_stocks_df_period(const.tickers_CAC40_dict, "2y", data_type='prices', remove_nan_by='row')
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
    df_price = create_stocks_df_period(const.tickers_CAC40_dict, "6mo", data_type='prices', remove_nan_by='row')
    df_price = df_price.drop(['CAC40'], axis=1)

    print(df_price.iloc[df_price.shape[0] - 1, :])


if __name__ == "__main__":
    # main1()
    cac_prediction_6mo = int(round(global_models.make_prediction('6mo')))
    # cac_prediction_2y = int(round(make_prediction('2y')))
    # cac_prediction_1y = int(round(make_prediction('1y')))

    print('La prevision du CAC40 pour ce soir est {} se basant sur les données des 6 derniers mois.'.format(
        cac_prediction_6mo))
    # print('La prevision du CAC40 pour ce soir est {} se basant sur les données des 12 derniers mois.'.format(cac_prediction_1y))
    # print('La prevision du CAC40 pour ce soir est {} se basant sur les données des 24 derniers mois.'.format(cac_prediction_2y))
