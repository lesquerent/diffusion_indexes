import pandas as pd
import yfinance as yf
import annex.constants as const
from ml_models.functions import save_model


def get_tickers_in_dict(excel_file_path, sheet_name_stock):
    """


    Parameters
    ----------
    excel_file_path : str
        Path of the excel file containing the tickers.
    sheet_name_stock : str
        Name of the excel sheet where the tickers are located.

    Returns
    -------
    tickers_dict : dict
        Dictionary containing key = Stock, value=ticker.

    """

    tickers_dict = pd.read_excel(excel_file_path, usecols="A,C", sheet_name=sheet_name_stock, index_col=0)[
        "Ticker"].to_dict()
    return tickers_dict


def create_stocks_df_date(my_dict, start_date='2020-01-01', end_date='2021-03-12', data_type='returns', remove_nan_by='row'):
    """

    Parameters
    ----------
    my_dict : dict
        Dictionary containing key = Stock, value=ticker.
    start_date: str
        Corresponding to the beginning of the history.
        format : AAAA-MM-DD
        Default : '2020-01-01'
    end_date: str
        Corresponding to the end of the history
        format : AAAA-MM-DD
        Default : 2021-03-12
    data_type : str
        'returns' ou 'prices', cor corresponds to the type of data we want.
        Default : 'returns'
    remove_nan_by : str
        'row' ou 'col' corresponds to the method of removal of NaN.
        Default : 'row'

    Returns
    -------
    dataFrame : pd.DataFrame
        Corresponds to a dataframe containing prices or returns at the close of the share for
        all dates of the selected period.


    """

    # //////Test on parameters\\\\\\#
    try:
        assert data_type == 'prices' or data_type == 'returns'
    except AssertionError:
        print("!!ERROR!! create_stocks_df accepts only data_type='prices' or data_type='returns' !!ERROR!!")
        return

    try:
        assert remove_nan_by == 'col' or remove_nan_by == 'row'
    except AssertionError:
        print("!!ERROR!! create_stocks_df accepts only suppr_nan_by ='col' or suppr_nan_by='row' !!ERROR!!")
        return

    # //////Data recovery\\\\\\#

    dataFrame = pd.DataFrame()

    # We browse the Tickers dictionary
    for key, value in my_dict.items():
        # Price data is retrieved at closing time
        data = yf.Ticker(value).history(start=start_date, end=end_date)["Close"]

        # If we want to recover the yields (in percentage)
        if data_type == 'returns':
            data = yf.Ticker(value).history(start=start_date, end=end_date)["Close"]
            data = data.pct_change()

        # Adds data in the form of yield or price depending on the chosen option
        try:
            dataFrame[key] = data
        except ValueError:
            print("INFO : L'action {key} ({value}) ne sera pas dans le data set.".format(key=key, value=value))

    # //////Removal of NaN\\\\\\#
    # If you want to delete columns that contain NaN
    if remove_nan_by == 'col':
        # If we are in the case of yield we must delete the first line because the calculation
        # of yields induces NaN on the first line.
        if data_type == 'returns':
            # Look for lines that have NaN
            index_with_nan = dataFrame.index[dataFrame.isnull().any(axis=1)].tolist()
            # Removes the first one induced by the returns of the data frame
            dataFrame.drop(index_with_nan[0], 0, inplace=True)
            # Searches for columns that have NaN
            column_with_nan = dataFrame.columns[dataFrame.isnull().any()].tolist()
            # Deletes these columns
            dataFrame.drop(column_with_nan, 1, inplace=True)

        else:  # case data_type=prices
            # Searches for columns that have NaN
            column_with_nan = dataFrame.columns[dataFrame.isnull().any()].tolist()
            # Deletes these columns
            dataFrame.drop(column_with_nan, 1, inplace=True)

    else:  # case remove_nan_by=='row'

        # Look for lines that have NaN
        index_with_nan = dataFrame.index[dataFrame.isnull().any(axis=1)].tolist()
        # Removes the first one induced by the returns of the data frame
        dataFrame.drop(index_with_nan, 0, inplace=True)

    return dataFrame


def create_stocks_df_period(my_dict, period='1mo', data_type='returns', remove_nan_by='row'):
    """

    Parameters
    ----------
    my_dict : dict
        Dictionary containing key = Stock, value=ticker.
    period : str
        Corresponds to the period required to recover the prices.
        valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        Default: '1mo'
    data_type : str
        'returns' ou 'prices', cor corresponds to the type of data we want.
        Default : 'returns'
    remove_nan_by : str
        'row' ou 'col' corresponds to the method of removal of NaN.
        Default : 'row'

    Returns
    -------
    dataFrame : pd.DataFrame
        Corresponds to a dataframe containing prices or returns at the close of the share for
        all dates of the selected period.

    """

    # //////Test on parameters\\\\\\#
    try:
        assert data_type == 'prices' or data_type == 'returns'
    except AssertionError:
        print("!!ERROR!! create_stocks_df accepts only data_type='prices' or data_type='returns' !!ERROR!!")
        return

    try:
        assert remove_nan_by == 'col' or remove_nan_by == 'row'
    except AssertionError:
        print("!!ERROR!! create_stocks_df accepts only suppr_nan_by ='col' or suppr_nan_by='row' !!ERROR!!")
        return

    # //////Data recovery\\\\\\#

    dataFrame = pd.DataFrame()

    # We browse the Tickers dictionary
    for key, value in my_dict.items():
        # Price data is retrieved at closing time
        data = yf.Ticker(value).history(period=period)["Close"]

        # If we want to recover the yields (in percentage)
        if data_type == 'returns':
            data = yf.Ticker(value).history(period=period)["Close"]
            data = data.pct_change()

        # Adds data in the form of yield or price depending on the chosen option
        try:
            dataFrame[key] = data
        except ValueError:
            print("INFO : L'action {key} ({value}) ne sera pas dans le data set.".format(key=key, value=value))

    # //////Removal of NaN\\\\\\#
    # If you want to delete columns that contain NaN
    if remove_nan_by == 'col':
        # If we are in the case of yield we must delete the first line because the calculation
        # of yields induces NaN on the first line.
        if data_type == 'returns':
            # Look for lines that have NaN
            index_with_nan = dataFrame.index[dataFrame.isnull().any(axis=1)].tolist()
            # Removes the first one induced by the returns of the data frame
            dataFrame.drop(index_with_nan[0], 0, inplace=True)
            # Searches for columns that have NaN
            column_with_nan = dataFrame.columns[dataFrame.isnull().any()].tolist()
            # Deletes these columns
            dataFrame.drop(column_with_nan, 1, inplace=True)

        else:  # case data_type=prices
            # Searches for columns that have NaN
            column_with_nan = dataFrame.columns[dataFrame.isnull().any()].tolist()
            # Deletes these columns
            dataFrame.drop(column_with_nan, 1, inplace=True)

    else:  # case remove_nan_by=='row'

        # Look for lines that have NaN
        index_with_nan = dataFrame.index[dataFrame.isnull().any(axis=1)].tolist()
        # Removes the first one induced by the returns of the data frame
        dataFrame.drop(index_with_nan, 0, inplace=True)

    return dataFrame


if __name__ == '__main__':
    # Path to the excel file containing all the tickers
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # file_path = os.path.join(BASE_DIR, os.path.basename('annex'))
    # file_path = os.path.join(file_path, os.path.basename('ticker_stocks.xlsx'))

    ticker_stocks = const.tickers_CAC40_dict
    cac40_stocks_prices = create_stocks_df_date(ticker_stocks, start_date='2020-01-01', end_date='2021-03-15', data_type='prices')
    print(cac40_stocks_prices)
    cac40_stocks_returns = create_stocks_df_date(ticker_stocks, start_date='2020-01-01', end_date='2021-03-15', data_type='returns')
    print(cac40_stocks_returns)

    save_model(cac40_stocks_prices, 'cac40_stocks_prices_20_01_01_21_15_03.pickle')
    save_model(cac40_stocks_returns, 'cac40_stocks_returns_20_01_01_21_15_03.pickle')
