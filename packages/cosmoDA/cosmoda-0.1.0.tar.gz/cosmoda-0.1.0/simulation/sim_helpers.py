import numpy as np
import pandas as pd
import scipy as sp
import anndata as ad
from sklearn.metrics import confusion_matrix

import cosmoDA.cosmoDA as go
import statsmodels.stats.multitest as mt

import rpy2
from rpy2.robjects.packages import importr
from rpy2.robjects import numpy2ri, pandas2ri
import rpy2.robjects as ro

rpy2.robjects.numpy2ri.activate()
rpy2.robjects.pandas2ri.activate()

import importlib
import warnings
warnings.filterwarnings("ignore")

genscore = importr("genscore")
base = importr("base")
CompDA = importr("CompDA")
magrittr = importr("magrittr")
stats = importr("stats")


def generate_banded_cov(p, diag, offdiag, diag_corr, offdiag_corr, n_offdiag_corr):
    A0 = sp.sparse.diags([offdiag, diag, offdiag], [-1, 0, 1], shape=(p, p)).toarray()
    A0[:n_offdiag_corr, :n_offdiag_corr] = sp.sparse.diags(
        [offdiag_corr, diag_corr, offdiag_corr],
        [-1, 0, 1],
        shape=(n_offdiag_corr, n_offdiag_corr)
    ).toarray()

    return A0


def generate_beta(p, effect_size, n_effects):
    beta0 = np.repeat(-0.5, p)
    # beta0[-1] = 1
    beta1 = beta0.copy()
    beta1[:n_effects] += effect_size

    return beta0, beta1


def generate_genscore_data(A0, beta0, beta1, n, p, seed=None):
    domain = genscore.make_domain("simplex", p=p)

    if seed is None:
        seed = ro.r("NULL")

    x_0 = genscore.gen(n, setting="log_log", abs=False, eta=beta0, K=A0, domain=domain, finite_infinity=10000, seed=seed,
                       burn_in=1000, thinning=1000, verbose=False, remove_outofbound=True)

    x_1 = genscore.gen(n, setting="log_log", abs=False, eta=beta1, K=A0, domain=domain, finite_infinity=10000, seed=seed,
                       burn_in=1000, thinning=1000, verbose=False, remove_outofbound=True)

    x_comb = np.concatenate([x_0, x_1])
    cov = np.repeat([0, 1], n)
    anndata_comb = ad.AnnData(X=x_comb, var=pd.DataFrame(index=np.arange(p)), obs=pd.DataFrame({"covariate": cov}))

    return anndata_comb

def estimate_ancombc(data, cov_name):
    ancombc_out = ro.r(f"""
        library(ANCOMBC)
        library(phyloseq)

        #prepare phyloseq data format

        counts = {pandas2ri.py2rpy_pandasdataframe(pd.DataFrame(data.X, columns=data.var.index, index=data.obs.index)).r_repr()}

        sample = {pandas2ri.py2rpy_pandasdataframe(pd.DataFrame(data.obs,
                               columns=[cov_name])).r_repr()}

        cell_types = colnames(counts)

        OTU = otu_table(t(counts), taxa_are_rows = TRUE)

        #create phyloseq data object
        data = phyloseq(OTU, sample_data(sample))

        ancombc_out = suppressMessages(ancombc(phyloseq = data,
                              formula = "{cov_name}",
                              p_adj_method = "fdr",
                              prv_cut = 0.1,
                              lib_cut = 0,
                              group = "{cov_name}",
                              struc_zero = TRUE,
                              neg_lb = TRUE, tol = 1e-5,
                              max_iter = 100,
                              conserve = TRUE,
                              alpha = 0.05,
                              global = FALSE
                              ))

        out = ancombc_out$res
        out
        """)

    parameters = [f"betax_{i}" for i in range(data.X.shape[1])]

    res_df = pd.DataFrame({
        "estimate": ancombc_out[0][-1].flatten().tolist(),
        "std": ancombc_out[1][-1].flatten().tolist(),
        "pval": ancombc_out[3][-1].flatten().tolist(),
        "qval": ancombc_out[4][-1].flatten().tolist()
    }, index=parameters)

    return res_df


def estimate_dirichreg(data, cov_name):
    p_vals_Dirichreg = ro.r(f"""
        library(DirichletReg)

        counts = {pandas2ri.py2rpy_pandasdataframe(pd.DataFrame(data.X, columns=data.var.index)).r_repr()}
        counts$counts = DR_data(counts)
        data = cbind(counts, {pandas2ri.py2rpy_pandasdataframe(pd.DataFrame(data.obs, columns=[cov_name])).r_repr()})

        fit = DirichReg(counts ~ {cov_name}, data)
        if(fit$optimization$convergence > 2L) {{
        pvals = matrix(rep(0, {data.X.shape[1]}),nrow = 1)
        }} else {{
        u = summary(fit)
        pvals = u$coef.mat[grep('Intercept', rownames(u$coef.mat), invert=T), 4]
        v = names(pvals)
        pvals = matrix(pvals, ncol=length(u$varnames))
        rownames(pvals) = gsub('condition', '', v[1:nrow(pvals)])
        colnames(pvals) = u$varnames
        }}
        pvals
    """)

    parameters = [f"betax_{i}" for i in range(data.X.shape[1])]
    reject_dirichreg, qvals_dirichreg, _, _ = mt.multipletests(p_vals_Dirichreg[0], 0.05, method="fdr_bh")

    res_df = pd.DataFrame({
        "pval": p_vals_Dirichreg[0],
        "qval": qvals_dirichreg
    }, index=parameters)

    return res_df


def estimate_genscore_benchmark(x, lambda1s, cov=None, tol=1e-8, maxit=1000, h_mode="pow", h_param1=2, do_test=False, return_elts=True, lambda_select="se"):
    n, p = x.shape
    est_gs = go.estimate(x, cov=cov, tol=tol, maxit=maxit, centered=False, symmetric="symmetric", scale="",
                         lambda1s=lambda1s, h_param1=h_param1, BIC_refit=True, return_raw=True,
                         return_elts=return_elts, diagonal_multiplier=None, cv_fold=5, cv_fold_seed=42)

    if lambda_select == "se":
        cv_losses = np.mean(est_gs["cv_losses"], axis=1)
        cv_stds = np.std(est_gs["cv_losses"], axis=1) / np.sqrt(n)
        lambda_min_cv = np.where(cv_losses == np.min(cv_losses))[0][0]
        lambda_se_cv = np.where(cv_losses <= np.min(cv_losses) + cv_stds[lambda_min_cv])[0][0]
    else:
        lambda_min_cv = lambda_select
        lambda_se_cv = lambda_select

    est_gs["lambda_min_cv"] = lambda_min_cv
    est_gs["lambda_se_cv"] = lambda_se_cv

    if do_test:
        if cov is None:
            raise ValueError("For DA testing, a covariate must be specified!")
        test_df = go.da_test(est_gs, lambda_se_cv, cov)
        est_gs["test_results"] = test_df
    return est_gs


def estimate_CompDA(x, cov):
    n, p = x.shape
    half_min = np.min(x[x != 0]) / 2

    fit_CompDA = CompDA.CompDA(x=x, y=ro.vectors.FloatVector(cov), family_y="binomial", epsilon=half_min, cv_folds=5,
                               m=1e4, verbose=False)
    q = stats.p_adjust(fit_CompDA[:, 1], "BH")
    tb_result = pd.DataFrame({"beta": fit_CompDA[:, 0], "pval": fit_CompDA[:, 1], "qval": q}, index=np.arange(p))
    return tb_result


def eval_multi(p, n_effects, result):
    gt = np.repeat(False, p)
    gt[:n_effects] = True
    tn, fp, fn, tp = confusion_matrix(gt, result["qval"] < 0.05).ravel()

    return tn, fp, fn, tp


def get_scores(df):
    """
    Calculates extended binary classification summary statistics, such as TPR, TNR, youden index, f1-score, MCC

    Parameters
    ----------
    df: DataFrame
        Must contain columns tp, tn, fp, fn

    Returns
    -------
    df: DataFrame
        Same df with added columns tpr, tnr, precision, accuracy, youden, f1_score, mcc
    """
    tp = df["tp"].astype("float64")
    tn = df["tn"].astype("float64")
    fp = df["fp"].astype("float64")
    fn = df["fn"].astype("float64")

    tpr = (tp / (tp + fn)).fillna(0)
    df["tpr"] = tpr
    fpr = (fp / (fp + tn)).fillna(0)
    df["fpr"] = fpr
    tnr = (tn / (tn + fp)).fillna(0)
    df["tnr"] = tnr
    precision = (tp / (tp + fp)).fillna(0)
    df["precision"] = precision
    fdr = (fp / (tp + fp)).fillna(0)
    df["fdr"] = fdr
    acc = ((tp + tn) / (tp + tn + fp + fn)).fillna(0)
    df["accuracy"] = acc

    df["youden"] = tpr + tnr - 1
    df["f1_score"] = 2 * (tpr * precision / (tpr + precision)).fillna(0)

    df["mcc"] = (((tp * tn) - (fp * fn)) / np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))).fillna(0)

    return df
