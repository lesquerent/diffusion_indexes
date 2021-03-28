import numpy as np
from data_processing import *
from sklearn import decomposition
from numpy import linalg as LA
import annex.constants as const


def select_component(pca_data, percent):
    """
    Returns the number of components such that percent% of the information is explained.

    Params
    ------
        pca_data : pca data
        percent : percentage of data explained

    Returns
    -------
        index : number of components required to meet the percentage

    """
    index = 0
    var = np.cumsum(np.round(pca_data.explained_variance_ratio_, decimals=3) * 100)
    while var[index] < percent:
        index += 1
    return index


def create_principal_components_array(dict_of_tickers, end_date="2021-03-29"):
    """

    Parameters
    ----------
    dict_of_tickers : dict
        Dictionary containing key = Stock, value=ticker.
    end_date : str
        Corresponds to the last date of the historic needed.
        Format : "YYYY-MM-DD"
        Default: "2021-03-29"

    Returns
    -------
    principal_component_array : np.array
        Array containing the main components for the selected period

    """

    # DataFrame containing CAC40 stock returns
    df_cac40_prices_returns = create_stocks_df(dict_of_tickers, end_date="2021-03-29")
    cac40_stocks_returns = df_cac40_prices_returns[1]
    del cac40_stocks_returns['^FCHI']

    # PCA with sklearn module
    pca = decomposition.PCA(n_components=cac40_stocks_returns.shape[1]).fit(cac40_stocks_returns)

    # Select_component, function that calculates the number of components such that x% of the information is explained
    nb_component = select_component(pca, 95)

    array_of_principal_components = decomposition.PCA(n_components=nb_component).fit(cac40_stocks_returns)
    array_of_principal_components = array_of_principal_components.transform(cac40_stocks_returns)

    return array_of_principal_components


def marchenko_pastur_pdf1(l, Q):
    """

    Parameters
    ----------
    l : float
        Correspond to a float which will give us pdf(l)
    Q : float
        Corresponds to the

    Returns
    -------
    Value of the Marchenko Pastur Pdf evaluate in l

    """

    def m0(a):
        # Element wise maximum of (a,0)
        return np.maximum(a, np.zeros_like(a))

    l_plus = (1 + (1 / Q) ** 0.5) ** 2
    l_min = (1 - (1 / Q) ** 0.5) ** 2
    return Q * np.sqrt(m0(l_plus - l) * m0(l - l_min)) / (2 * np.pi * l)


def principal_component(dict_of_tickers, history_period='3mo'):
    # DataFrame containing CAC40 stock returns, with NaN suppression per line
    df_cac40_prices_returns = create_stocks_df(dict_of_tickers, end_date="2021-03-29")
    cac40_stocks_returns = df_cac40_prices_returns[1]

    del cac40_stocks_returns['^FCHI']

    # PCA with sklearn module
    pca = decomposition.PCA(n_components=cac40_stocks_returns.shape[1]).fit(cac40_stocks_returns)

    # Correlation matrix
    cor_matrix = cac40_stocks_returns.interpolate().corr()

    # M : number of line and  N : number de column
    M, N = cac40_stocks_returns.shape
    Q = M / N

    print(M, N)

    # Eigenvalue and eigenvector of the correlation matrix
    eigenval, eigenvec = LA.eig(cor_matrix)

    # Variance of the eigenvalues
    sigma = np.var(eigenval)

    # Array that we will return
    array_of_PC = []

    for i in range(N):
        if eigenval[i] < marchenko_pastur_pdf1(eigenval[i]):
            array_of_PC.append(eigenvec[i])

    return array_of_PC


if __name__ == '__main__':
    last_date = "2021-03-29"
    # np.array containing the principal components :
    array_of_principal_component = create_principal_components_array(const.tickers_cac40_dict_2, last_date)
    print(array_of_principal_component.shape)
