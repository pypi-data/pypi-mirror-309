import numpy as np
import pandas as pd
import anndata as ad

import rpy2
from rpy2.robjects.packages import importr
from rpy2.robjects import numpy2ri

rpy2.robjects.numpy2ri.activate()
vegan = importr("vegan")
cda = importr("easyCODA")

from typing import Optional, Tuple, Union, List


def geometric_mean(x: np.ndarray, positive: bool = False) -> np.ndarray:
    """
    calculates the geometric mean of a vector
    :param x: Input data
    :param positive: If True, the geometric mean is calculated for positive values of x only
    :return: geometric mean of data
    """
    assert not np.all(x == 0)

    if positive:
        x = x[x > 0]
    a = np.log(x)
    g = np.exp(a.sum() / len(a))
    return g


def clr(x: np.ndarray) -> np.ndarray:
    """
    CLR (centered log-ratio) transformation
    :param x: Input data
    :return: CLR-transformed data
    """
    gmeans = np.apply_along_axis(geometric_mean, 1, x)
    out = np.log(np.divide(x, gmeans[:, np.newaxis]))
    return out


def alr_1(x: np.ndarray) -> np.ndarray:
    """
    ALR (additive log-ratio) transformation, appendend by a column of zeros
    :param x: Input data
    :return: ALR-transformed data
    """
    return np.log(np.divide(x, x[:, -1][:, np.newaxis]))


def alr(x: np.ndarray) -> np.ndarray:
    """
    ALR (additive log-ratio) transformation
    :param x: Input data
    :return: ALR-transformed data
    """
    return np.log(np.divide(x[:, :-1], x[:, -1][:, np.newaxis]))


def closure(x: np.ndarray) -> np.ndarray:
    """
    Calculate closure operation (x/sum(x))
    :param x: Input data
    :return: Closed data
    """
    return x / np.sum(x, axis=1, keepdims=True)


def power_trafo(x: np.ndarray, a: float, comp: bool = False) -> np.ndarray:
    """
    Power transformation (Greenacre, 2024)
    :param x: Input data
    :param a: Power
    :param comp: If True, perform chiPower transformation (Greenacre, 2024),
    else perform regular power transformation (Greenacre, 2024, Eq. 7)
    :return: Transformed data
    """
    xa = x ** a
    xa = closure(xa)

    if comp:
        rm = np.mean(xa, axis=1, keepdims=True)
        z = (1 / a) * (np.sqrt(x.shape[1]) * xa / np.sqrt(rm) - 1)
    else:
        z = (1 / a) * (x.shape[1] * xa - 1)

    return z


def prepare_data(
        data: Union[np.ndarray, ad.AnnData, pd.DataFrame],
        replace_zeros: bool = False,
        reference_component: Optional[str] = None,
        scale_to_rel: Optional[bool] = True
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Prepare dataset for model fitting
    :param data: Input data
    :param replace_zeros: If True, replace zero values with 0.5
    :param reference_component: This component will be moved to the last position in the output data
    :param scale_to_rel: If True, transform data to relative abundances
    :return: Output data, names of features, names of samples
    """
    if type(data) == pd.DataFrame:
        X = data.values.copy()
        ct_names = data.columns.copy()
        sample_names = data.index.copy()
    elif type(data) == ad.AnnData:
        X = data.X.copy()
        ct_names = data.var_names.copy()
        sample_names = data.obs_names.copy()
    elif type(data) == np.ndarray:
        X = data.copy()
        ct_names = np.arange(X.shape[1])
        sample_names = np.arange(X.shape[0])
    else:
        raise ValueError("Data type not supported")

    ct_names = np.array(ct_names.tolist())

    if replace_zeros:
        X[X == 0] = 0.5

    if scale_to_rel:
        X = closure(X)

    if reference_component is not None:
        ref_id = np.where(ct_names == reference_component)[0][0]
        ct_names[ref_id], ct_names[-1] = ct_names[-1], ct_names[ref_id]
        temp = X[:, ref_id].copy()
        X[:, ref_id] = X[:, -1]
        X[:, -1] = temp

    return X.astype(np.float64), ct_names, sample_names


def find_a_procrustes(data: np.ndarray, a_s: List[float] = None, trafo: str = "clr") -> Tuple[float, List]:
    """
    Find ideal power for power transformation, cf. Greenacre, 2024
    :param data: Input data
    :param a_s: List of exponents to consider
    :param trafo: Transformation to use. Current options: "clr", "alr"
    :return: Exponent wit highest procrustes correlation, list of procrustes correlations for all values in a_s
    """
    if a_s is None:
        a_s = np.round(np.arange(0.01, 1, 0.01), 2)

    data_zero_repl, _, _ = prepare_data(data, replace_zeros=True)

    if trafo == "clr":
        data_trafo = clr(data_zero_repl)
    elif trafo == "alr":
        data_trafo = alr_1(data_zero_repl)
    else:
        raise ValueError(f"Transformation {trafo} not supported")
    trafo_pc = cda.PCA(data_trafo, weight=False, nd=13)[-2]

    data_zeros, _, _ = prepare_data(data, replace_zeros=False)

    procs = []
    for a in a_s:
        data_pow = power_trafo(data_zeros, a, comp=False)
        pow_pc = cda.PCA(data_pow, weight=False, nd=13)[-2]
        proc = vegan.protest(trafo_pc, pow_pc, permutations=0)
        procs.append(proc[10][0])

    a_opt = a_s[np.where(procs == np.max(procs))[0][0]]

    return a_opt, procs
