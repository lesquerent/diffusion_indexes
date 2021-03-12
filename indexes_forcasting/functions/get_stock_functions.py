# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 15:52:07 2021

@author: thiba
"""

import yfinance as yf
import pandas as pd
TICKER = '^FCHI'
PERIOD = '2y'


def take_stock_value_and_date(ticker,period):
    """


    Parameters
    ----------
    ticker : STR
        Ticker correspondant à l'indice recherche.
    period : STR
        Correspond à la periode voulue pour récupérer les prix.
        valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max.

    Returns
    -------
    list
        Liste comprenant la liste des dates et la liste des prix.

    """

    data= yf.Ticker(ticker).history(period)["High"]
    dataFrame = pd.DataFrame()

    dataFrame.insert(0,ticker,data)

    value_list = dataFrame[ticker].values.tolist()

    date_list_span = dataFrame.index.tolist()
    date_list=[]
    for date_span in date_list_span:
        date_list.append(str(date_span)[:10])

    return [date_list,value_list]

dr = take_stock_value_and_date(TICKER,PERIOD)

