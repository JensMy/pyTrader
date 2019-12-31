import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import style

style.use ('ggplot')


def generate_heatmap_from_csv(workdir, aindex, dataset):
    # Ausgabe auf einer Heatmap

    df = pd.read_csv (workdir + aindex + '_' + dataset + '.csv')

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
    plt.xticks (rotation=90)
    heatmap.set_clim (-1, 1)
    plt.tight_layout ()
    plt.show ()
