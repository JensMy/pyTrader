import datetime as dt
import os

import fs_op
import getData
import manipulateData
import plotData


def main(workdir, aindex, update, mData, dataset, v, ml):
    # workdir = workdir + "/Files/" + aindex + "/"

    if aindex == "dax":
        aindex = "DAX"
        wikilink = "https://de.wikipedia.org/wiki/DAX"
        t_col = 1
        rstr = ""
    elif aindex == "sp500":
        aindex = "SP500"
        wikilink = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        t_col = 0
        rstr = ""
    elif aindex == "dow":
        aindex = "DOW_JONES"
        wikilink = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average#Components"
        t_col = 2
        rstr = "NYSE:"
    elif aindex == "krypto":
        aindex == "Krypto"
        wikilink = "https://de.wikipedia.org/wiki/Liste_von_Kryptow%C3%A4hrungen"
        t_col = 2
        rstr = ""
    else:
        print ("no Index added")
        os.system ('cls' if os.name == 'nt' else 'clear')
        return 0

    if dataset == "jk":
        dataset = "joined_closes"
    basedir = workdir + "/Files/"
    workdir = workdir + "/Files/" + aindex + "/"
    start = dt.datetime (1940, 1, 1)
    end = dt.datetime (2019, 12, 19)
    if not os.path.exists (workdir + "/"):
        os.makedirs (workdir + '/')

    if update == False:
        getData.safe_aind_tickers (workdir, aindex=aindex, wikilink=wikilink, t_col=t_col, rstr=rstr)
        getData.get_data_from_yahoo (workdir=workdir, start=start, end=end, aindex=aindex)
    if update == True:

        fs_op.create_tarball (basedir, aindex)
        fs_op.remove_folder (basedir, aindex)
        if not os.path.exists (workdir + "/"):
            os.makedirs (workdir + '/')
        getData.safe_aind_tickers (workdir, aindex=aindex, wikilink=wikilink, t_col=t_col, rstr=rstr)
        getData.get_data_from_yahoo (workdir=workdir, start=start, end=end, aindex=aindex)

    if mData == True:
        manipulateData.join_adjClose (workdir, aindex)
    if v == True:
        plotData.generate_heatmap_from_csv (workdir, aindex, dataset)

    if ml == True:

        lines = fs_op.list_files (workdir)

        for line in lines:
            print (line)

        print ("Which ticker do you want to analyze?:")
        ticker = input ("Ticker Name; ")
        print ("How many Days would you like to guess ajead?")
        daycount = input ("Guess Ahead Predicion; ")
        manipulateData.ml_labelprocessor (workdir, aindex, ticker, daycount, dataset)
