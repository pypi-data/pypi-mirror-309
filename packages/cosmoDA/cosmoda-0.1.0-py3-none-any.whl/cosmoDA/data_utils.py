import os
import pandas as pd
import anndata as ad
import numpy as np

tax_levels = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus"]


def read_ibs_data(author, level, data_dir):

    # read data
    subdir_name = [x for x in os.listdir(data_dir) if x.startswith(author+"-")][0]
    file_name = data_dir + subdir_name + f"/{author.lower()}_{level.lower()}-agg.csv"
    raw_data = pd.read_csv(file_name, index_col=0)

    # get taxonomic levels in the data
    tl = [x for x in tax_levels[:tax_levels.index(level) + 1]]

    # extract counts
    count_data = raw_data.pivot(index="Sample", columns=tl, values="Abundance")
    # get taxonomic tree (for data.var)
    tax_info = pd.DataFrame(index=count_data.columns).reset_index()
    tax_index = tax_info.apply('*'.join, axis=1)
    tax_index = [s.replace("(", "") .replace(")", "") for s in tax_index]
    tax_info.index = tax_index

    count_data.columns = tax_index

    # get metadata
    metadata_cols = raw_data.columns.drop(["Sample", "Abundance"] + tax_levels, errors="ignore")
    metadata = raw_data.groupby("Sample").agg(dict([(x, "first") for x in metadata_cols]))

    ret = ad.AnnData(X=count_data, obs=metadata, var=tax_info)
    return ret


def prepare_data(adata, ref_ct_id, pseudocount=0, prevalence_cut=0.6, outliers=None):

    data_pseudo = adata.X.copy()
    data_pseudo[data_pseudo == 0] = pseudocount
    data_df = pd.DataFrame(data_pseudo, index=adata.obs.index, columns=adata.var.index)

    cols = list(data_df)
    cols[ref_ct_id], cols[-1] = cols[-1], cols[ref_ct_id]
    data_df_swap = data_df.copy()[cols]

    data_x_red = data_df_swap
    perc_0 = np.sum(data_x_red == pseudocount, axis=0) / data_x_red.shape[0]
    print(perc_0)
    data_x_red = data_x_red.loc[:, perc_0 < prevalence_cut]
    if outliers:
        for k, v in outliers.items():
            data_x_red = data_x_red.loc[data_x_red[k] < v * np.sum(data_x_red, axis=1), :]

    data_rel = np.array(data_x_red) / np.sum(np.array(data_x_red), axis=1, keepdims=True)
    data_rel2 = pd.DataFrame(data_rel, index=data_x_red.index, columns=data_x_red.columns)
    return data_rel, data_rel2
