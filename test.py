import numpy as np
from sklearn.datasets import make_regression
import matplotlib.pyplot as plt

import yfinance as yf
import pandas as pd
# Sklearn pour une PCA simplified
from sklearn import decomposition
# Pour scaler les données
from sklearn.preprocessing import StandardScaler


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
        try:
            dataFrame[cle]=data
        except ValueError:
            print('key {} value {} ne sera pas dans le data set'.format(cle, value))


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


def select_component(pca_data, percent):
    """
    Renvoie le nombre de composante tel que percent% de l'information est expliquée

    Params
    ------
        pca_data : données de la pca
        percent : pourcentage de données expliquées

    Returns
    -------
        index : nombre de composantes nécessaire pour satisfaire le pourcentage

    """
    index = 0
    var = np.cumsum(np.round(pca_data.explained_variance_ratio_, decimals=3) * 100)
    while var[index] < percent:
        index += 1
    return index


def Create_Principal_components_array(tickers_CAC40_dict, period='3mo'):
    """

    Parameters
    ----------
    tickers_CAC40_dict : dict
        Dictionnaire contenant key = Stock, value=ticker.
    period : str
        Correspond à la periode voulue pour récupérer les prix.
        valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max

    Returns
    -------
    principal_component_array : np.array
        Array contenant les principales composantes pour la period selectionnée

    """

    # DataFrame contenant les rendements des actions du CAC40, avec une suppression des NaN par ligne
    CAC40_Stocks_returns = Creer_dataFrame_stocks(tickers_CAC40_dict, period, data_type='returns', suppr_nan_by='row')

    # Suppression des valeur de l'indice du CAC40
    CAC_40_Stocks_returns = CAC40_Stocks_returns.drop(['CAC40'], axis=1)

    # Initialise the Scaler
    scaler = StandardScaler()

    # Scaler (standardiser) les rendements
    scaler.fit(CAC40_Stocks_returns)
    pca = decomposition.PCA(n_components=31).fit(CAC40_Stocks_returns)

    # Select_component, fonction qui calcul le nombre de composante tel que x% de l'information soit expliqué
    nb_component = select_component(pca, 95)

    principal_component_array = decomposition.PCA(n_components=5).fit(CAC40_Stocks_returns)
    principal_component_array = principal_component_array.transform(CAC40_Stocks_returns)

    return principal_component_array


tickers_CAC40_dict = {'Accor': 'AC.PA', 'Air Liquide': 'AI.PA',
                      'Airbus': 'AIR.PA', 'ArcelorMittal': 'MT.AS',
                      'Atos': 'ATO.PA', 'AXA': 'CS.PA',
                      'BNP Paribas': 'BNP.PA', 'Bouygues': 'EN.PA',
                      'Capgemini': 'CAP.PA', 'Carrefour': 'CA.PA',
                      'Crédit Agricole': 'ACA.PA', 'Danone': 'BN.PA',
                      'Dassault Systèmes': 'DSY.PA', 'Engie': 'ENGI.PA',
                      'Essilor': 'EL.PA', 'Hermès': 'RMS.PA',
                      'Kering': 'KER.PA', "L'Oréal": 'OR.PA',
                      'Legrand': 'LR.PA', 'LVMH': 'MC.PA',
                      'Michelin': 'ML.PA', 'Orange': 'ORA.PA',
                      'Pernod Ricard': 'RI.PA', 'PSA': 'UG.PA',
                      'Publicis': 'PUB.PA', 'Renault': 'RNO.PA',
                      'Safran': 'SAF.PA', 'Saint-Gobain': 'SGO.PA',
                      'Sanofi': 'SAN.PA', 'Schneider Electric': 'SU.PA', 'Société Générale': 'GLE.PA',
                      'Sodexo': 'SW.PA', 'STMicroelectronics': 'STM.PA', 'Thales': 'HO.PA', 'Total': 'FP.PA',
                      'Unibail-Rodamco-Westfield': 'URW.AS', 'Veolia': 'VIE.PA', 'Vinci': 'DG.PA',
                      'Vivendi': 'VIV.PA', 'Worldline': 'WLN.PA', 'CAC40': '^FCHI'}

periode = '3mo'  # Periode de l'historique valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# np.array contenant les principales composante :

array_of_principal_component = Create_Principal_components_array(tickers_CAC40_dict, periode)
print(array_of_principal_component)


# pd.dataFrame contenant les prix des strock du CAC40 (^FCHI)
df_cac40_stock_price = Creer_dataFrame_stocks(tickers_CAC40_dict, periode, data_type='prices', suppr_nan_by='row')
df_cac40_stock_price = df_cac40_stock_price.drop(['CAC40'], axis=1)
df_cac40_stock_price.drop(df_cac40_stock_price.head(1).index, inplace=True)
