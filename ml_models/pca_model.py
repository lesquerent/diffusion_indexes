import numpy as np
from sklearn import decomposition
from numpy import linalg as LA
import annex.constants as const
import statsmodels
import annex
from data_processing import create_stocks_df_period


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


def create_principal_components_array(data):
    """

    Parameters
    ----------
    dict_of_tickers : dict
        Dictionary containing key = Stock, value=ticker.
    history_period : str
        Corresponds to the period required to recover the prices.
        valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        Default: '3mo'

    Returns
    -------
    principal_component_array : np.array
        Array containing the main components for the selected period

    """

    pca = decomposition.PCA(n_components=data.shape[1]).fit(data)

    # Select_component, function that calculates the number of components such that x% of the information is explained
    nb_component = select_component(pca, 95)

    array_of_pc = decomposition.PCA(n_components=data.shape[1]).fit(data)
    array_of_pc = array_of_pc.transform(data)

    return array_of_pc, pca


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
    CAC40_Stocks_returns = create_stocks_df_period(dict_of_tickers, history_period)

    # Removal of values from the CAC40 index
    cac40_stocks_returns = CAC40_Stocks_returns.drop(['CAC40'], axis=1)

    # PCA with sklearn module
    pca = decomposition.PCA(n_components=31).fit(cac40_stocks_returns)

    # Correlation matrix
    cor_matrix = CAC40_Stocks_returns.interpolate().corr()

    # M : number of line and  N : number de column
    M, N = CAC40_Stocks_returns.shape
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
    period = '3mo'  # Period of history (valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)
    dict_of_tickers = annex.constants.tickers_CAC40_dict

    cac40_stocks_returns = create_stocks_df_period(dict_of_tickers, period='1y')
    cac40_stocks_returns = cac40_stocks_returns.drop(['CAC40'], axis=1)
    # np.array containing the principal components :
    array_of_principal_components = create_principal_components_array(cac40_stocks_returns)
    print(array_of_principal_components.shape)
