from sklearn.linear_model import LinearRegression

from indexes_forcasting.functions.data_processing import create_stocks_df_period
import annex.constants as const
import global_models


def create_linear_model(period='6mo'):
    # CAC40 index linear reg
    df_price = create_stocks_df_period(const.tickers_CAC40_dict, period, data_type='prices', remove_nan_by='row')
    df_index = df_price['CAC40']
    df_price = df_price.drop(['CAC40'], axis=1)
    # Model

    linear_model = LinearRegression()
    linear_model.fit(df_price, df_index)
    # linear_model.score(df_price, df_index)
    return linear_model


if __name__ == '__main__':
    model = create_linear_model('1y')
    global_models.save_model(model, 'saved_trained_models/linear_model_v2_1y.pickle')
