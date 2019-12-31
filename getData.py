import os
import pickle

import bs4 as bs
import pandas as pd
import pandas_datareader.data as web
import requests
from pandas_datareader._utils import RemoteDataError


def safe_aind_tickers(workdir, aindex, wikilink, rstr, t_col):
    # extrahiert Datensatz aus Wikipedia

    resp = requests.get (wikilink)
    soup = bs.BeautifulSoup (resp.text, 'lxml')
    table = soup.find ('table', {'class': 'wikitable sortable'})

    tickers = []
    for row in table.findAll ('tr')[1:]:
        ticker = row.findAll ('td')[t_col].text.strip ()

        ticker = ticker.replace (rstr, "")
        ticker = ticker.replace (" ", "")
        ticker = ticker.replace ("/", "")
        ticker = ticker.lstrip ()
        ticker = ticker.rstrip ()
        for x in range (0, 10):
            ticker = ticker.replace ("[" + str (x) + "]", "")

        tickers.append (ticker)
        print (ticker)

    with open (workdir + aindex + 'tickers.pickle', 'wb') as f:
        pickle.dump (tickers, f)
    os.system ('cls' if os.name == 'nt' else 'clear')
    return tickers


def get_data_from_yahoo(workdir, aindex, start, end, reload_dax=False):
    # lädt Umfangreiche Datebsätze als csv von Yahoo Finance herunter
    if reload_dax:
        tickers = safe_aindex_tickers ()
    else:
        with open (workdir + aindex + 'tickers.pickle', 'rb') as f:
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

        os.system ('cls' if os.name == 'nt' else 'clear')
