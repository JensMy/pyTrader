import os
import pickle

import pandas as pd


def join_adjClose(workdir, aindex):
    # extrahiert aus den Datensätzen die Adj Close Spalte

    with open (workdir + aindex + 'tickers.pickle', 'rb') as f:
        tickers = pickle.load (f)

    for count, ticker in enumerate (tickers):
        main_df = pd.DataFrame ()

    for count, ticker in enumerate (tickers):

        df = pd.read_csv (workdir + 'stock_dfs/{}.csv'.format (ticker))
        df.set_index ('Date', inplace=True)
        df.rename (columns={'Adj Close': ticker}, inplace=True)

        df.drop (['Open', 'High', 'Low', 'Close', 'Volume', '50ma'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join (df, how='outer')

        if count % 10 == 0:
            os.system ('cls' if os.name == 'nt' else 'clear')
            print (count)
    os.system ('cls' if os.name == 'nt' else 'clear')
    print (main_df)
    main_df.to_csv (workdir + aindex + '_joined_closes.csv')


def ml_labelprocessor(workdir, aindex, ticker, daycount, dataset):
    df = pd.read_csv (workdir + aindex + '_' + dataset + '.csv', index_col=0)
    tickers = df.columns.values.tolist ()
    df.fillna (0, inplace=True)
    for i in range (1, int (daycount) + 1):
        df['{}_{}d'.format (ticker, i)] = (df[ticker].shift (-1) - df[ticker]) / df[ticker]
    df.fillna (0, inplace=True)

    return tickers, df
