import os
from sklearn.linear_model import LinearRegression
import pickle
import annex.constants as const
from indexes_forcasting.functions.data_processing import create_stocks_df_period

from ml_models import global_models
import yfinance as yf


def open_data(file_name):
    """
        Open the model saved in ml_models/saved_trained_models/file_name
    Parameters
    ----------
    file_name : str
        Named of the model used in the path

    """
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder = os.path.join(project_dir, os.path.basename('data_pickle'))
    file_path = os.path.join(data_folder, os.path.basename(file_name))

    if os.path.exists(file_path):
        print("Loading Trained Model : {}".format(file_name))
        data = pickle.load(open(file_path, "rb"))

    else:
        print("No model named '{}', check this and retry".format(file_name))
        data = None
    return data

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

if __name__ == "__main__":
    tickers_cac40_dict_2 = {
						'Air Liquide': 'AI.PA', 'Airbus': 'AIR.PA',
						'Alstom': 'ALO.PA', 'ArcelorMittal': 'MT.AS', 'Atos': 'ATO.PA',
						'AXA': 'CS.PA', 'BNP Paribas': 'BNP.PA', 'Bouygues': 'EN.PA',
						'Capgemini': 'CAP.PA', 'Carrefour': 'CA.PA', 'Crédit Agricole': 'ACA.PA',
						'Danone': 'BN.PA', 'Dassault Systèmes': 'DSY.PA', 'Engie': 'ENGI.PA',
						'EssilorLuxottica': 'EL.PA', 'Hermès': 'RMS.PA', 'Kering': 'KER.PA',
						"L'Oréal": 'OR.PA', 'Legrand': 'LR.PA', 'LVMH': 'MC.PA',
						'Michelin': 'ML.PA', 'Orange': 'ORA.PA', 'Pernod Ricard': 'RI.PA',
						'Publicis': 'PUB.PA', 'Renault': 'RNO.PA', 'Safran': 'SAF.PA',
						'Saint-Gobain': 'SGO.PA', 'Sanofi': 'SAN.PA', 'Schneider Electric': 'SU.PA',
						'Société Générale': 'GLE.PA', 'Stellantis': 'STLA.PA',
						'STMicroelectronics': 'STM.PA', 'Teleperformance': 'TEP.PA', 'Thales': 'HO.PA',
						'Total': 'FP.PA', 'Unibail-Rodamco-Westfield': 'URW.AS', 'Veolia': 'VIE.PA',
						'Vinci': 'DG.PA', 'Vivendi': 'VIV.PA', 'Worldline': 'WLN.PA',
						'CAC40': '^FCHI'
						}

    tickers_cac40_dict = tickers_cac40_dict_2

    str_tickers = ""

    for key, value in tickers_cac40_dict.items():
        str_tickers += "{} ".format(value)


    df_stocks_prices = open_data('df_stocks_prices.pickle')

    start_date = data_stocks_values.index[-1]

    end_date="2021-03-29"
    start_date=""
    data_value = yf.download(str_tickers, start=start_date, end=end_date)["Close"]
