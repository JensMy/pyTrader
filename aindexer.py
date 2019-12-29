import datetime as dt
import os
import pickle

import bs4 as bs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import requests
from matplotlib import style
from pandas_datareader._utils import RemoteDataError

style.use ('ggplot')


def safe_dax_tickers(workdir, aindex, wikilink, t_col):
    # extrahiert Datensatz aus Wikipedia

    resp = requests.get (wikilink)
    soup = bs.BeautifulSoup (resp.text, 'lxml')
    table = soup.find ('table', {'class': 'wikitable sortable'})


    tickers = []
    for row in table.findAll ('tr')[1:]:
        ticker = row.findAll ('td')[t_col].text.strip ()

        for x in range(0, 10):
            ticker = ticker.replace("["+ str(x)+"]", "")



        ticker = ticker.replace(" ","")
        ticker = ticker.replace ("/", "")



        tickers.append (ticker)
        print(ticker)

    with open (workdir + aindex+ 'tickers.pickle', 'wb') as f:
        pickle.dump (tickers, f)

    return tickers

#safe_sp500_tickers ()



def get_data_from_yahoo(workdir, aindex, start, end, reload_dax=False):
    # lädt Umfangreiche Datebsätze als csv von Yahoo Finance herunter
    if reload_dax:
        tickers = safe_aindex_tickers ()
    else:
        with open (workdir + aindex+ 'tickers.pickle', 'rb') as f:
            tickers = pickle.load (f)

    if not os.path.exists (workdir + 'stock_dfs'):
        os.makedirs (workdir + 'stock_dfs')



    for ticker in tickers:

        try:
            if not os.path.exists (workdir + 'stock_dfs/{}.csv'.format (ticker)):
                df = web.DataReader (ticker, 'yahoo', start, end)
                df['50ma'] = df['Adj Close'].rolling (window=50, min_periods=0).mean ()
                df.to_csv (workdir + 'stock_dfs/{}.csv'.format (ticker))
                print (ticker + " added successfully")
            else:
                print ("Ticker from {} already availablle".format (ticker))
        except RemoteDataError:
            print ("No information for ticker " + ticker)
            df = pd.read_csv ('nan.csv', parse_dates=True, index_col=0)
            df['50ma'] = df['Adj Close'].rolling (window=50, min_periods=0).mean ()
            df.to_csv (workdir + 'stock_dfs/{}.csv'.format (ticker))
            print (ticker + " adding failed due missing dataset, replacing by nullvalues")
            continue
        except KeyError:
            df = pd.read_csv ('nan.csv', parse_dates=True, index_col=0)
            df.to_csv (workdir + 'stock_dfs/{}.csv'.format (ticker))
            print (ticker + " adding failed due missing dataset, replacing by nullvalues")
            continue


#get_data_from_yahoo ()

def compile_data(workdir, aindex):
    # extrahiert aus den Datensätzen die Adj Close Spalte

    with open (workdir + aindex + 'tickers.pickle', 'rb') as f:
        tickers = pickle.load (f)

    for count, ticker in enumerate (tickers):
        main_df = pd.DataFrame ()

    for count, ticker in enumerate (tickers):

        df = pd.read_csv (workdir + 'stock_dfs/{}.csv'.format (ticker))
        df.set_index ('Date', inplace=True)
        df.rename (columns={'Adj Close': ticker}, inplace=True)


        df.drop (['Open', 'High', 'Low', 'Close', 'Volume','50ma'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join (df, how='outer')

        if count % 10 == 0:
            print (count)

    print (main_df)
    main_df.to_csv (workdir + aindex +'_joined_closes.csv')


#compile_data ()

def visualize_data(workdir, aindex):
    # Ausgabe auf einer Heatmap

    df = pd.read_csv (workdir + aindex + '_joined_closes.csv')

    df_corr = df.corr ()

    data = df_corr.values
    fig = plt.figure ()
    ax = fig.add_subplot (1, 1, 1)
    heatmap = ax.pcolor (data, cmap=plt.cm.RdYlGn)
    fig.colorbar (heatmap)
    ax.set_xticks (np.arange (data.shape[0]) + 0.5, minor=False)
    ax.set_yticks (np.arange (data.shape[1]) + 0.5, minor=False)

    ax.invert_yaxis ()
    ax.xaxis.tick_top ()

    column_lables = df_corr.columns
    row_lables = df_corr.index
    ax.set_xticklabels (column_lables)
    ax.set_yticklabels (row_lables)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()

 #  df['AAPL'].plot()
 #  plt.show()

#visualize_data()


def main(workdir, aindex, wikilink, t_col, v):
    workdir = workdir + "/Files/" + aindex + "/"
    start = dt.datetime (1940, 1, 1)
    end = dt.datetime (2019, 12, 19)
    if not os.path.exists (workdir + aindex + "/"):
        os.makedirs (workdir + aindex + '/')
    safe_dax_tickers (workdir, aindex=aindex, wikilink=wikilink, t_col=t_col)
    get_data_from_yahoo (workdir=workdir, start=start, end=end, aindex=aindex)
    compile_data (workdir, aindex)
    if v == True:
        visualize_data (workdir, aindex)
