import streamlit as st

# Input handlers
def str_to_list(gene_str):
    # remove whitespace
    gene_str = gene_str.replace(" ", "").replace("\n", ",").upper()

    if len(gene_str) != 0:
    
        if "," not in gene_str:
            st.error("Please check that your delimiters are commas or new lines!", icon = '🚨')
        gene_list = gene_str.split(",")
        gene_list = [i for i in gene_list if i != ""]

    else:
        gene_list = []
    return gene_list