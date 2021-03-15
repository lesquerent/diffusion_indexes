from sklearn.linear_model import LinearRegression
import annex.constants as const
from data_processing import create_stocks_df_period
from ml_models import global_models
from ml_models.functions import save_model


def create_linear_model(df_price):
    # CAC40 index linear reg
    df_index = df_price['CAC40']
    df_price = df_price.drop(['CAC40'], axis=1)
    # Model

    linear_model = LinearRegression()
    linear_model.fit(df_price, df_index)
    # linear_model.score(df_price, df_index)
    return linear_model


if __name__ == '__main__':
    cac40_stocks_prices = global_models.open_model('cac40_stocks_prices_20_01_01_21_15_03.pickle')

    model = create_linear_model(cac40_stocks_prices)
    save_model(model, 'saved_trained_models/linear_model_v2_1y.pickle')
