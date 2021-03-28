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


def create_stocks_df(dict_of_ticker,end_date="2021-03-28", ug_pa_file_name='ug.csv'):
    """
        Create and returns :
            a dataFrame containing all stocks and CAC40 value
            a dataFrame containing all stocks and CAC40 returns

    Parameters
    ----------
    dict_of_ticker : dict
        Dictionary containing key = Stock names, value=ticker..
    ug_pa_file_name : str
        Name of the file containing UG.PA data. The default is 'ug.csv'
    end_date : str, optional
        The date until we take data. Format : 'YYYY-MM-DD' The default is "2021-03-28".

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
    ug_value = pd.read_csv(ug_pa_file_path, sep =';',header=0, index_col='Date',parse_dates=True)

    # Define the ticker list base on the dictionnary of tickers
    str_tickers =""

    for key,value in tickers_cac40_dict.items():
        str_tickers +="{} ".format(value)

    # Take stocks value from yfinance
    data_value = yf.download(str_tickers, start=start_date, end=end_date)["Close"]

    # Define the history bound of UG.PA
    ug_index =ug_value.index
    first_ug_date = ug_index[0]
    last_ug_date = ug_index[-1]

    # Replace STLA.PA by the corresponding UG.PA value before the fusion of PSA and STLA
    data_value.loc[first_ug_date:last_ug_date,'STLA.PA'] = ug_value['UG.PA']

    # Compute returns
    data_returns = data_value.pct_change()
    # Drop the first row fill off NaN cause by the returns computing
    data_returns = data_returns.drop(first_ug_date, axis='index')

    # Fill NaN by a linear interpolation along the columns
    data_returns = data_returns.interpolate(method='linear', axis=1)

    return data_value,data_returns

if __name__ == '__main__':
    # Path to the excel file containing all the tickers
    ticker_file_path = r"C:\Users\thiba\OneDrive - De Vinci\Documents\éducation\ESILV\2020-2021\S8\pi2\diffusion_indexes\annex\ticker_stocks.xlsx "

    # Creation of the dictionary containing all the tickers
    # tickers_CAC40_dict = get_tickers_in_dict(ticker_file_path, "CAC40")
    # print(tickers_CAC40_dict)
    # Delete CAC40 values in the dictionary
    # del tickers_CAC40_dict['CAC40']
    # print(tickers_CAC40_dict)
    # tickers_SP500_dict=get_tickers_in_dict(ticker_file_path,"S&P500")


    # Create CAC40 stocks dataFrames
    df_prices_returns = create_stocks_df(tickers_cac40_dict)
    df_stocks_prices = df_prices_returns[0]
    df_stocks_returns = df_prices_returns[1]

    # Create CAC40 index dataFrames
    df_index_value =df_stocks_prices['^FCHI']
    df_index_returns = df_stocks_returns['^FCHI']

    del df_stocks_prices['^FCHI']
    del df_stocks_returns['^FCHI']