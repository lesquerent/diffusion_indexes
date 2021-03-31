import datetime
import os
import pickle
import pandas as pd

from annex import constants as const
from data_processing import create_stocks_df, update_stocks_df


def save_data(data, file_name):
    """
        Saved my_model in ml_models/saved_trained_models/file_name
    Parameters
    ----------
    data : pd.DataFrame
        Data to saved.
    file_name : str
        Named of the dataframe used in the path

    """
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder = os.path.join(project_dir, os.path.basename('data_pickle'))
    file_path = os.path.join(data_folder, os.path.basename(file_name))
    # if os.path.exists(file_path):
    #     print("Dat named '{}' already exists".format(file_name))
    #
    # else:
    with open(file_path, "wb") as file:
        pickle.dump(data, file)
        print('Trained Model Saved : {}'.format(file_name))

    return None


def open_data(file_name):
    """
        Open the model saved in ml_models/saved_trained_models/file_name
    Parameters
    ----------
    file_name : str
        Named of the model used in the path

    """
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder = os.path.join(project_dir, os.path.basename('data_pickle'))
    file_path = os.path.join(data_folder, os.path.basename(file_name))

    if os.path.exists(file_path):
        print("Loading Trained Model : {}".format(file_name))
        data = pickle.load(open(file_path, "rb"))

    else:
        print("No model named '{}', check this and retry".format(file_name))
        data = None
    return data


def need_update(data_file_name):
    data = open_data(data_file_name)
    current_date = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d')
    data_need_update = False
    if datetime.datetime.today().weekday() < 5 and datetime.datetime.today().hour >= 18 and data.index[
        -1] != current_date:
        data_need_update = True

    return data_need_update


def create_saved_df(last_date, stocks_value_file_name, stocks_returns_file_name, index_value_file_name,
                    index_returns_file_name):
    # Create CAC40 stocks dataFrames
    tickers_cac40_dict = const.tickers_cac40_dict_2
    df_prices_returns = create_stocks_df(tickers_cac40_dict, last_date)
    df_stocks_prices = df_prices_returns[0]
    df_stocks_returns = df_prices_returns[1]

    # Create CAC40 index dataFrames
    df_index_value = df_stocks_prices['^FCHI']
    df_index_returns = df_stocks_returns['^FCHI']

    del df_stocks_prices['^FCHI']
    del df_stocks_returns['^FCHI']
    stocks_value_file_name = '{}.pickle'.format(stocks_value_file_name)
    stocks_returns_file_name = '{}.pickle'.format(stocks_returns_file_name)
    index_value_file_name = '{}.pickle'.format(index_value_file_name)
    index_returns_file_name = '{}.pickle'.format(index_returns_file_name)

    save_data(df_stocks_prices, stocks_value_file_name)
    save_data(df_stocks_returns, stocks_returns_file_name)
    save_data(df_index_value, index_value_file_name)
    save_data(df_index_returns, index_returns_file_name)


def update_data(dict_of_tickers, stocks_value_file_df, stocks_returns_file_df, index_value_file_df,
                index_returns_file_df):
    # ----- Update dataframe
    update_df = update_stocks_df(dict_of_tickers, stocks_value_file_df, stocks_returns_file_df, index_value_file_df,
                                 index_returns_file_df)

    # ----- Save dataframe
    save_data(update_df[0], 'df_stocks_prices.pickle')
    save_data(update_df[1], 'df_stocks_returns.pickle')
    save_data(update_df[2], 'df_index_value.pickle')
    save_data(update_df[3], 'df_index_returns.pickle')
    return update_df[0], update_df[1], update_df[2], update_df[3]


if __name__ == '__main__':
    # last_date_ = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y-%m-%d'),
    #                                         '%Y-%m-%d')  # + datetime.timedelta(days=1)
    file_name_stocks_v = 'df_stocks_prices'
    file_name_stocks_r = 'df_stocks_returns'
    file_name_index_v = 'df_index_value'
    file_name_index_r = 'df_index_returns'
    create_saved_df('2021-03-01', file_name_stocks_v, file_name_stocks_r, file_name_index_v, file_name_index_r)
    #
    # df_s_p = open_data('df_stocks_prices.pickle')
    # df_s_r = open_data('df_stocks_returns.pickle')
    # df_i_p = open_data('df_index_value.pickle')
    # df_i_r = open_data('df_index_returns.pickle')
    #
    # end_date = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y-%m-%d'),
    #                                       '%Y-%m-%d') + datetime.timedelta(days=1)
    # update_ = update_data(const.tickers_cac40_dict_2, 'df_stocks_prices.pickle', 'df_stocks_returns.pickle',
    #                       'df_index_value.pickle', 'df_index_returns.pickle', end_date)
    # df_s_p_u = update_[0]
    # df_s_r_u = update_[1]
    # df_i_p_u = update_[2]
    # df_i_r_u = update_[3]

    print(need_update('df_stocks_prices.pickle'))
