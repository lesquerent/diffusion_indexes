import yfinance as yf
import pandas as pd


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


def create_stocks_df(my_dict, period='1mo', data_type='returns', remove_nan_by='row'):
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
    ticker_file_path = r"C:\Users\thiba\OneDrive - De Vinci\Documents\éducation\ESILV\2020-2021\S7\Pi2\ticker_stocks" \
                       r".xlsx "

    # Creation of the dictionary containing all the tickers
    # tickers_CAC40_dict = get_tickers_in_dict(ticker_file_path, "CAC40V2")
    # Delete CAC40 values in the dictionary
    # del tickers_CAC40_dict['CAC40']
    # print(tickers_CAC40_dict)
    # tickers_SP500_dict=get_tickers_in_dict(ticker_file_path,"S&P500")

    # ///////////CAC40 Data Collection\\\\\\\\\\\\

    # DataFrame containing CAC40 yields, with NaN suppression per column
    # df_CAC40_Returns_col=create_stocks_df(tickers_CAC40_dict,"5d",data_type='returns',remove_nan_by='col')

    # DataFrame containing CAC40 yields, with NaN suppression per line
    # df_CAC40_Returns_row = create_stocks_df(tickers_CAC40_dict, "2y", data_type='returns', remove_nan_by='row')

    # DataFrame containing CAC40 prices, with NaN suppression per column
    # df_CAC40_Price_col=create_stocks_df(tickers_CAC40_dict,"5d",data_type='prices',remove_nan_by='col')

    # DataFrame containing CAC40 prices, with NaN suppression per line
    # df_CAC40_Price_row=create_stocks_df(tickers_CAC40_dict,"5d",data_type='prices',remove_nan_by='row')

    # //////// If you want to save the DataFrame data in an Excel file :
    # df_CAC40_Returns_row.to_excel("CAC40_Returns.xlsx")
