import streamlit as st
import pandas as pd
import numpy as np

from helper_functions.downloads import file_downloads
from helper_functions.query_handler import str_to_list
from helper_functions.plots import line_plot, mdsc_heatmap

# import base64

st.title("Severe COVID-19 Temporally-Regulated Genes")

with st.expander(label = "Show documentation", expanded=True):
    st.markdown('''
                <div style="text-align: justify;">
                This webtool allows users to plot the genes that are temporally regulated during severe COVID-19 as described in the publication by
                <a href=https://www.thelancet.com/journals/ebiom/article/PIIS2352-3964(21)00055-4/fulltext>Ong et al., eBioMedicine, 2021</a>.<br></br>
                The data plotted is based on 6 severe or moderately severe patients, and daily bloods were taken from day U+2212 -4 to day 13 post respiratory nadir, 
                which is defined by low (<95%) arterial oxygen levels and supplemental oxygen administration (non-invasive ventilation or mechanical ventilation) required.<br><br>
                Day 0 indicates day of respiratory nadir, where peak symptoms were documented. 
                Out of 29,405 genes, 4,831 genes were temporally regulated, as determined by extraction and analysis of differential gene expression (EDGE) (FDR-adjusted p-value < 0.05; q-value < 0.05; Benja-mini-Hochberg step-up procedure).
                
                ## Usage
                Users may query the dataset either by providing a comma-, or newline-separated list of genes or selecting from a dropdown menu in the sidebar.<br></br>
                Genes that were not found will be shown in an expander.<br></br> 
                Myeloid-derived suppressor cell signatures mentioned in Table 1 of [Len et al., Viruses, 2023]() is displayed in a heatmap under the <b>MDSC Heatmap</b> tab for reference.
                </div>
                ''',
                unsafe_allow_html=True)
    
queryPlots, heatmap = st.tabs(['Line Plots', 'MDSC Heatmap'])

lsmeans = st.cache_data(pd.read_csv)("data_files/Severe_COVID-19_LSmeans.csv", index_col=0)
possible_genes = sorted(lsmeans.index.to_list())

queryExp = st.sidebar.expander("Query options", expanded = True)
geneQuery = queryExp.text_area("Enter a list of gene symbols (comma or new line-separated)") # accepts user list

with queryExp:
    userGeneList = str_to_list(geneQuery)

# don't know what genes to use? Have multi-select options...
geneMultiselect = queryExp.multiselect("Not sure what genes to input? Select genes here 👇", options = possible_genes, default = possible_genes[0:4])

combined_list = set(userGeneList).union(set(geneMultiselect))
confirmIn = sorted([i for i in possible_genes if i in combined_list])

if len(combined_list) != len(confirmIn):
    notFound = pd.Series(list(set(combined_list).difference(set(confirmIn))), name="NotFound")
    with st.expander("Genes not found in dataset", expanded = True):
        st.warning("Some genes were not found to be temporally regulated in the Ong et al (2021) article. See list below for more details.", icon = "⚠️")
        st.dataframe(notFound)
    

if len(confirmIn) != 0:
    outFig = line_plot(lsmeans, confirmIn)
    _ = [queryPlots.plotly_chart(v, theme=None) for k,v in outFig.items()]
    with queryPlots:
        file_downloads.zip_imgs(file_downloads.plots_to_buffer(outFig, graph_module="plotly", format = 'pdf'), format = "pdf", zipfilename="line_plots.zip")
    
else:
    st.warning("Please enter a gene in the sidebar or select from the dropdown menu.", icon = '⬅️')

heatmap.pyplot(mdsc_heatmap(lsmeans))
# with open("data_files/mdscSigclustermap.pdf", "rb") as f:
#     base64_pdf = base64.b64encode(f.read()).decode('utf-8')

#     # Embedding PDF in HTML
#     pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf" style="border:none;"></iframe>'

#     # Displaying File
#     heatmap.markdown(pdf_display, unsafe_allow_html=True)
