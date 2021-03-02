import yfinance as yf
import pandas as pd


def Recuper_tickers_in_dict(chemin_fichier_excel, sheet_name_stock):
    """


    Parameters
    ----------
    chemin_fichier_excel : str
        Chemin du fichier excel contenant les tickers.
    sheet_name_stock : str
        Nom de la feuille excel ou se trouve les tickers.

    Returns
    -------
    tickers_dict : dict
        Dictionnaire contenant key = Stock, value=ticker..

    """

    tickers_dict = pd.read_excel(chemin_fichier_excel, usecols="A,C", sheet_name=sheet_name_stock, index_col=0)[
        "Ticker"].to_dict()
    return tickers_dict


def Creer_dataFrame_stocks(my_dict, periode, data_type, suppr_nan_by):
    """

    Parameters
    ----------
    my_dict : dict
        Dictionnaire contenant key = Stock, value=ticker.
    periode : str
        Correspond à la periode voulue pour récupérer les prix.
        valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    data_type : str
        'returns' ou 'prices, correspond au type de données que l'on veut.
    suppr_nan_by : str
        'row' ou 'col' correspond à la méthode de suppression des NaN.

    Returns
    -------
    dataFrame : pd.DataFrame
        Correspond à un dataframe contenant le prix à la cloture de l'action pour toutes les dates de la periode sélectionné.

    """

    # //////Test sur les paramètres\\\\\\#
    try:
        assert data_type == 'prices' or data_type == 'returns'

    except AssertionError:
        print("!!ERROR!! Creer_dataFrame_stocks n'accepte que data_type='prices' ou data_type='returns' !!ERROR!!")
        return

    try:
        assert suppr_nan_by == 'col' or suppr_nan_by == 'row'

    except AssertionError:
        print("!!ERROR!! Creer_dataFrame_stocks n'accepte que suppr_nan_by ='col' or suppr_nan_by='row' !!ERROR!!")
        return

    # //////Récupération des datas\\\\\\#

    dataFrame = pd.DataFrame()

    # On parcours les dictionnaire des Tickers
    for cle, value in my_dict.items():
        # On récupère les données de prix à la fermeture
        data = yf.Ticker(value).history(period=periode)["Close"]

        # Si on veut récupérer les rendements (en pourcentage)
        if data_type == 'returns':
            data = yf.Ticker(value).history(period=periode)["Close"]
            data = data.pct_change()

        # Ajoute les données sous forme de rendement ou de prix suivant l'option choisi
        dataFrame.insert(0, cle, data)

    # //////Suppression des NaN\\\\\\#
    # Si on veut supprimer les colonnes qui contiennent des NaN
    if suppr_nan_by == 'col':
        # Si on est dans le cas de rendement on doit supprimer la première ligne car le calcul des rendements induit des NaN sur la première ligne
        if data_type == 'returns':
            # Cherche les lignes qui possède des NaN
            index_with_nan = dataFrame.index[dataFrame.isnull().any(axis=1)].tolist()
            # Supprime la première induite par les retunrs du data frame
            dataFrame.drop(index_with_nan[0], 0, inplace=True)
            # Cherche les colonnes qui possède des NaN
            column_with_nan = dataFrame.columns[dataFrame.isnull().any()].tolist()
            # Supprime ces colonnes
            dataFrame.drop(column_with_nan, 1, inplace=True)

        else:  # cas data_type=prices
            # Cherche les colonnes qui possède des NaN
            column_with_nan = dataFrame.columns[dataFrame.isnull().any()].tolist()
            # Supprime ces colonnes
            dataFrame.drop(column_with_nan, 1, inplace=True)

    else:  # cas suppr_nan_by=='row'

        # Cherche les lignes qui possède des NaN
        index_with_nan = dataFrame.index[dataFrame.isnull().any(axis=1)].tolist()
        # Supprime la première induite par les retunrs du data frame
        dataFrame.drop(index_with_nan, 0, inplace=True)

    return dataFrame


if __name__ == '__main__':
    # Chemin ou se trouve le fichier excel contenant tout les tickers
    chemin_fichier_ticker = r"C:\Users\thiba\OneDrive - De Vinci\Documents\éducation\ESILV\2020-2021\S7\Pi2\ticker_stocks.xlsx"

    # Création du dictionnaire contenant tout les ticker
    tickers_CAC40_dict = Recuper_tickers_in_dict(chemin_fichier_ticker, "CAC40")
    # Supprimer les valeurs du CAC40 dans le dictionnaire
    del tickers_CAC40_dict['CAC40']
    print(tickers_CAC40_dict)
    # tickers_SP500_dict=Recuper_tickers_in_dict(chemin_fichier_ticker,"S&P500")

    # ///////////Récupération des données pour le CAC40\\\\\\\\\\\\

    # DataFrame contenant les rendement du CAC40, avec une suppression des NaN par colonne
    # df_CAC40_Returns_col=Creer_dataFrame_stocks(tickers_CAC40_dict,"5d",data_type='returns',suppr_nan_by='col')

    # DataFrame contenant les rendement du CAC40, avec une suppression des NaN par ligne
    df_CAC40_Returns_row = Creer_dataFrame_stocks(tickers_CAC40_dict, "2y", data_type='returns', suppr_nan_by='row')

    # DataFrame contenant les prix du CAC40, avec une suppression des NaN par colonne
    # df_CAC40_Price_col=Creer_dataFrame_stocks(tickers_CAC40_dict,"5d",data_type='prices',suppr_nan_by='col')

    # DataFrame contenant les prix du CAC40, avec une suppression des NaN par ligne
    # df_CAC40_Price_row=Creer_dataFrame_stocks(tickers_CAC40_dict,"5d",data_type='prices',suppr_nan_by='row')

    # //////// Si vous voulez enregistrer les données du DataFrame dans un fichier Excel :
    # df_CAC40_Returns_row.to_excel("CAC40_Returns.xlsx")
