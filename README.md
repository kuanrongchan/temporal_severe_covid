# Genes temporally regulated by severe COVID-19

![temporal_dynamics](https://github.com/kuanrongchan/temporal_severe_covid/assets/91276553/df27d352-10ff-4687-850e-592c869342b8)

[![DOI](https://zenodo.org/badge/443649989.svg)](https://zenodo.org/doi/10.5281/zenodo.7114839)

The running instance of this webtool may be found at https://temporal-severe-covid.streamlit.app.
This webtool allows users to plot the genes that are temporally regulated during severe COVID-19 as described in the publication by Ong et al., eBioMedicine, 2021 (https://www.thelancet.com/journals/ebiom/article/PIIS2352-3964(21)00055-4/fulltext). The data plotted is based on 6 severe or moderately severe patients, and daily bloods were taken from day -4 to day 13 post respiratory nadir. Day 0 indicates day of respiratory nadir, where peak symptoms were documented. Out of 29,405 genes, 4,831 genes were temporally regulated, as determined by extraction and analysis of differential gene expression (EDGE) (FDR-adjusted p-value < 0.05; q-value < 0.05; Benjamini-Hochberg step-up procedure).

This webtool is open-source and free to use. The web tool works by running the Python programming language at backend to plot the time-series data, while the Streamlit framework is used to display the output graph.

To use the webtool, enter a comma or new-line separated list of genes or select genes from the dropdown menu in the sidebar. Line plots for each gene found in the dataset will be plotted and made available for download as a zip file containing PDF figures for each gene. Genes that were not found will be shown in an expander. Myeloid-derived suppressor cell signatures mentioned in Table 1 of [Len et al., Viruses, 2023]() is displayed in a heatmap under the <b>MDSC heatmap</b> tab for reference.

The app is jointly made by Clara Koh and Kuan Rong Chan based on the data published by Ong et al., eBioMedicine, 2021. We thank Jia Soon for providing the data on MDSC gene signatures that can be used to query against this database. For more details on what we do, feel free to visit us at kuanrongchan.com.
