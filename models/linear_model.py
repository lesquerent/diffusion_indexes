from sklearn.linear_model import LinearRegression

from indexes_forcasting.functions.data_processing import create_stocks_df
import annex.constants as const
import models


def create_linear_model(period='6mo'):
    # CAC40 index linear reg
    df_price = create_stocks_df(const.tickers_CAC40_dict, period, data_type='prices', remove_nan_by='row')
    df_index = df_price['CAC40']
    df_price = df_price.drop(['CAC40'], axis=1)
    # Model

    model = LinearRegression()
    model.fit(df_price, df_index)
    model.score(df_price, df_index)
    return model


if __name__ == '__main__':
    model = create_linear_model()
    models.save_model(model, 'linear_model_v1.pickle')
