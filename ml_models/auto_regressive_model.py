import numpy as np
from sklearn import decomposition

from ml_models import global_models
import matplotlib.pyplot as plt
from statsmodels.tsa.api import VAR
from annex import constants as const
from ml_models.pca_model import create_principal_components_array, select_component


def create_var_model(data):
    var_model = VAR(data)
    results = var_model.fit(ic='aic')
    # lag_order = results.k_ar
    # print('lag order : {}'.format(lag_order))
    return results


def main2():
    # period = '2y'
    # array_of_principal_component = create_principal_components_array(const.tickers_CAC40_dict, period)
    # # Create train and test set
    #
    # # Creation of the VAR model
    # model = create_var_model(array_of_principal_component)[0]
    # ml_models.save_model(model, 'var_model_2y_v1.pickle')
    # Plotting input time series:

    var_model = global_models.open_model('var_model_2y_v1.pickle')
    var_model.plot()
    plt.show()

    # Plotting time series autocorrelation function:
    # model.plot_acorr()

    # print(model.summary())
    # lag_order = model.k_ar
    # print('Lag order = {}'.format(lag_order))
    #
    # model.forecast(array_of_principal_component[-lag_order:], 5)
    # model.plot_forecast(13)
    #
    # index = np.linspace(0, 40, 31)
    # plt.show()


if __name__ == '__main__':
    # main1()
    # main2()
    # DataFrame containing CAC40 stock returns, with NaN suppression per line
    cac40_stocks_returns = global_models.open_model('cac40_stocks_returns_20_01_01_21_15_03.pickle')

    # Removal of values from the CAC40 index
    cac40_stocks_returns = cac40_stocks_returns.drop(['CAC40'], axis=1)

    # PCA with sklearn module
    pca = decomposition.PCA(n_components=cac40_stocks_returns.shape[1]).fit(cac40_stocks_returns)

    # Select_component, function that calculates the number of components such that x% of the information is explained
    nb_component = select_component(pca, 95)

    array_of_principal_components = decomposition.PCA(n_components=cac40_stocks_returns.shape[1]).fit(
        cac40_stocks_returns)

    array_of_principal_components = array_of_principal_components.transform(cac40_stocks_returns)
    model = create_var_model(array_of_principal_components)

    global_models.save_model(model, 'saved_trained_models/var_model_v2_1y.pickle')
