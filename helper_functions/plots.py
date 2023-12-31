import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import math
import streamlit as st

def line_plot(dataset, geneList):
    # Plot collection
    plots = {}
    # Filter the gene list
    subset_data = dataset[dataset.index.isin(geneList)]
    x_labs = subset_data.columns.str.replace("Day ", "").to_list()
    dataArr = subset_data.values.flatten()
    min_max = (round(min(dataArr) - 0.5), round(max(dataArr) + 0.5))
    for gene in geneList:
        fig = go.Figure(go.Scatter(x = x_labs,
                                   y = subset_data.loc[gene,:],
                                   mode='lines',
                                   name = gene,
                                   line = dict(color = 'coral', width = 3),
                                   hovertemplate="Day %{x} relative to respiratory nadir<br>LSMeans %{y:.3f}"))
        fig.update_layout(title = dict(text = f"<b>{gene}</b>", x = 0.5, font= dict(size = 18, family = 'sans-serif')),
                          xaxis = dict(title = "Day relative to respiratory nadir", tickvals = np.arange(-4, 14, 1)),
                          yaxis = dict(title = "LSMeans", range = [min_max[0], min_max[1]]),
                          plot_bgcolor = "white",
                          showlegend = False)
        plots[gene] = fig
        
    return plots

def mdsc_heatmap(dataset):
    with open("data_files/M-MDSC_signature.txt", 'r') as f:
        Mmdsc = f.readlines()
        Mmdsc = [i.replace("\n", "") for i in Mmdsc]
    
    with open("data_files/PMN-MDSC_signature.txt", 'r') as f:
        PMNmdsc = f.readlines()
        PMNmdsc = [i.replace("\n", "") for i in PMNmdsc]
    
    with open("data_files/overlapping_signature.txt", 'r') as f:
        overlap = f.readlines()
        overlap = [i.replace("\n", "") for i in overlap]

    Mmdsc_exclusive = set(Mmdsc) - set(overlap)
    PMNmdsc_exclusive = set(PMNmdsc) - set(overlap)

    unionlabel = list(set(Mmdsc).union(set(PMNmdsc)))
    labeldf = pd.DataFrame(index = unionlabel)
    for l in unionlabel:
        if l in Mmdsc_exclusive:
            labeldf.loc[l, 'group'] = 'M-MDSC'
            labeldf.loc[l, 'subset'] = 'orange'
        elif l in PMNmdsc_exclusive:
            labeldf.loc[l, 'group'] = 'PMN-MDSC'
            labeldf.loc[l, 'subset'] = 'cornflowerblue'
        elif l in overlap:
            labeldf.loc[l, 'group'] = 'M- & PMN-MDSC'
            labeldf.loc[l, 'subset'] = 'lightgrey'
    
    labeldf.loc[:, 'group'] = pd.Categorical(labeldf.group, categories = ['M-MDSC', 'PMN-MDSC', 'M- & PMN-MDSC'])
    mdsc_lsmeans = dataset[dataset.index.isin(labeldf.index)]
    labeldf = labeldf.loc[mdsc_lsmeans.index,:].sort_values(by='group')
    mdsc_lsmeans = mdsc_lsmeans.loc[labeldf.index,:]

    cm = sns.clustermap(data = mdsc_lsmeans,
                         row_colors = labeldf.subset,
                         z_score=None,
                         center = 0,
                         cmap = "RdBu_r",
                         dendrogram_ratio=0.0001, # has to exist because even though there's no cluster, it still takes up space
                         col_cluster=False,
                         row_cluster=False,
                         cbar_pos = (0.98, 0.05, 0.04, 0.06),
                         cbar_kws = {'label': 'LSMeans'},
                         figsize=(8,21),
                         yticklabels=True)
    
    cm.fig.suptitle("Myeloid-Derived Suppressor Cell (MDSC) Gene Signatures", y = 1.01, fontsize = 14, fontweight = 'bold')
    cm.ax_heatmap.set(xlabel = 'Day relative to respiratory nadir')
    # add legend manually for the subset colours
    handles = [Patch(facecolor=a) for a in ['orange', 'cornflowerblue','lightgrey']]
    plt.legend(handles, ['M-MDSC', 'PMN-MDSC', 'M- & PMN-MDSC'], title='subset',
            bbox_to_anchor=(1.16, 0.98), bbox_transform=cm.fig.transFigure)
    
    # cm.savefig("mdscSigclustermap.pdf")
    return cm