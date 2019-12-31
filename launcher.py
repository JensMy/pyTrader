import os
import time

import aindexer
import config


# Main Methode zum Aufruf der Aindexer Funktion
def configure():
    workdir = ".."

    print ("Which Index do you want to process?:")
    aindex = input ("Ticker Name; ")
    print ("Do you want to update the Dataset?:")
    updateval = input ("y/n; ")
    if updateval == "y":
        update = True
        mData = True
    else:
        update = False
        mData = False
    # print ("which Dataset do you want to process?:")
    # ticker = input ("jk / : ")

    print ("Do you want to Visualize the Dataset?:")
    vval = input ("y/n; ")
    if vval == "y":
        v = True
    else:
        v = False

    ml = False

    os.system ('cls' if os.name == 'nt' else 'clear')
    print ("You decided to continue with the index :" + aindex + "\n")

    print ("if you want to safe the settings for the next run of this program type y")
    cclicfg = input ("y/n; ")
    if cclicfg == "y":
        clicfg = False
    else:
        clicfg = True

    config.writeconfig ('settings.ini', clicfg=str (clicfg), workdir=workdir, aindex=aindex, update=update, mData=mData,
                        dataset="jk", v=v, ml=ml)


def launch():
    print (config.readconfig ("settings.ini")[1])

    time.sleep (5)
    aindexer.main (config.readconfig ('settings.ini')[1],
                   config.readconfig ('settings.ini')[3],
                   config.readconfig ('settings.ini')[2],
                   config.readconfig ('settings.ini')[5],
                   config.readconfig ('settings.ini')[4],
                   config.readconfig ('settings.ini')[6],
                   config.readconfig ('settings.ini')[7])


def runner(iterations):
    i = 0
    while iterations > i:
        if not os.path.exists ('settings.ini'):
            configure ()

        #  if config.readconfig('settings.ini')[0] == False:
        #      configure ()
        #      config.writeconfig(settingsfile="settings.ini", clicfg=str(True))

        launch ()
        i = i + 1


runner (1)
