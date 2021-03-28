# -*- coding: utf-8 -*-

import yfinance as yf
import pandas as pd
import os
from annex import constants as const


def create_stocks_df(dict_of_ticker, end_date="2021-03-28", ug_pa_file_name='ug.csv'):
    """
        Create and returns :
            a dataFrame containing all stocks and CAC40 value
            a dataFrame containing all stocks and CAC40 returns

    Parameters
    ----------
    dict_of_ticker : dict
        Dictionary containing key = Stock names, value=ticker..
    ug_pa_file_path : TYPE
        DESCRIPTION.
    end_date : TYPE, optional
        DESCRIPTION. The default is "2021-03-28".

    Returns
    -------
    data_value : pd.DataFrame
        Corresponds to a dataframe containing values at the close of the stocks for
        all dates of the selected period.
    data_returns : pd.DataFrame
        Corresponds to a dataframe containing returns at the close of the share for
        all dates of the selected period.

    """
    start_date = "2020-01-01"

    # Define the path of the UG.PA.csv file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    annex_folder = os.path.join(BASE_DIR, os.path.basename('annex'))
    ug_pa_file_path = os.path.join(annex_folder, os.path.basename('ug.csv'))
    ug_value = pd.read_csv(ug_pa_file_path, sep=';', header=0, index_col='Date', parse_dates=True)

    # Define the ticker list base on the dictionary of tickers
    str_tickers = ""

    for key, value in dict_of_ticker.items():
        str_tickers += "{} ".format(value)

    # Take stocks value from yfinance
    data_value = yf.download(str_tickers, start=start_date, end=end_date)["Close"]

    # Define the history bound of UG.PA
    ug_index = ug_value.index
    first_ug_date = ug_index[0]
    last_ug_date = ug_index[-1]

    # Replace STLA.PA by the corresponding UG.PA value before the fusion of PSA and STLA
    data_value.loc[first_ug_date:last_ug_date, 'STLA.PA'] = ug_value['UG.PA']

    # Compute returns
    data_returns = data_value.pct_change()
    # Drop the first row fill off NaN cause by the returns computing
    data_returns = data_returns.drop(first_ug_date, axis='index')

    # Fill NaN by a linear interpolation along the columns
    data_returns = data_returns.interpolate(method='linear', axis=1)

    return data_value, data_returns


if __name__ == '__main__':
    # Create CAC40 stocks dataFrames
    tickers_cac40_dict = const.tickers_cac40_dict_2
    df_prices_returns = create_stocks_df(tickers_cac40_dict)
    df_stocks_prices = df_prices_returns[0]
    df_stocks_returns = df_prices_returns[1]

    # Create CAC40 index dataFrames
    df_index_value = df_stocks_prices['^FCHI']
    df_index_returns = df_stocks_returns['^FCHI']

    del df_stocks_prices['^FCHI']
    del df_stocks_returns['^FCHI']

