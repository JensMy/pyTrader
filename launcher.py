import aindexer


# Main Methode zum Aufruf der Aindexer Funktion

def launch():
    # working
    workdir = ".."
    aindexer.main (workdir=workdir, aindex="dax", wikilink="https://de.wikipedia.org/wiki/DAX", t_col=1, v=False)
    # working
    aindexer.main (workdir=workdir, aindex="sp500",
                   wikilink="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", t_col=0, v=False)
    # need to Filter out EXCHANGE Listing
    aindexer.main (workdir=workdir, aindex="dow",
                   wikilink="https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average#Components",
                   t_col=2, v=False)
    # need to Seperate BTC/XBT into 2 seperate Tickers
    aindexer.main (workdir=workdir, aindex="krypto",
                   wikilink="https://de.wikipedia.org/wiki/Liste_von_Kryptow%C3%A4hrungen", t_col=2, v=False)


launch ()
