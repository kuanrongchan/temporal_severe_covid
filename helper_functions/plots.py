import plotly.graph_objects as go
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
                                   hovertemplate="Day %{x} relative to nadir<br>LSMeans %{y:.3f}"))
        fig.update_layout(title = dict(text = f"<b>{gene}</b>", x = 0.5, font= dict(size = 18, family = 'sans-serif')),
                          xaxis = dict(title = "Day relative to nadir", tickvals = np.arange(-4, 14, 1)),
                          yaxis = dict(title = "LSMeans", range = [min_max[0], min_max[1]]),
                          plot_bgcolor = "white",
                          showlegend = False)
        plots[gene] = fig
        
    return plots