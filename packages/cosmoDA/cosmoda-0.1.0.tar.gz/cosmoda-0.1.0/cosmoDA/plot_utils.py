import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sccoda.util.data_visualization as scv
import sccoda.util.cell_composition_data as scd
import anndata as ad
from matplotlib import cm
from matplotlib.colors import ListedColormap
from typing import Optional, Tuple, Union, List


def plot_barplots(
        data_df: pd.DataFrame,
        figsize: Tuple[int, int] = (10, 4),
        bins: Optional[int] = 30
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plot collection of histograms, one for each data component
    :param data_df: Input data
    :param figsize: Figure size
    :param bins: Number of bins in each histogram
    :return: Figure, Axis object
    """
    p = data_df.shape[1]
    ncols = int(np.ceil(np.sqrt(p)))
    nrows = int(np.ceil(np.sqrt(p)))

    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

    i = 0
    for x in data_df.columns:
        sns.histplot(data_df, x=x, bins=bins, ax=ax[int((i - i % ncols) / ncols), i % ncols])
        i += 1

    return fig, ax


def plot_stacked_bars(data_df: pd.DataFrame, mean_ls: int, plot_legend: Optional[bool] = True) -> plt.Axes:
    """
    Stacked barplot
    :param data_df: Input data (relative abundances)
    :param mean_ls: mean library size to scale data to
    :param plot_legend: If True, plot legend
    :return: Axes object
    """
    data_scc = scd.from_pandas(data_df, covariate_columns=[])
    data_scc.X = np.round(data_scc.X * mean_ls, 0)
    data_scc.obs["x"] = 1
    ax = scv.stacked_barplot(data_scc, "x", plot_legend=plot_legend)
    return ax


# Stacked barplot
def stackbar(
        y: np.ndarray,
        type_names: List[str],
        title: str,
        level_names: List[str],
        cmap,
        plot_legend: bool = True,
        type: str = "relative",
        ax: plt.axes = None,
        **plt_kwargs
) -> plt.Subplot:
    """
    Plots a stacked barplot for one (discrete) covariate
    Typical use (only inside stacked_barplot): plot_one_stackbar(data.X, data.var.index, "xyz", data.obs.index)
    :param y: The count data, collapsed onto the level of interest.
    i.e. a binary covariate has two rows, one for each group, containing the count mean of each cell type
    :param type_names: The names of all cell types
    :param title: Plot title, usually the covariate's name
    :param level_names: names of the covariate's levels
    :param cmap: The color map for the barplot
    :param plot_legend: If True, adds a legend
    :param type: If "relative", scale to relative abundances. If "absolute", leave data as-is
    :param ax: Axes to plot on
    :param plt_kwargs: Further arguments, passed to plt.bar
    :return: Axes object
    """

    n_bars, n_types = y.shape

    if ax is None:
        ax = plt.gca()
    r = np.array(range(n_bars))
    sample_sums = np.sum(y, axis=1)

    barwidth = 0.85
    cum_bars = np.zeros(n_bars)

    for n in range(n_types):
        if type == "relative":
            bars = [i / j * 100 for i, j in zip([y[k][n] for k in range(n_bars)], sample_sums)]
        elif type == "absolute":
            bars = [i for i in [y[k][n] for k in range(n_bars)]]
        else:
            raise ValueError("type must be 'relative' or 'absolute'")
        ax.bar(r, bars, bottom=cum_bars, color=cmap(n % cmap.N),
               width=barwidth, label=type_names[n], linewidth=0, **plt_kwargs)
        cum_bars += bars

    ax.set_title(title)
    if plot_legend:
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)
    ax.set_xticks(r)
    ax.set_xticklabels(level_names, rotation=45)
    if type == "relative":
        ax.set_ylabel("Proportion")
    elif type == "absolute":
        ax.set_ylabel("count")

    return ax


def get_top_n_and_others(
        ann: ad.AnnData,
        n: int = 10,
        orderby: str = None,
        plottype: str = "relative"
) -> Union[None, Tuple[ad.AnnData, pd.Series]]:
    """
    Get top n features (by mean count) from an anndata object and aggregate all others into a column "others"
    :param ann: Input AnnData
    :param n: Number of most abundant features to consider
    :param orderby: Sample order. If "total", order samples by total counts.
    If a feature name, order samples by counts of this feaure. Else, order by most abundant feature.
    :param plottype: If "relative", scale to relative abundances. If "absolute", leave data as-is
    :return: Ordered and aggregated data, order of features
    """
    temp = pd.DataFrame(ann.X, index=ann.obs.index, columns=ann.var.index)

    feat_avs = np.mean(temp, axis=0)
    top_n = feat_avs.sort_values(ascending=False)[:n+1].index.tolist()
    if temp.shape[1] > n:
        if "unclassified" in top_n:
            top_n.remove("unclassified")
        else:
            top_n = top_n[:-1]

        other = np.sum(ann.X[:, np.logical_not([x in top_n for x in ann.var.index])], axis=1)

        X_temp = np.c_[ann[:, top_n].X, other]

        var_temp = pd.DataFrame(index=top_n + ["other"])
    else:
        var_temp = pd.DataFrame(index=top_n)

        X_temp = np.c_[ann[:, top_n].X]

    ad_sel = ad.AnnData(X=X_temp, var=var_temp, obs=ann.obs)

    if orderby == "total":
        order = pd.Series(np.sum(ad_sel.X, axis=1), index=ad_sel.obs.index).sort_values(ascending=False).index.tolist()
    else:
        if orderby is None:
            orderby = top_n[0]
        if plottype == "relative":
            order = (pd.Series((ad_sel[:, orderby].X.flatten()/np.sum(ad_sel.X, axis=1)), index=ad_sel.obs.index).
                     sort_values(ascending=False).index.tolist())
        elif plottype == "absolute":
            order = (pd.Series(ad_sel[:, orderby].X.flatten(), index=ad_sel.obs.index).sort_values(ascending=False).
                     index.tolist())
        else:
            return

    return ad_sel, order


def plot_sample_stackbar(
        data_df: pd.DataFrame,
        title: str = "",
        ax: plt.axes = None,
        plottype: str = "relative",
        col: cm.ScalarMappable = None,
        orderby: str = None,
        feature_order: List[str] = None
) -> plt.axes:
    """
    Plot sample-wise stacked barplot
    :param data_df: Input data (relative abundances)
    :param title: Plot title
    :param ax: Axes to plot on
    :param plottype: If "relative", scale to relative abundances. If "absolute", leave data as-is
    :param col: Colormap to use
    :param orderby: Sample order. If "total", order samples by total counts.
    If a feature name, order samples by counts of this feaure. Else, order by most abundant feature.
    :param feature_order: Plotting order of features
    :return: Axes object
    """
    p = data_df.shape[1]
    data_rel_ad = ad.AnnData(X=np.array(data_df), var=pd.DataFrame(index=data_df.columns),
                             obs=pd.DataFrame(index=data_df.index))

    sel, o_ = get_top_n_and_others(data_rel_ad, n=p, plottype=plottype, orderby=orderby)
    sel2 = sel[o_]
    if col is None:
        col = ListedColormap([cm.tab20(n) for n in range(p)])

    if feature_order is not None:
        sel2 = sel2[:, feature_order]

    ax = stackbar(
        sel2.X,
        type_names=sel2.var.index,
        title=title,
        level_names=sel2.obs.index,
        cmap=col,
        plot_legend=True,
        ax=ax,
        type=plottype
    )

    return ax
