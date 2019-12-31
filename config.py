import configparser

default_rel = "DEFAULT"
program_rel = "OPERATIONAL"
data_rel = "DATA"
ml_rel = "MaschineLearning"


def writeconfig(settingsfile, clicfg, workdir, aindex, update, mData, dataset, v, ml):
    config = configparser.ConfigParser ()

    config[program_rel] = {}
    config.set (program_rel, 'restartCluInput', clicfg)
    config.set (program_rel, 'WorkDir', workdir)
    # config.setdefault(program_rel, 'WorkDir', workdir)

    config.set (program_rel, 'runUpdater', str (update))
    config[data_rel] = {}
    config.set (data_rel, 'Index', aindex)
    config.set (data_rel, 'useDataset', str (dataset))
    config.set (data_rel, 'rebuildDataset', str (mData))
    config.set (data_rel, 'Visualize', str (v))
    config[ml_rel] = {}
    config.set (ml_rel, 'mlPreprocessor', str (ml))

    with open (settingsfile, 'w') as configfile:
        config.write (configfile)


def readconfig(settingsfile):
    configdata = []
    config = configparser.ConfigParser ()
    config.read (settingsfile)
    config.sections ()

    configdata.append (config.getboolean (program_rel, 'restartCluInput'))
    configdata.append (config[program_rel]['WorkDir'])
    configdata.append (config.getboolean (program_rel, 'runUpdater'))
    configdata.append (config[data_rel]['Index'])
    configdata.append (config[data_rel]['useDataset'])
    configdata.append (config.getboolean (data_rel, 'rebuildDataset'))
    configdata.append (config.getboolean (data_rel, 'visualize'))
    configdata.append (config.getboolean (ml_rel, "mlPreProcessor"))
    # clicfg=
    # workdir =
    # update =
    # aindex =
    # mdata=
    # dataset =
    # v =
    # ml =

    return configdata
