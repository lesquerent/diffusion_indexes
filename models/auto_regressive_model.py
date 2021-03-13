import matplotlib.pyplot as plt
from statsmodels.tsa.api import VAR
import annex.constants as const
import models

from pca import *


def create_var_model(training_set):
    """

    :param training_set: dataset for training
    :return:
        var_model : the statsmodels.tsa.api.VAR model corresponding to the dataset
        lag_order : corresponding to the lag order of the model
    """
    var_model = VAR(training_set)

    var_model.select_order()
    var_model = var_model.fit(ic='aic')
    lag_order = var_model.k_ar
    return var_model, lag_order


def main2():
    # period = '2y'
    # array_of_principal_component = create_principal_components_array(const.tickers_CAC40_dict, period)
    # # Create train and test set
    #
    # # Creation of the VAR model
    # model = create_var_model(array_of_principal_component)[0]
    # models.save_model(model, 'var_model_2y_v1.pickle')
    # Plotting input time series:

    var_model = models.open_model('var_model_2y_v1.pickle')
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


def main1():
    period = '6mo'
    # Create train and test set
    array_of_principal_component = np.array([[-0.00739105, -0.02305929, -0.02998845, -0.0181435, -0.00411993],
                                             [-0.07759111, -0.02769151, -0.01018943, 0.00548652, -0.01850119],
                                             [0.06334292, 0.01916812, 0.01537566, -0.01334124, -0.01736806],
                                             [0.03864517, 0.00888155, 0.00480103, 0.01205922, 0.00105049],
                                             [0.00148886, -0.02164409, 0.04803721, 0.08797021, 0.05544501],
                                             [0.03628522, -0.0006689, 0.00915828, 0.00108643, -0.00698304],
                                             [0.05995416, -0.0036684, -0.02873346, 0.0046079, -0.00534844],
                                             [-0.01974782, -0.00830584, 0.02531814, -0.00089273, 0.00990051],
                                             [-0.05784584, -0.05937998, -0.01889895, -0.02594667, -0.05443161],
                                             [0.00930868, 0.03609237, -0.0004026, 0.01293472, -0.02264252],
                                             [-0.00876826, -0.00170654, -0.01257848, 0.00934594, -0.00518553],
                                             [0.04833158, 0.01489079, 0.01491801, -0.00492795, -0.00189086],
                                             [0.16209154, -0.02646623, -0.00324927, -0.00808532, 0.00776848],
                                             [-0.08304331, 0.02068485, -0.02057977, -0.0057745, -0.04108215],
                                             [-0.10466697, -0.00895596, -0.01241946, 0.02995045, 0.00072432],
                                             [0.01500323, -0.0123753, 0.00073876, 0.01865936, -0.00597334],
                                             [-0.03844717, 0.06503594, 0.00696404, -0.02825747, 0.01219281],
                                             [0.00383828, 0.01235622, -0.0157568, 0.0173594, -0.0025585],
                                             [0.02355485, -0.00144891, -0.003654, -0.0184077, -0.01198016],
                                             [0.05392045, -0.02692846, -0.005582, 0.01653781, -0.00875687],
                                             [-0.02129791, 0.06045555, 0.03100667, -0.06844746, -0.02600335],
                                             [-0.00473509, -0.01260645, 0.00891706, 0.02797532, -0.02720809],
                                             [-0.13204954, -0.00409928, 0.02358676, 0.02782418, 0.02546161],
                                             [-0.03875233, -0.06709157, 0.10830183, -0.0771394, 0.05584428],
                                             [-0.01829513, 0.06907672, -0.0963976, -0.04228844, 0.08286972],
                                             [0.06672694, -0.01777831, 0.01887499, 0.00241302, -0.01494472],
                                             [-0.0281741, -0.01391157, 0.00362152, 0.00728696, 0.01163819],
                                             [0.00731646, 0.12075377, 0.05982303, 0.03415278, -0.01903341],
                                             [-0.04310025, -0.03247746, -0.06978119, 0.01660314, 0.01344106],
                                             [0.08158428, -0.00721101, -0.02552157, 0.00482874, 0.03327702],
                                             [0.01251324, -0.04992081, -0.02570997, -0.0254297, -0.01560174]])

    training_set = np.array([[-0.00739105, -0.02305929, -0.02998845, -0.0181435, -0.00411993],
                             [-0.07759111, -0.02769151, -0.01018943, 0.00548652, -0.01850119],
                             [0.06334292, 0.01916812, 0.01537566, -0.01334124, -0.01736806],
                             [0.03864517, 0.00888155, 0.00480103, 0.01205922, 0.00105049],
                             [0.00148886, -0.02164409, 0.04803721, 0.08797021, 0.05544501],
                             [0.03628522, -0.0006689, 0.00915828, 0.00108643, -0.00698304],
                             [0.05995416, -0.0036684, -0.02873346, 0.0046079, -0.00534844],
                             [-0.01974782, -0.00830584, 0.02531814, -0.00089273, 0.00990051],
                             [-0.05784584, -0.05937998, -0.01889895, -0.02594667, -0.05443161],
                             [0.00930868, 0.03609237, -0.0004026, 0.01293472, -0.02264252],
                             [-0.00876826, -0.00170654, -0.01257848, 0.00934594, -0.00518553],
                             [0.04833158, 0.01489079, 0.01491801, -0.00492795, -0.00189086],
                             [0.16209154, -0.02646623, -0.00324927, -0.00808532, 0.00776848],
                             [-0.08304331, 0.02068485, -0.02057977, -0.0057745, -0.04108215],
                             [-0.10466697, -0.00895596, -0.01241946, 0.02995045, 0.00072432],
                             [0.01500323, -0.0123753, 0.00073876, 0.01865936, -0.00597334],
                             [-0.03844717, 0.06503594, 0.00696404, -0.02825747, 0.01219281],
                             [0.00383828, 0.01235622, -0.0157568, 0.0173594, -0.0025585],
                             [0.02355485, -0.00144891, -0.003654, -0.0184077, -0.01198016],
                             [0.05392045, -0.02692846, -0.005582, 0.01653781, -0.00875687],
                             [-0.02129791, 0.06045555, 0.03100667, -0.06844746, -0.02600335],
                             [-0.00473509, -0.01260645, 0.00891706, 0.02797532, -0.02720809],
                             [-0.13204954, -0.00409928, 0.02358676, 0.02782418, 0.02546161],
                             [-0.03875233, -0.06709157, 0.10830183, -0.0771394, 0.05584428],
                             [-0.01829513, 0.06907672, -0.0963976, -0.04228844, 0.08286972],
                             [0.06672694, -0.01777831, 0.01887499, 0.00241302, -0.01494472],
                             [-0.0281741, -0.01391157, 0.00362152, 0.00728696, 0.01163819],
                             [0.00731646, 0.12075377, 0.05982303, 0.03415278, -0.01903341],
                             [-0.04310025, -0.03247746, -0.06978119, 0.01660314, 0.01344106]])

    test_set = np.array([[-0.00739105, -0.02305929, -0.02998845, -0.0181435, -0.00411993],
                         [-0.07759111, -0.02769151, -0.01018943, 0.00548652, -0.01850119],
                         [0.06334292, 0.01916812, 0.01537566, -0.01334124, -0.01736806],
                         [0.03864517, 0.00888155, 0.00480103, 0.01205922, 0.00105049],
                         [0.00148886, -0.02164409, 0.04803721, 0.08797021, 0.05544501],
                         [0.03628522, -0.0006689, 0.00915828, 0.00108643, -0.00698304],
                         [0.05995416, -0.0036684, -0.02873346, 0.0046079, -0.00534844],
                         [-0.01974782, -0.00830584, 0.02531814, -0.00089273, 0.00990051],
                         [-0.05784584, -0.05937998, -0.01889895, -0.02594667, -0.05443161],
                         [0.00930868, 0.03609237, -0.0004026, 0.01293472, -0.02264252],
                         [-0.00876826, -0.00170654, -0.01257848, 0.00934594, -0.00518553],
                         [0.04833158, 0.01489079, 0.01491801, -0.00492795, -0.00189086],
                         [0.16209154, -0.02646623, -0.00324927, -0.00808532, 0.00776848],
                         [-0.08304331, 0.02068485, -0.02057977, -0.0057745, -0.04108215],
                         [-0.10466697, -0.00895596, -0.01241946, 0.02995045, 0.00072432],
                         [0.01500323, -0.0123753, 0.00073876, 0.01865936, -0.00597334],
                         [-0.03844717, 0.06503594, 0.00696404, -0.02825747, 0.01219281],
                         [0.00383828, 0.01235622, -0.0157568, 0.0173594, -0.0025585],
                         [0.02355485, -0.00144891, -0.003654, -0.0184077, -0.01198016],
                         [0.05392045, -0.02692846, -0.005582, 0.01653781, -0.00875687],
                         [-0.02129791, 0.06045555, 0.03100667, -0.06844746, -0.02600335],
                         [-0.00473509, -0.01260645, 0.00891706, 0.02797532, -0.02720809],
                         [-0.13204954, -0.00409928, 0.02358676, 0.02782418, 0.02546161],
                         [-0.03875233, -0.06709157, 0.10830183, -0.0771394, 0.05584428],
                         [-0.01829513, 0.06907672, -0.0963976, -0.04228844, 0.08286972],
                         [0.06672694, -0.01777831, 0.01887499, 0.00241302, -0.01494472],
                         [-0.0281741, -0.01391157, 0.00362152, 0.00728696, 0.01163819],
                         [0.00731646, 0.12075377, 0.05982303, 0.03415278, -0.01903341],
                         [-0.04310025, -0.03247746, -0.06978119, 0.01660314, 0.01344106],
                         [0.08158428, -0.00721101, -0.02552157, 0.00482874, 0.03327702],
                         [0.01251324, -0.04992081, -0.02570997, -0.0254297, -0.01560174]])
    array_of_principal_component = create_principal_components_array(const.tickers_CAC40_dict, period)
    training_set = array_of_principal_component

    # Creation of the VAR model
    model = VAR(training_set)

    model.select_order()
    results = model.fit(ic='aic')

    # Plotting input time series:
    # results.plot()

    # Plotting time series autocorrelation function:
    # results.plot_acorr()

    print(results.summary())
    lag_order = results.k_ar
    print('Lag order = {}'.format(lag_order))

    results.forecast(array_of_principal_component[-lag_order:], 5)
    results.forecast(test_set[-lag_order:], 13)
    results.plot_forecast(13)

    index = np.linspace(0, 40, 31)
    plt.plot(test_set[:, 4])
    plt.show()


if __name__ == '__main__':
    main1()
    # main2()
