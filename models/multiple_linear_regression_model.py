import annex.constants as const
from models.pca import create_principal_components_array
from indexes_forcasting.functions.data_processing import create_stocks_df
from matplotlib import pyplot as plt
import numpy as np


def coef_determination(y, pred):
    """
        Confidence level
    :param y:
    :param pred:
    :return:
    """
    u = ((y - pred) ** 2).sum()
    v = ((y - y.mean()) ** 2).sum()
    return 1 - u / v


def model(X, theta):
    """
        Creation des thetas
    :param X:
    :param theta:
    :return:
    """
    return X.dot(theta)


def cost_function(X, y, theta):
    m = len(y)
    return 1 / (2 * m) * np.sum((model(X, theta) - y) ** 2)


# Gradient
def grad(X, y, theta):
    m = len(y)
    return 1 / m * X.T.dot(model(X, theta) - y)


def gradient_descent(X, y, theta, learning_rate, n_iterations):
    cost_history = np.zeros(n_iterations)

    for i in range(0, n_iterations):
        theta = theta - learning_rate * grad(X, y, theta)
        cost_history[i] = cost_function(X, y, theta)

    return theta, cost_history


def main1():
    # Regression example :
    period = '3mo'
    # np.array containing the main components :
    array_of_principal_component = create_principal_components_array(const.tickers_CAC40_dict, period)

    # pd.dataFrame containing the returns of the stocks of the CAC40 (^FCHI)
    df_cac40_stock_returns = create_stocks_df(const.tickers_CAC40_dict, period, data_type='returns',
                                              remove_nan_by='row')

    # Remove CAC40 index from de DF
    df_cac40_stock_returns = df_cac40_stock_returns.drop(['CAC40'], axis=1)
    df_cac40_stock_returns.drop(df_cac40_stock_returns.head(1).index, inplace=True)

    x, y = array_of_principal_component[1:, :], df_cac40_stock_returns.iloc[:, 7]

    plt.scatter(x[:, 3], y)
    print(x.shape)
    print(y.shape)
    # redimention de y
    y = y.values.reshape(x.shape[0], 1)
    X = np.hstack((x, np.ones((x.shape[0], 1))))

    # Creation des theta
    theta = np.random.randn(6, 1)
    theta

    plt.scatter(x[:, 0], y)
    plt.scatter(x[:, 0], model(X, theta), c='r')
    plt.show()
    print('Cost function : {}'.format(cost_function(X, y, theta)))

    # Gadient
    n_iterations = 10000
    learning_rate = 0.01

    theta_final, cost_history = gradient_descent(X, y, theta, learning_rate, n_iterations)

    print(theta_final)

    # Predictions
    predictions = model(X, theta_final)

    plt.scatter(x[:, 4], y)
    plt.scatter(x[:, 4], predictions, c='r')
    plt.show()
    plt.plot(range(n_iterations), cost_history)
    plt.show()

if __name__ == '__main__':
   main1()