import numpy as np
import scipy as sp
import ctypes
from ctypes import *
import statsmodels.stats.multitest as mt
import pandas as pd
from scipy.special import gammaln

from pathlib import Path
from typing import Optional, Tuple, Union, List


def dist_simplex(x: np.ndarray, h_param1: float, n: int, p: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Get h(X), dh(X) on the simplex.
    :param x: Input data
    :param h_param1: Exponent to use in h
    :param n: Number of samples
    :param p: Number of features
    :return: h(X), dh(X)
    """
    dist_x = np.array([[np.min([x[i, j], x[i, -1]]) for j in range(p - 1)] for i in range(n)])
    dist_p = np.array([[1 if x[i, j] < x[i, -1] else -1 for j in range(p - 1)] for i in range(n)])

    hdx = dist_x ** h_param1
    hpdx = h_param1 * dist_x ** (h_param1 - 1)
    hpdx[dist_p == -1] *= -1

    return hdx, hpdx


def get_elts_ab(
        x: np.ndarray,
        h_param1: float,
        a: float,
        b: float,
        diagonal_multiplier: float,
        cov: Optional[np.ndarray] = None,
        sum_zero: bool = False,
        aug_method: str = "man",
        finite_infinity: float = 1e20,
        adjust_power: bool = True
) -> dict:
    """
    Calculate score matching elements for the simples
    :param x: Input data
    :param h_param1: Exponent to use in h
    :param a: Power for Interaction part
    :param b: Power for location part
    :param diagonal_multiplier: Scaling factor for diagonal of Gamma
    :param cov: Covariate vector
    :param sum_zero: If True, enforce zero-sum rows in K
    :param aug_method: Augmentation method for simplex constraint. EIther "man" or "C", produces identical reults
    :param finite_infinity: Value to replace numerical infinity values
    :param adjust_power: If True, adjust elements to asypmtotically approximate the logarithm
    :return: Dictionary of elements
    """
    n, p = x.shape

    if a == 0:
        xa = np.log(x)
        a_ = 1
    else:
        xa = (x ** a)
        a_ = a
    xa_1 = np.nan_to_num(x ** (a - 1), copy=False, nan=0.0, posinf=finite_infinity, neginf=-finite_infinity)
    xa_2 = np.nan_to_num(x ** (a - 2), copy=False, nan=0.0, posinf=finite_infinity, neginf=-finite_infinity)

    xb_1 = np.nan_to_num(x ** (b - 1), copy=False, nan=0.0, posinf=finite_infinity, neginf=-finite_infinity)
    xb_2 = np.nan_to_num(x ** (b - 2), copy=False, nan=0.0, posinf=finite_infinity, neginf=-finite_infinity)

    hdx, hpdx = dist_simplex(x, h_param1, n, p)

    sum_h = (np.sum(hdx, axis=1) * xa_2[:, -1]).reshape((n, 1))
    sum_hp = (np.sum(hpdx, axis=1) * xa_1[:, -1]).reshape((n, 1))
    sum_h2 = np.nan_to_num(np.sum(hdx, axis=1) * x[:, -1] ** (2 * a - 2), copy=False, nan=0.0, posinf=finite_infinity, neginf=-finite_infinity).reshape((n, 1))

    # Set up g
    xa_1_m = ((hdx * xa_1[:, :-1]).T * xa_1[:, -1].T).T
    g_K = np.einsum("ij, ik -> ijk",
                    xa,
                    np.concatenate([
                        (hpdx * xa_1[:, :-1]) + (a - 1) * (hdx * xa_2[:, :-1]),
                        - sum_h + (a - 1) * sum_hp
                    ], axis=1)
                    )
    for n_ in range(n):
        for p_ in range(p - 1):
            g_K[n_, p_, p_] += np.nan_to_num(a_ * hdx[n_, p_] * x[n_, p_] ** (2 * a - 2), copy=False, nan=0.0, posinf=finite_infinity, neginf=-finite_infinity)
            g_K[n_, p - 1, p_] -= a_ * xa_1_m[n_, p_]
            g_K[n_, p_, p - 1] -= a_ * xa_1_m[n_, p_]
        g_K[n_, -1, -1] += a_ * sum_h2[n_]

    g_K = g_K.reshape((n, p ** 2), order="F")

    g_eta = np.concatenate([
        - hpdx * xb_1[:, :-1] - (b - 1) * hdx * xb_2[:, :-1],
        - (b - 1) * sum_h + sum_hp
    ], axis=1)

    def get_temp(j, k, xa, xa_1, xb_1, hdx, sum_hd):
        xa_m1 = np.concatenate(
            [np.multiply(xa_1[:, j], xa.transpose(1, 0)).transpose(), (-1 * xb_1[:, j]).reshape((n, 1))], axis=1)
        xa_m1_k = np.concatenate(
            [np.multiply(xa_1[:, k], xa.transpose(1, 0)).transpose(), (-1 * xb_1[:, k]).reshape((n, 1))], axis=1)
        if sum_hd:
            hdx_ = np.sum(hdx, axis=1)
            temp = np.multiply(hdx_, np.einsum("ij, ik -> ijk", xa_m1, xa_m1_k).transpose(1, 2, 0)).transpose(2, 0, 1)
        else:
            temp = np.multiply(hdx[:, j], np.einsum("ij, ik -> ijk", xa_m1, xa_m1_k).transpose(1, 2, 0)).transpose(2, 0, 1)
        return temp

    # diagonal elements of blocks in Gamma
    Gamma_K0 = np.concatenate([get_temp(j, j, xa, xa_1, xb_1, hdx, False) for j in range(p - 1)], axis=2)
    Gamma_K = Gamma_K0[:, :-1, [i for i in range(Gamma_K0.shape[2]) if ((i + 1) % (p + 1) != 0)]]
    Gamma_K_eta = Gamma_K0[:, :-1, [i for i in range(Gamma_K0.shape[2]) if ((i + 1) % (p + 1) == 0)]]
    Gamma_eta = Gamma_K0[:, -1:, [i for i in range(Gamma_K0.shape[2]) if ((i + 1) % (p + 1) == 0)]]

    Gamma_Kp0 = get_temp(p - 1, p - 1, xa, xa_1, xb_1, hdx, True)
    Gamma_K = np.concatenate([Gamma_K, Gamma_Kp0[:, :p, :p]], axis=2)
    Gamma_K_eta = np.concatenate([Gamma_K_eta, Gamma_Kp0[:, :p, [p]]], axis=2)

    Gamma_eta = np.concatenate([Gamma_eta, Gamma_Kp0[:, p, p].reshape((n, 1, 1))], axis=2)

    # Off-diagonal blocks
    Gamma_K0_jp = np.concatenate([-1 * get_temp(j, p - 1, xa, xa_1, xb_1, hdx, False) for j in range(p - 1)], axis=2)
    Gamma_K_jp = Gamma_K0_jp[:, :-1, [i for i in range(Gamma_K0_jp.shape[2]) if ((i + 1) % (p + 1) != 0)]]
    Gamma_K_eta_jp = Gamma_K0_jp[:, :-1, [i for i in range(Gamma_K0_jp.shape[2]) if ((i + 1) % (p + 1) == 0)]]
    Gamma_eta_jp = Gamma_K0_jp[:, -1, [i for i in range(Gamma_K0_jp.shape[2]) if ((i + 1) % (p + 1) == 0)]]

    Gamma_Kj_etap = Gamma_K_eta_jp.copy()
    Gamma_Kp_etaj = Gamma_K_eta_jp.copy()

    if sum_zero and aug_method == "man":
        for n_ in range(n):
            for j in range(p):
                g_K[n_, (j * p):((j + 1) * p)] -= g_K[n_, j * p + j]
                Gamma_K[n_, :, (j * p):((j + 1) * p)] -= Gamma_K[n_, j, (j * p):((j + 1) * p)]
                Gamma_K[n_, :, (j * p):((j + 1) * p)] = (
                            Gamma_K[n_, :, (j * p):((j + 1) * p)].T - Gamma_K[n_, :, j * (p + 1)]).T

            for j in range(p - 1):
                Gamma_K_jp[n_, :, (j * p):((j + 1) * p)] -= Gamma_K_jp[n_, j, (j * p):((j + 1) * p)]
                Gamma_K_jp[n_, :, (j * p):((j + 1) * p)] = (
                            Gamma_K_jp[n_, :, (j * p):((j + 1) * p)].T - Gamma_K_jp[n_, :, (j + 1) * p - 1])
                Gamma_Kj_etap[n_, :, j] -= Gamma_Kj_etap[n_, j, j]
            Gamma_Kp_etaj[n_, :, :] -= Gamma_Kp_etaj[n_, p - 1, :]

            for j in range(p):
                Gamma_K_eta[n_, :, [j]] = Gamma_K_eta[n_, :, [j]] - Gamma_K_eta[n_, j, j]

    # Adjust by factor a to keep scale
    if adjust_power:
        Gamma_K = 1/a_**2 * Gamma_K
        Gamma_K_jp = 1/a_**2 * Gamma_K_jp
        Gamma_K_eta = 1/a_ * Gamma_K_eta
        Gamma_Kj_etap = 1/a_ * Gamma_Kj_etap
        Gamma_Kp_etaj = 1/a_ * Gamma_Kp_etaj
        g_K = 1/a_ * g_K

    Gamma_K_jp_elts = Gamma_K_jp
    r = 0
    r2 = p
    for j in range(p - 1):
        Gamma_K_jp_elts[:, :, r:r2] = np.transpose(Gamma_K_jp_elts[:, :, r:r2], axes=(0, 2, 1))
        r2 += p
        r += p

    diag_with_mult = np.concatenate(
        [np.diag(np.mean(Gamma_K, axis=0)[:, (i * p):((i + 1) * p)]) for i in range(p)]) * diagonal_multiplier

    elts_dict = {
        "g_K": g_K,
        "g_eta": g_eta,
        "Gamma_K": Gamma_K,
        "Gamma_K_eta": Gamma_K_eta,
        "Gamma_K_jp": Gamma_K_jp_elts,
        "Gamma_Kj_etap": Gamma_Kj_etap,
        "Gamma_Kp_etaj": Gamma_Kp_etaj,
        "Gamma_eta": Gamma_eta,
        "Gamma_eta_jp": Gamma_eta_jp,
        "diagonals_with_multiplier": diag_with_mult
    }
    if cov is not None:
        Gamma_K_eta_c = np.multiply(cov, Gamma_K_eta.transpose(1, 2, 0)).transpose(2, 0, 1)
        elts_dict["Gamma_K_eta_c"] = Gamma_K_eta_c

        Gamma_Kj_etap_c = np.multiply(cov, Gamma_Kj_etap.transpose(1, 2, 0)).transpose(2, 0, 1)
        elts_dict["Gamma_Kj_etap_c"] = Gamma_Kj_etap_c

        Gamma_Kp_etaj_c = np.multiply(cov, Gamma_Kp_etaj.transpose(1, 2, 0)).transpose(2, 0, 1)
        elts_dict["Gamma_Kp_etaj_c"] = Gamma_Kp_etaj_c

        Gamma_eta_c = np.multiply(cov, Gamma_eta.transpose(1, 2, 0)).transpose(2, 0, 1)
        elts_dict["Gamma_eta_c"] = Gamma_eta_c
        Gamma_eta_c2 = np.multiply(cov ** 2, Gamma_eta.transpose(1, 2, 0)).transpose(2, 0, 1)
        elts_dict["Gamma_eta_c2"] = Gamma_eta_c2

        Gamma_eta_jp_c = np.multiply(cov, Gamma_eta_jp.transpose(1, 0)).transpose()
        elts_dict["Gamma_eta_jp_c"] = Gamma_eta_jp_c
        Gamma_eta_jp_c2 = np.multiply(cov ** 2, Gamma_eta_jp.transpose(1, 0)).transpose()
        elts_dict["Gamma_eta_jp_c2"] = Gamma_eta_jp_c2

        g_eta_c = np.einsum("i, ij -> ij", cov, g_eta)
        elts_dict["g_eta_c"] = g_eta_c

    return elts_dict


def log_binom(n: int, k: float) -> float:
    """
    Calculate log-binomial coefficient, numercally stable
    :param n: Number of choices
    :param k: Number of draws
    :return: log(n over k)
    """
    if (k == 0) or (n == k):
        return 0.
    else:
        return gammaln(n+1) - (gammaln(k+1) + gammaln(n-k+1))


def eBIC(
        res: dict,
        elts: dict,
        BIC_refit: bool = True,
        gammas: np.ndarray = np.array([0, 0.5, 1]),
        use_covariate: bool = False
) -> Tuple[np.ndarray, np.ndarray]:
    """
    BIC_refit: calculate BIC (with refit) or not
    :param res: Score matching results
    :param elts: Score matching elements
    :param BIC_refit: If true, return BICs of refit run
    :param gammas: Scaling factors for BIC
    :param use_covariate: If True, use the covariate (requires res and elts to be produced with a covariate)
    :return: eBICs, refit eBICs
    """
    n = elts["n"]
    p = elts["p"]

    loss = 2 * n * res["crit"]
    eBIC_refit = np.repeat(np.inf, len(gammas))
    if elts["centered"] | elts["profiled_if_noncenter"]:
        if res["symmetric"] == "symmetric":
            nedges = len(res["edges"]) / 2
            eBIC_p2 = nedges * np.log(n)
            eBIC_p3s = 2 * gammas * log_binom(p * (p - 1) / 2, nedges)
        else:
            nedges = len(res["edges"])
            eBIC_p2 = nedges * np.log(n)
            eBIC_p3s = 2 * gammas * log_binom(p * (p - 1), nedges)
    else:
        if res["symmetric"] == "symmetric":
            nedges1 = len(res["edges"]) / 2
        else:
            nedges1 = len(res["edges"])
        nedges2 = len(res["eta_support"])
        eBIC_p2 = (nedges1 + nedges2) * np.log(n)
        if res["symmetric"] == "symmetric":
            eBIC_p3s = 2 * gammas * (log_binom(p * (p - 1) / 2, nedges1) + log_binom(p, nedges2))
        else:
            eBIC_p3s = 2 * gammas * (log_binom(p * (p - 1), nedges1) + log_binom(p, nedges2))

    eBIC_ = loss + eBIC_p2 + eBIC_p3s
    if BIC_refit:
        loss_refit = 2 * n * refit(res, elts, use_covariate)
        eBIC_refit = loss_refit + eBIC_p2 + eBIC_p3s

    return eBIC_, eBIC_refit


def refit(res: dict, elts: dict, use_covariate: bool = False) -> float:
    """
    Get loss value of refit
    :param res: Score matching results
    :param elts: Score matching elements
    :param use_covariate: If True, use the covariate (requires res and elts to be produced with a covariate)
    :return: refit loss
    """
    p = elts["p"]

    if len(res["edges"]) == 0:
        res["edges"] = np.array(0)
    if np.max(np.array(res["edges"] % elts["p"]), 0) >= elts["n"] - 2:  # If max degree > n, (with multiplier 1) Gamma sub-matrix not invertible, so do not refit; n-1 because res$edges does not contain diagonals
        return np.inf

    for i in range(p):
        for j in range(p):
            if p * i + j not in res["edges"]:
                res["K"][i, j] = 0

    if elts["centered"] | elts["profiled_if_noncenter"]:
        test = get_results(elts, symmetric=res["symmetric"], lambda1=0., tol=res["tol"], maxit=res["maxit"], previous_res=res,
                           is_refit=True, use_covariate=use_covariate)

    else:
        for j in range(p):
            if j not in res["eta_support"]:
                res["eta"][j] = 0
        test = get_results(elts, symmetric=res["symmetric"], lambda1=0., lambda2=0., tol=res["tol"], maxit=res["maxit"],
                           previous_res=res, is_refit=True, use_covariate=use_covariate)

    return test["crit"]


def make_folds(nsamp: int, nfold: int, cv_fold_seed: int = None) -> List[np.ndarray]:
    """
    Make cross-validation folds
    :param nsamp: Number of samples
    :param nfold: Number of folds
    :param cv_fold_seed: Random seed
    :return: List with nfold entries. Each entry contains the sample indices for the respective fold
    """
    rng = np.random.default_rng(cv_fold_seed)
    id_ = rng.choice(np.arange(nsamp), nsamp, replace=False)
    every = np.floor(nsamp / nfold)
    ends = [int(i * every) for i in range(nfold + 1)]
    return [id_[ends[i]:ends[i + 1]] for i in range(nfold)]


def calc_crit(elts: dict, res: dict, penalty: bool, use_covariate: bool = False) -> float:
    """
    Calculate score matching loss
    :param elts: Score matching elements
    :param res: Score matching results
    :param penalty: If True, use  diagonal multiplier on Gamma
    :param use_covariate: If True, use covariate (requires res and elts to be produced with a covariate)
    :return: Score matching loss
    """
    if elts["profiled_if_noncenter"]:
        raise ValueError("In calc_crit(): elts must not be profiled if non-centered.")
    if elts["centered"] != (res["eta"] is None):
        raise ValueError("elts and res must be both centered or both non-centered.")
    if elts["p"] != res["p"]:
        raise ValueError("elts$p and res$p must be equal.")

    p = elts["p"]
    if penalty:
        if (elts["setting"] == "gaussian") and (elts["domain_type"] == "R"):
            for j in range(p * (p - 1)):
                elts["Gamma_K"][j, j] = elts["diagonals_with_multiplier"][j]
        else:
            for i in range(p):
                for j in range(p):
                    elts["Gamma_K"][j, p * i + j] = elts["diagonals_with_multiplier"][p * i + j]

    if (elts["setting"] == "gaussian") and (elts["domain_type"] == "R"):
        crit = np.sum([res["K"][:, i].T @ elts["Gamma_K"] @ res["K"][:, i] for i in range(p)]) / 2 - np.sum(
            np.diag(res["K"]))
        if not elts["centered"]:
            crit = (crit + np.sum([np.sum(res["K"][:, i] * elts["Gamma_K_eta"]) * res["eta"][i] for i in range(p)]) +
                    np.sum(res["eta"] ** 2) / 2)
    else:
        crit = np.sum([
            res["K"][:, i].T @
            (elts["Gamma_K"][:, i * p:(i + 1) * p] @ res["K"][:, i] / 2 - elts["g_K"][i * p:(i + 1) * p])
            for i in range(p)])
        if not elts["centered"]:
            crit = (crit + np.sum([res["K"][:, i].T @ elts["Gamma_K_eta"][:, i] * res["eta"][i] for i in range(p)]) -
                    np.sum(res["eta"] * elts["g_eta"]) +
                    np.sum(res["eta"] ** 2 * elts["Gamma_eta"]) / 2)
            if use_covariate:
                crit = (crit + np.sum([res["K"][:, i].T @ elts["Gamma_K_eta_c"][:, i] * res["eta_c"][i] for i in range(p)]) -
                        np.sum(res["eta_c"] * elts["g_eta_c"]) +
                        np.sum(res["eta_c"] ** 2 * elts["Gamma_eta_c2"]) / 2 +
                        np.sum(res["eta"] * elts["Gamma_eta_c"] * res["eta_c"]))

        if elts["domain_type"] == "simplex":
            crit = crit + np.sum([res["K"][:, i].T @ elts["Gamma_K_jp"][:, i * p:(i + 1) * p] @ res["K"][:, p - 1] for i in range(p - 1)])
            if not elts["centered"]:
                crit = crit + np.sum([res["K"][:, i].T @ elts["Gamma_Kj_etap"][:, i] * res["eta"][p - 1] +
                                      res["K"][p - 1, :] @ elts["Gamma_Kp_etaj"][:, i] * res["eta"][i] +
                                      res["eta"][i] * elts["Gamma_eta_jp"][i] * res["eta"][p - 1] for i in range(p - 1)])
                if use_covariate:
                    crit = crit + np.sum([res["K"][:, i].T @ elts["Gamma_Kj_etap_c"][:, i] * res["eta_c"][p - 1] +
                                          res["K"][p - 1, :] @ elts["Gamma_Kp_etaj_c"][:, i] * res["eta_c"][i] +
                                          res["eta_c"][i] * elts["Gamma_eta_jp_c2"][i] * res["eta_c"][p - 1] +
                                          res["eta"][i] * elts["Gamma_eta_jp_c"][i] * res["eta_c"][p - 1] +
                                          res["eta_c"][i] * elts["Gamma_eta_jp_c"][i] * res["eta"][p - 1] for i in
                                          range(p - 1)])

    if penalty:
        l1 = res["lambda1"].item()
        l2 = res["lambda2"].item()
        crit = crit + l1 * np.sum(np.abs(res["K"][np.identity(p) == 0]))
        if l2 is not None:  # res$lambda2 is NULL if res is centered or profiled
            crit = crit + l2 * np.sum(np.abs(res["eta"]))
            if use_covariate:
                crit = crit + l2 * np.sum(np.abs(res["eta_c"]))
        if elts["domain_type"] == "simplex":
            crit = crit + (p - 2) * l1 * np.sum(np.abs(res["K"][:(p-1), p - 1]) + np.abs(res["K"][p - 1, :(p-1)]))
            if l2 is not None:
                crit = (crit + (p - 2) * l2 * np.abs(res["eta"][p - 1]))
                if use_covariate:
                    crit = crit + ((p - 2) * l2 * np.abs(res["eta_c"][p - 1]))

    return crit


def estimate(
        x: np.ndarray,
        centered: bool = False,
        symmetric: str = "symmetric",
        scale: str = "",
        setting: str = "log_log_sum0",
        a: float = 0,
        b: float = 0,
        h_param1: float = 2,
        cov: np.ndarray = None,
        diagonal_multiplier: float = None,
        sum_zero: bool = True,
        lambda1s: Union[List[float], float, np.ndarray] = 0.,
        lambda_ratio: float = np.inf,
        aug_method: str = "man",
        tol: float = 1e-8,
        maxit: int = 1000,
        BIC_refit: bool = False,
        warmstart: bool = False,
        eBIC_gammas: Union[List[float], np.ndarray] = np.array([0, 0.5, 1]),
        cv_fold: int = None,
        cv_fold_seed: int = None,
        return_raw: bool = False,
        return_elts: bool = False,
        adjust_power: bool = True,
        verbose: int = 0
) -> dict:
    """
    Estimate COSMODACHS or power interaction model
    :param x: Input data
    :param centered: If True, only estimate K
    :param symmetric: Parameter from genscore. Should always be "symmetric" for simplex models
    :param scale: Parameter from genscore. Should always be "" for simplex models
    :param setting: Parameter from genscore. Should always be "log_log_sum0" or "log_log" for simplex models
    :param a: Power for Interaction part
    :param b: Power for location part
    :param h_param1: Exponent to use in h
    :param cov: Covariate vector
    :param diagonal_multiplier: Scaling factor for diagonal of Gamma
    :param sum_zero: If True, enforce zero-sum constraint on K
    :param lambda1s: Regularization parameters to consider
    :param lambda_ratio: Parameter from genscore (Ratio between lambda_1 and lambda_2).
    Should always be np.inf for simplex models
    :param aug_method: Augmentation method for simplex constraint. EIther "man" or "C", produces identical reults
    :param tol: Numerical tolerance for convergence
    :param maxit: Maximum number of iterations
    :param BIC_refit: If true, return BICs of refit run
    :param warmstart: If true, use previous result for warm start
    :param eBIC_gammas: Scaling factors for eBIC
    :param cv_fold: Number of cross-validation folds
    :param cv_fold_seed: Random seed for cross-validation
    :param return_raw: If True, return estimates for K
    :param return_elts: If True, return elements dictionary
    :param adjust_power: If True, adjust elements to asypmtotically approximate the logarithm
    :param verbose: Verbosity level (0: No Outputs; 1: Notify for major steps; 2: Notify about progress)
    :return: Estimation results dictionary
    """
    n, p = x.shape

    if diagonal_multiplier is None:
        # Alternative diagonal multiplier (Theorem 4, Yu et al.)
        # prob_hold = 0.95
        # tau = -1 * (np.log(1 - prob_hold) / np.log(p))
        # diagonal_multiplier = 1 + np.sqrt((tau * np.log(p) + np.log(4)) / (2 * n))

        diagonal_multiplier = 1 + (1 - 1 / (1 + 4 * np.exp(1) * max(6 * np.log(p) / n, np.sqrt(6 * np.log(p) / n))))
    if (diagonal_multiplier < 1 + tol) & (p > n):
        raise RuntimeWarning("p > n and diagonal_multiplier should be larger than 1.")
    elif diagonal_multiplier > 1 - tol:
        diagonal_multiplier = np.max((1, diagonal_multiplier))

    if a == 0 and b == 0:
        elts_big = get_elts_ab(x, h_param1, a=a, b=b, diagonal_multiplier=diagonal_multiplier,
                                                    cov=cov, sum_zero=sum_zero, aug_method=aug_method, adjust_power=adjust_power)

    elif a >= 0 and b >= 0:
        elts_big = get_elts_ab(x, h_param1, a=a, b=b, diagonal_multiplier=diagonal_multiplier,
                                                    cov=cov, sum_zero=sum_zero, aug_method=aug_method, adjust_power=adjust_power)
    else:
        raise NotImplementedError(f"Not implemented for a={a}!")

    if cov is not None:
        if cov.shape != (n, ):
            raise ValueError("Covariate shape does not match data shape")
        use_covariate = True
    else:
        use_covariate = False

    if return_elts:
        elts_ret = elts_big.copy()
        elts_ret["sum_to_zero"] = sum_zero
        elts_ret["n"] = n
        elts_ret["p"] = p
        elts_ret["diagonal_multiplier"] = diagonal_multiplier

    else:
        elts_ret = None

    elts = {
        'n': n,
        'p': p,
        'g_K': np.mean(elts_big["g_K"], axis=0),
        'g_eta': np.mean(elts_big["g_eta"], axis=0),
        'Gamma_K': np.mean(elts_big["Gamma_K"], axis=0),
        'Gamma_K_eta': np.mean(elts_big["Gamma_K_eta"], axis=0),
        'Gamma_K_jp': np.mean(elts_big["Gamma_K_jp"], axis=0),
        'Gamma_Kj_etap': np.mean(elts_big["Gamma_Kj_etap"], axis=0),
        'Gamma_Kp_etaj': np.mean(elts_big["Gamma_Kp_etaj"], axis=0),
        'Gamma_eta': np.mean(elts_big["Gamma_eta"], axis=0),
        'Gamma_eta_jp': np.mean(elts_big["Gamma_eta_jp"], axis=0),
        'centered': False,
        "scale": scale,
        "profiled_if_noncenter": False,
        "sum_to_zero": sum_zero,
        "diagonal_multiplier": diagonal_multiplier,
        "diagonals_with_multiplier": elts_big["diagonals_with_multiplier"],
        "setting": setting,
        "domain_type": "simplex"
    }

    if use_covariate:
        elts["Gamma_K_eta_c"] = np.mean(elts_big["Gamma_K_eta_c"], axis=0)
        elts["Gamma_Kj_etap_c"] = np.mean(elts_big["Gamma_Kj_etap_c"], axis=0)
        elts["Gamma_Kp_etaj_c"] = np.mean(elts_big["Gamma_Kp_etaj_c"], axis=0)
        elts["Gamma_eta_c"] = np.mean(elts_big["Gamma_eta_c"], axis=0)
        elts["Gamma_eta_c2"] = np.mean(elts_big["Gamma_eta_c2"], axis=0)
        elts["Gamma_eta_jp_c"] = np.mean(elts_big["Gamma_eta_jp_c"], axis=0)
        elts["Gamma_eta_jp_c2"] = np.mean(elts_big["Gamma_eta_jp_c2"], axis=0)
        elts["g_eta_c"] = np.mean(elts_big["g_eta_c"], axis=0)

    edgess = []

    if not centered:
        etas = []
        if use_covariate:
            eta_cs = []
        else:
            eta_cs = None
    else:
        etas = None

    if isinstance(lambda1s, int) or isinstance(lambda1s, float):
        lambda1s = [lambda1s]
    if lambda1s is None:
        lambda1s = [0.]
    lambda_length = len(lambda1s)
    convergeds = np.zeros(lambda_length)
    iters = np.zeros(lambda_length)
    if verbose > 0:
        print("Calculating estimates.")

    raw_estimates = []

    BICs = np.full((lambda_length, 2 * len(eBIC_gammas)), np.inf)
    lambda2s = []

    lc = 0
    for lambda_index in range(lambda_length):
        if verbose > 1:
            if lc % 10 == 0:
                print(f"Lambda {lc}/{lambda_length}")
        if not warmstart:
            res = None
        if lambda_ratio == np.inf:
            lambda_2 = 0.
        else:
            lambda_2 = lambda1s[lambda_index] / lambda_ratio
        lambda2s.append(lambda_2)
        res = get_results(elts, lambda1=lambda1s[lambda_index], lambda2=lambda_2, symmetric=symmetric, tol=tol,
                          maxit=maxit, previous_res=res, is_refit=False, use_covariate=use_covariate)

        convergeds[lambda_index] = res["converged"]
        iters[lambda_index] = res["iters"]
        edgess.append(res["edges"])

        if return_raw:
            raw_estimates.append(res["K"].copy())
        if "eta" in res.keys():
            etas.append(res["eta"])
        if "eta_c" in res.keys():
            eta_cs.append(res["eta_c"])
        # exclude_eta <- res$exclude_eta

        BICs[lambda_index, :len(eBIC_gammas)], BICs[lambda_index, len(eBIC_gammas):] = eBIC(res, elts,
                                                                                            BIC_refit=BIC_refit,
                                                                                            gammas=eBIC_gammas,
                                                                                            use_covariate=use_covariate)

        if (not return_raw) and (len(res["edges"]) == p * (p - 1)) and (
                lambda_index < lambda_length):  # If all edges are selected for some lambda, end early
            BICs[(lambda_index + 1):lambda_length, ] = np.inf
            convergeds[(lambda_index + 1):lambda_length] = 0  # convergeds[lambda_index]
            iters[(lambda_index + 1):lambda_length] = 0
            for li in np.arange((lambda_index + 1), lambda_length):
                edgess[li] = edgess[[li - 1]]
            break

        lc += 1

    lambda_index_stopped = lambda_index

    if cv_fold is not None:
        ids = make_folds(n, cv_fold, cv_fold_seed)
        cv_losses = np.full((lambda_length, cv_fold), np.inf)
        res = None
        for fold in range(cv_fold):
            if verbose > 1:
                print(f"Fold {fold + 1}/{cv_fold}")
            this_ids = ids[fold]
            rest_ids = np.hstack([ids[i] for i in range(cv_fold) if i != fold])
            if use_covariate:
                cov_this = cov[this_ids]
                cov_rest = cov[rest_ids]
            else:
                cov_this = cov
                cov_rest = cov
            elts_this = get_elts_ab(x[this_ids, :], h_param1, a=a, b=b, diagonal_multiplier=diagonal_multiplier,
                                    cov=cov_this, sum_zero=sum_zero, aug_method=aug_method, adjust_power=adjust_power)
            elts_rest = get_elts_ab(x[rest_ids, :], h_param1, a=a, b=b, diagonal_multiplier=diagonal_multiplier,
                                    cov=cov_rest, sum_zero=sum_zero, aug_method=aug_method, adjust_power=adjust_power)

            elts_this_ = {
                'n': len(this_ids),
                'p': p,
                'g_K': np.mean(elts_this["g_K"], axis=0),
                'g_eta': np.mean(elts_this["g_eta"], axis=0),
                'Gamma_K': np.mean(elts_this["Gamma_K"], axis=0),
                'Gamma_K_eta': np.mean(elts_this["Gamma_K_eta"], axis=0),
                'Gamma_K_jp': np.mean(elts_this["Gamma_K_jp"], axis=0),
                'Gamma_Kj_etap': np.mean(elts_this["Gamma_Kj_etap"], axis=0),
                'Gamma_Kp_etaj': np.mean(elts_this["Gamma_Kp_etaj"], axis=0),
                'Gamma_eta': np.mean(elts_this["Gamma_eta"], axis=0),
                'Gamma_eta_jp': np.mean(elts_this["Gamma_eta_jp"], axis=0),
                'centered': False,
                "scale": scale,
                "profiled_if_noncenter": False,
                "sum_to_zero": sum_zero,
                "diagonal_multiplier": diagonal_multiplier,
                "diagonals_with_multiplier": elts_this["diagonals_with_multiplier"],
                "setting": setting,
                "domain_type": "simplex"
            }

            elts_rest_ = {
                'n': len(rest_ids),
                'p': p,
                'g_K': np.mean(elts_rest["g_K"], axis=0),
                'g_eta': np.mean(elts_rest["g_eta"], axis=0),
                'Gamma_K': np.mean(elts_rest["Gamma_K"], axis=0),
                'Gamma_K_eta': np.mean(elts_rest["Gamma_K_eta"], axis=0),
                'Gamma_K_jp': np.mean(elts_rest["Gamma_K_jp"], axis=0),
                'Gamma_Kj_etap': np.mean(elts_rest["Gamma_Kj_etap"], axis=0),
                'Gamma_Kp_etaj': np.mean(elts_rest["Gamma_Kp_etaj"], axis=0),
                'Gamma_eta': np.mean(elts_rest["Gamma_eta"], axis=0),
                'Gamma_eta_jp': np.mean(elts_rest["Gamma_eta_jp"], axis=0),
                'centered': False,
                "scale": scale,
                "profiled_if_noncenter": False,
                "sum_to_zero": sum_zero,
                "diagonal_multiplier": diagonal_multiplier,
                "diagonals_with_multiplier": elts_rest["diagonals_with_multiplier"],
                "setting": setting,
                "domain_type": "simplex"
            }

            if use_covariate:
                elts_this_["Gamma_K_eta_c"] = np.mean(elts_this["Gamma_K_eta_c"], axis=0)
                elts_this_["Gamma_Kj_etap_c"] = np.mean(elts_this["Gamma_Kj_etap_c"], axis=0)
                elts_this_["Gamma_Kp_etaj_c"] = np.mean(elts_this["Gamma_Kp_etaj_c"], axis=0)
                elts_this_["Gamma_eta_c"] = np.mean(elts_this["Gamma_eta_c"], axis=0)
                elts_this_["Gamma_eta_c2"] = np.mean(elts_this["Gamma_eta_c2"], axis=0)
                elts_this_["Gamma_eta_jp_c"] = np.mean(elts_this["Gamma_eta_jp_c"], axis=0)
                elts_this_["Gamma_eta_jp_c2"] = np.mean(elts_this["Gamma_eta_jp_c2"], axis=0)
                elts_this_["g_eta_c"] = np.mean(elts_this["g_eta_c"], axis=0)

                elts_rest_["Gamma_K_eta_c"] = np.mean(elts_rest["Gamma_K_eta_c"], axis=0)
                elts_rest_["Gamma_Kj_etap_c"] = np.mean(elts_rest["Gamma_Kj_etap_c"], axis=0)
                elts_rest_["Gamma_Kp_etaj_c"] = np.mean(elts_rest["Gamma_Kp_etaj_c"], axis=0)
                elts_rest_["Gamma_eta_c"] = np.mean(elts_rest["Gamma_eta_c"], axis=0)
                elts_rest_["Gamma_eta_c2"] = np.mean(elts_rest["Gamma_eta_c2"], axis=0)
                elts_rest_["Gamma_eta_jp_c"] = np.mean(elts_rest["Gamma_eta_jp_c"], axis=0)
                elts_rest_["Gamma_eta_jp_c2"] = np.mean(elts_rest["Gamma_eta_jp_c2"], axis=0)
                elts_rest_["g_eta_c"] = np.mean(elts_rest["g_eta_c"], axis=0)

            for lambda_index in range(lambda_index_stopped):
                if verbose > 1:
                    if lambda_index % 10 == 0:
                        print(f"Lambda {lambda_index}/{lambda_length}")
                if not warmstart:
                    res = None
                res = get_results(elts_rest_, symmetric=True, lambda1=lambda1s[lambda_index],
                                  lambda2=lambda1s[lambda_index] / lambda_ratio, tol=tol, maxit=maxit, previous_res=res,
                                  is_refit=False, use_covariate=use_covariate)
                cv_losses[lambda_index, fold] = calc_crit(elts_this_, res, penalty=False, use_covariate=use_covariate)
    else:
        cv_losses = None
    if verbose > 0:
        print("Done.")

    out_dict = {
        "edgess": edgess,
        "etas": etas,
        "BICs": BICs[:, :len(eBIC_gammas)],
        "BIC_refits": BICs[:, len(eBIC_gammas):],
        "lambda1s": lambda1s,
        "lambda2s": lambda2s,
        "cv_losses": cv_losses,
        "convergeds": convergeds,
        "iters": iters,
        "raw_estimates": raw_estimates,
        "symmetric": symmetric,
        "elts": elts_ret,
    }

    if use_covariate:
        out_dict["eta_cs"] = eta_cs

    return out_dict


def wrap_function(lib, funcname, restype, argtypes):
    """Simplify wrapping ctypes functions"""
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


base_path = Path(__file__)
libc = ctypes.CDLL((base_path / '../../src/simplex_genscore.so').resolve())
libc_cov = ctypes.CDLL((base_path / '../../src/simplex_genscore_cov.so').resolve())


simplex_full_cov = wrap_function(libc_cov, "simplex_full_cov", None, [
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_int),
    np.ctypeslib.ndpointer(c_int),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(c_double),
])


simplex_full = wrap_function(libc, "simplex_full", None, [
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_int),
    np.ctypeslib.ndpointer(c_int),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(c_double),
])

simplex_centered = wrap_function(libc, "simplex_centered", None, [
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(c_int),
    np.ctypeslib.ndpointer(c_double),
    np.ctypeslib.ndpointer(int),
    np.ctypeslib.ndpointer(c_double),
])


def get_results(
        elts: dict,
        symmetric: str = "symmetric",
        lambda1: float = 0.,
        lambda2: float = 0.,
        tol: float = 1e-6,
        maxit: int = 10000,
        previous_res: dict = None,
        is_refit: bool = False,
        use_covariate: bool = False
) -> dict:
    """
    Score matching estimator (wraps C code)
    :param elts: Score matching elements
    :param symmetric: Parameter from genscore. Should always be "symmetric" for simplex models
    :param lambda1: Regularization parameter for K
    :param lambda2: Regularization parameter for eta
    :param tol: Numerical tolerance for convergence
    :param maxit: Maximum number of iterations
    :param previous_res: Previous results for warmstart
    :param is_refit: If True, run in refit mode
    :param use_covariate: If True, use covariate
    :return: Results dictionary
    """

    n = elts["n"]
    p = elts["p"]

    if is_refit:
        if symmetric != previous_res["symmetric"]:
            symmetric = previous_res["symmetric"]
        lambda1 = 0.
        lambda2 = 0.

    if previous_res is None:
        previous_res = {"lambda1": float(lambda1), "K": np.identity(p)}
        exclude = np.zeros((p, p))  # Do not exclude any edge

        previous_res["eta"] = np.zeros(p)
        if use_covariate:
            previous_res["eta_c"] = np.zeros(p)
        exclude_eta = np.zeros(p)  # Initialize eta to the zero vector
    else:
        l2 = previous_res["lambda2"].item()
        l1 = previous_res["lambda1"].item()
        if ((lambda1 != 0) & (np.abs(l1 - lambda1) / lambda1 <= tol) &
                (elts["centered"] | elts["profiled_if_noncenter"] |
                 ((lambda2 == np.inf) & (l2 == np.inf)) |
                 ((lambda2 != np.inf) & (l2 != 0) & (np.abs(l2 - lambda2) / lambda2 <= tol)) &
                 (previous_res["symmetric"] == symmetric) &
                 (maxit == previous_res["maxit"]) &
                 (tol != 0) &
                 (np.abs(previous_res["tol"] - tol) / tol <= tol) &
                 (previous_res["is_refit"] == is_refit))):  # If same parameters as in previous_res, return that
            previous_res["iters"] = 0
            return previous_res

        if previous_res["edges"] is None:  # If no edges given, do not exclude
            exclude = np.zeros((elts["p"], elts["p"]))
        else:  # If edges given, exclude all non-edges
            exclude = np.ones((p, p)) - np.identity(elts["p"])
            for i in range(p):
                for j in range(p):
                    if p * i + j in previous_res["edges"]:
                        exclude[i, j] = 0
            previous_res["K"][exclude == 1] = 0

        if (not elts["centered"]) & (not elts["profiled_if_noncenter"]):
            if previous_res["eta_support"] is None:  # If eta support not given, do not exclude
                exclude_eta = np.zeros(p)
            else:
                exclude_eta = np.repeat(1, elts["p"])
                exclude_eta[previous_res["eta_support"]] = 0
                previous_res["eta"][exclude_eta == 1] = 0
                if use_covariate:
                    previous_res["eta_c"][exclude_eta == 1] = 0

    manual_ncnp_to_c = np.isinf(lambda2)
    if manual_ncnp_to_c:
        elts["centered"] = True
    else:
        elts["centered"] = False

    if elts["sum_to_zero"]:
        previous_res["K"][np.identity(p) == 1] = 0

    if elts["centered"]:
        all_inputs = (
            np.array(elts["p"]),
            np.array(int(elts["sum_to_zero"])),
            np.array(elts["Gamma_K"]).flatten(order="F"),
            np.array(elts["Gamma_K_jp"]).flatten(order="F"),
            np.array(elts["g_K"]).flatten(order="F"),
            np.array(previous_res["K"]).flatten(order="F"),
            np.array(float(lambda1)),
            np.array(tol),
            np.array(maxit),
            np.array(0),
            np.array(0),
            np.array(0.),
            np.array(exclude.astype(np.int32)).flatten(order="F"),
            np.array(float(previous_res["lambda1"])),
            np.array(int(is_refit)),
            np.array(elts["diagonals_with_multiplier"]).flatten(order="F")
        )
        simplex_centered(
            *all_inputs
        )
        test = dict(zip(
            ["p", "sum_to_zero", "Gamma_K", "Gamma_K_jp", "g_K", "K", "lambda1", "tol", "maxit", "iters", "converged",
             "crit", "exclude", "previous_lambda1", "is_refit", "diagonals_with_multiplier"],
            all_inputs
        ))
        for k in ["Gamma_K_jp"]:
            test.pop(k)
    else:
        if use_covariate:
            all_inputs = (np.array(elts["p"]),
                          np.array(int(elts["sum_to_zero"])),
                          np.array(elts["Gamma_K"]).flatten(order="F"),
                          np.array(elts["Gamma_K_eta"]).flatten(order="F"),
                          np.array(elts["Gamma_K_eta_c"]).flatten(order="F"),
                          np.array(elts["Gamma_K_jp"]).flatten(order="F"),
                          np.array(elts["Gamma_Kj_etap"]).flatten(order="F"),
                          np.array(elts["Gamma_Kj_etap_c"]).flatten(order="F"),
                          np.array(elts["Gamma_Kp_etaj"]).flatten(order="F"),
                          np.array(elts["Gamma_Kp_etaj_c"]).flatten(order="F"),
                          np.array(elts["Gamma_eta"]).flatten(order="F"),
                          np.array(elts["Gamma_eta_c"]).flatten(order="F"),
                          np.array(elts["Gamma_eta_c2"]).flatten(order="F"),
                          np.array(elts["Gamma_eta_jp"]).flatten(order="F"),
                          np.array(elts["Gamma_eta_jp_c"]).flatten(order="F"),
                          np.array(elts["Gamma_eta_jp_c2"]).flatten(order="F"),
                          np.array(elts["g_K"]).flatten(order="F"),
                          np.array(elts["g_eta"]).flatten(order="F"),
                          np.array(elts["g_eta_c"]).flatten(order="F"),
                          np.array(previous_res["K"]).flatten(order="F"),
                          np.array(previous_res["eta"]).flatten(order="F"),
                          np.array(previous_res["eta_c"]).flatten(order="F"),
                          np.array(float(lambda1)),
                          np.array(float(lambda2)),
                          np.array(tol),
                          np.array(maxit),
                          np.array(0),
                          np.array(0),
                          np.array(0.),
                          np.array(exclude.astype(np.int32).flatten(order="F")),
                          np.array(exclude_eta.astype(np.int32).flatten(order="F")),
                          np.array(float(previous_res["lambda1"])),
                          np.array(int(is_refit)),
                          np.array(elts["diagonals_with_multiplier"]).flatten(order="F")
                          )
            simplex_full_cov(
                *all_inputs
            )
            test = dict(zip(
                ["p", "sum_to_zero", "Gamma_K", "Gamma_K_eta", "Gamma_K_eta_c", "Gamma_K_jp",
                 "Gamma_Kj_etap", "Gamma_Kj_etap_c", "Gamma_Kp_etaj", "Gamma_Kp_etaj_c",
                 "Gamma_eta", "Gamma_eta_c", "Gamma_eta_c2", "Gamma_eta_jp", "Gamma_eta_jp_c", "Gamma_eta_jp_c2",
                 "g_K", "g_eta", "g_eta_c", "K", "eta", "eta_c", "lambda1", "lambda2", "tol", "maxit", "iters",
                 "converged", "crit", "exclude", "exclude_eta", "previous_lambda1", "is_refit", "diagonals_with_multiplier"],
                all_inputs
            ))
            test["eta_support"] = np.where(np.abs(test["eta"] + test["eta_c"]) > tol)[0]  # For refit
            for k in ["Gamma_K_eta", "Gamma_K_jp", "Gamma_Kj_etap", "Gamma_Kp_etaj", "Gamma_eta", "Gamma_eta_jp",
                      "exclude_eta", "Gamma_K_eta_c", "Gamma_Kj_etap_c", "Gamma_Kp_etaj_c", "Gamma_eta_c",
                      "Gamma_eta_c2", "Gamma_eta_jp_c", "Gamma_eta_jp_c2"]:
                test.pop(k)

        else:
            all_inputs = (np.array(elts["p"]),
                          np.array(int(elts["sum_to_zero"])),
                          np.array(elts["Gamma_K"]).flatten(order="F"),
                          np.array(elts["Gamma_K_eta"]).flatten(order="F"),
                          np.array(elts["Gamma_K_jp"]).flatten(order="F"),
                          np.array(elts["Gamma_Kj_etap"]).flatten(order="F"),
                          np.array(elts["Gamma_Kp_etaj"]).flatten(order="F"),
                          np.array(elts["Gamma_eta"]).flatten(order="F"),
                          np.array(elts["Gamma_eta_jp"]).flatten(order="F"),
                          np.array(elts["g_K"]).flatten(order="F"),
                          np.array(elts["g_eta"]).flatten(order="F"),
                          np.array(previous_res["K"]).flatten(order="F"),
                          np.array(previous_res["eta"]).flatten(order="F"),
                          np.array(float(lambda1)),
                          np.array(float(lambda2)),
                          np.array(tol),
                          np.array(maxit),
                          np.array(0),
                          np.array(0),
                          np.array(0.),
                          np.array(exclude.astype(np.int32).flatten(order="F")),
                          np.array(exclude_eta.astype(np.int32).flatten(order="F")),
                          np.array(float(previous_res["lambda1"])),
                          np.array(int(is_refit)),
                          np.array(elts["diagonals_with_multiplier"]).flatten(order="F")
                          )
            simplex_full(
                *all_inputs
            )
            test = dict(zip(
                ["p", "sum_to_zero", "Gamma_K", "Gamma_K_eta", "Gamma_K_jp", "Gamma_Kj_etap", "Gamma_Kp_etaj", "Gamma_eta",
                 "Gamma_eta_jp", "g_K", "g_eta", "K", "eta", "lambda1", "lambda2", "tol", "maxit", "iters", "converged",
                 "crit", "exclude", "exclude_eta", "previous_lambda1", "is_refit", "diagonals_with_multiplier"],
                all_inputs
            ))
            test["eta_support"] = np.where(np.abs(test["eta"]) > tol)[0]  # For refit
            for k in ["Gamma_K_eta", "Gamma_K_jp", "Gamma_Kj_etap", "Gamma_Kp_etaj", "Gamma_eta", "Gamma_eta_jp",
                      "exclude_eta"]:
                test.pop(k)

    if elts["sum_to_zero"]:
        test["K"] = np.reshape(test["K"], newshape=(p, p))
        for i in range(p):
            test["K"][i, i] = -np.sum(test["K"][i, :])

    test["K"] = np.reshape(test["K"], newshape=(p, p))
    if manual_ncnp_to_c:
        centered = False
        test["eta"] = np.zeros(p)
        test["eta_support"] = 0
        test["lambda2"] = np.inf

    if symmetric == "symmetric":
        ed = np.where((np.abs(test["K"]) > tol) & (np.identity(p) == 0))
        test["edges"] = p * ed[0] + ed[1]  # all off-diagonal
    elif symmetric == "and":
        test["edges"] = np.where((np.abs(test["K"]) > tol) & (np.abs(test["K"].T) > tol) & (np.diag(p) == 0))
    else:  # "or"
        test["edges"] = np.where(((np.abs(test["K"]) > tol) | (np.abs(test["K"].T) > tol)) & (np.identity(p) == 0))
    test["symmetric"] = "symmetric"
    test["n"] = n
    for k in ["diagonals_with_multiplier", "g_K", "Gamma_K", "g_eta", "exclude", "gauss", "g_eta_c"]:
        if k in test:
            test.pop(k)

    return test


def form_gamma_g(
        p: int,
        Gamma_K: np.ndarray,
        Gamma_K_eta: np.ndarray,
        Gamma_K_eta_c: np.ndarray,
        Gamma_eta: np.ndarray,
        Gamma_eta_c: np.ndarray,
        Gamma_eta_c2: np.ndarray,
        Gamma_K_jp: np.ndarray,
        Gamma_Kj_etap: np.ndarray,
        Gamma_Kj_etap_c: np.ndarray,
        Gamma_Kp_etaj: np.ndarray,
        Gamma_Kp_etaj_c: np.ndarray,
        Gamma_eta_jp: np.ndarray,
        Gamma_eta_jp_c: np.ndarray,
        Gamma_eta_jp_c2: np.ndarray,
        g_K: np.ndarray,
        g_eta: np.ndarray,
        g_eta_c: np.ndarray,
        diagonal_multiplier: float,
        cov: np.ndarray = None,
        sum_zero: bool = False,
        aug_method: str = "man"
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Construct Gamma and g from individual components (see paper)
    :param p: Data dimensionality
    :param Gamma_K: Gamma_K
    :param Gamma_K_eta: Gamma_K_eta_0
    :param Gamma_K_eta_c: Gamma_K_eta_1
    :param Gamma_eta: Gamma_eta_0
    :param Gamma_eta_c: Gamma_eta_1
    :param Gamma_eta_c2: Gamma_eta_01
    :param Gamma_K_jp: Gamma_K_jp
    :param Gamma_Kj_etap: Gamma_Kj_etap_0
    :param Gamma_Kj_etap_c: Gamma_Kj_etap_1
    :param Gamma_Kp_etaj: Gamma_Kp_etaj_0
    :param Gamma_Kp_etaj_c: Gamma_Kp_etaj_1
    :param Gamma_eta_jp: Gamma_eta_jp_0
    :param Gamma_eta_jp_c: Gamma_eta_jp_1
    :param Gamma_eta_jp_c2: Gamma_eta_jp_01
    :param g_K: g_K
    :param g_eta: g_eta_0
    :param g_eta_c: g_eta_1
    :param diagonal_multiplier: Diagonal multiplier
    :param cov: Covariate vector
    :param sum_zero: If True, enforce zero sum in rows of K
    :param aug_method: Augmentation method for simplex constraint. EIther "man" or "C", produces identical reults
    :return: Gamma, g
    """

    def make_Cj(p, j):
        Cj = np.zeros((p - 1, p))
        Cj[:, j - 1] = -1
        for i in range(j - 1):
            Cj[i, i] = 1
        for i in range(p - j):
            Cj[j + i - 1, j + i] = 1
        return Cj

    if sum_zero and aug_method == "c":
        C = sp.linalg.block_diag(*[make_Cj(p, j + 1) for j in range(p)])

    Gamma_K_jp_ = Gamma_K_jp.copy()
    r = 0
    r2 = p
    for j in range(p - 1):
        Gamma_K_jp_[:, r:r2] = Gamma_K_jp_[:, r:r2].T
        r2 += p
        r += p

    # Puzzle together Gamma
    gamma_K = sp.linalg.block_diag(*[Gamma_K[:, j * p:(j + 1) * p] for j in range(p)])

    gamma_K[-p:, :(p - 1) * p] = Gamma_K_jp_
    gamma_K[:(p - 1) * p, -p:] = Gamma_K_jp_.T

    if sum_zero and aug_method == "c":
        gamma_K = C @ (gamma_K @ C.T)
        for j in range(p * (p - 1)):
            gamma_K[j, j] *= diagonal_multiplier
    elif sum_zero and aug_method == "man":
        for j in range(p ** 2):
            gamma_K[j, j] *= diagonal_multiplier

        # for j in range(p):
        #     gamma_K = np.delete(gamma_K, j * p, axis=0)
        #     gamma_K = np.delete(gamma_K, j * p, axis=1)

        gamma_K = np.delete(gamma_K, [j * p + j for j in range(p)], axis=0)
        gamma_K = np.delete(gamma_K, [j * p + j for j in range(p)], axis=1)
    else:
        for j in range(p ** 2):
            gamma_K[j, j] *= diagonal_multiplier

    gamma_K_eta = sp.linalg.block_diag(*[Gamma_K_eta[:, [j]] for j in range(p)])
    gamma_K_eta[-p:, :(p - 1)] = Gamma_Kp_etaj

    for j in range(p - 1):
        gamma_K_eta[j * p:p * (j + 1), -1] = Gamma_Kj_etap[:, j]
    if sum_zero and aug_method == "c":
        gamma_K_eta = C @ gamma_K_eta
    elif sum_zero and aug_method == "man":
        for j in range(p):
            gamma_K_eta = np.delete(gamma_K_eta, j * p, axis=0)

    gamma_K_eta_c = sp.linalg.block_diag(*[Gamma_K_eta_c[:, [j]] for j in range(p)])
    gamma_K_eta_c[-p:, :(p - 1)] = Gamma_Kp_etaj_c

    for j in range(p - 1):
        gamma_K_eta_c[j * p:p * (j + 1), -1] = Gamma_Kj_etap_c[:, j]
    if sum_zero and aug_method == "c":
        gamma_K_eta_c = C @ gamma_K_eta_c
    elif sum_zero and aug_method == "man":
        for j in range(p):
            gamma_K_eta_c = np.delete(gamma_K_eta_c, j * p, axis=0)

    gamma_eta = np.diag(Gamma_eta.flatten())
    gamma_eta[-1, :p - 1] = Gamma_eta_jp
    gamma_eta[:p - 1, -1] = Gamma_eta_jp

    gamma_eta_c = np.diag(Gamma_eta_c.flatten())
    gamma_eta_c[-1, :p - 1] = Gamma_eta_jp_c
    gamma_eta_c[:p - 1, -1] = Gamma_eta_jp_c

    gamma_eta_c2 = np.diag(Gamma_eta_c2.flatten())
    gamma_eta_c2[-1, :p - 1] = Gamma_eta_jp_c2
    gamma_eta_c2[:p - 1, -1] = Gamma_eta_jp_c2

    if cov is not None:

        gamma = np.block([[gamma_K, gamma_K_eta, gamma_K_eta_c],
                          [gamma_K_eta.T, gamma_eta, gamma_eta_c],
                          [gamma_K_eta_c.T, gamma_eta_c, gamma_eta_c2]])

    else:
        gamma = np.block([[gamma_K, gamma_K_eta],
                          [gamma_K_eta.T, gamma_eta]])

    if sum_zero and aug_method == "c":
        g_K_ = np.einsum("ij, kj -> ki", C, g_K)
    elif sum_zero and aug_method == "man":
        g_K_ = g_K.copy()
        for j in range(p):
            g_K_ = np.delete(g_K_, j * p, axis=0)
    else:
        g_K_ = g_K.copy()

    if cov is not None:
        g = np.concatenate([g_K_, g_eta, g_eta_c])
    else:
        g = np.concatenate([g_K_, g_eta])

    return gamma, g


def da_test(res: dict, lambda_id: int, cov: np.ndarray, verbose: int = 0) -> pd.DataFrame:
    """
    Perform differential abundance test
    :param res: Score matching results
    :param lambda_id: Index of regularization strength to consider
    :param cov: Covaiate vector
    :param verbose: Verbosity level (0: No Outputs; 1: Notify for major steps; 2: Notify about progress)
    :return: DA testing results DataFrame
    """

    sum_zero = res["elts"]["sum_to_zero"]
    n = res["elts"]["n"]
    p = res["elts"]["p"]

    K_fin = res["raw_estimates"][lambda_id]
    eta_0_fin = res["etas"][lambda_id]
    eta_c_fin = res["eta_cs"][lambda_id]

    K_fin_red = K_fin.reshape(p ** 2, order="F")
    if sum_zero:
        K_fin_red = np.delete(K_fin_red, [i * p + i for i in range(p)])
    sol = np.concatenate((K_fin_red, eta_0_fin, eta_c_fin))

    gamma, g = form_gamma_g(
        p=p,
        Gamma_K=np.mean(res["elts"]["Gamma_K"], axis=0),
        Gamma_K_eta=np.mean(res["elts"]["Gamma_K_eta"], axis=0),
        Gamma_K_eta_c=np.mean(res["elts"]["Gamma_K_eta_c"], axis=0),
        Gamma_eta=np.mean(res["elts"]["Gamma_eta"], axis=0),
        Gamma_eta_c=np.mean(res["elts"]["Gamma_eta_c"], axis=0),
        Gamma_eta_c2=np.mean(res["elts"]["Gamma_eta_c2"], axis=0),
        Gamma_K_jp=np.mean(res["elts"]["Gamma_K_jp"], axis=0),
        Gamma_Kj_etap=np.mean(res["elts"]["Gamma_Kj_etap"], axis=0),
        Gamma_Kj_etap_c=np.mean(res["elts"]["Gamma_Kj_etap_c"], axis=0),
        Gamma_Kp_etaj=np.mean(res["elts"]["Gamma_Kp_etaj"], axis=0),
        Gamma_Kp_etaj_c=np.mean(res["elts"]["Gamma_Kp_etaj_c"], axis=0),
        Gamma_eta_jp=np.mean(res["elts"]["Gamma_eta_jp"], axis=0),
        Gamma_eta_jp_c=np.mean(res["elts"]["Gamma_eta_jp_c"], axis=0),
        Gamma_eta_jp_c2=np.mean(res["elts"]["Gamma_eta_jp_c2"], axis=0),
        g_K=np.mean(res["elts"]["g_K"], axis=0),
        g_eta=np.mean(res["elts"]["g_eta"], axis=0),
        g_eta_c=np.mean(res["elts"]["g_eta_c"], axis=0),
        diagonal_multiplier=res["elts"]["diagonal_multiplier"],
        cov=cov,
        sum_zero=res["elts"]["sum_to_zero"],
        aug_method="man"
    )

    diffs = []
    for i in range(n):
        if verbose > 0:
            if i % int(n/10) == 0:
                print(f"Sample {i}/{n}")
        gamma_i, g_i = form_gamma_g(
            p,
            res["elts"]["Gamma_K"][i, :, :],
            res["elts"]["Gamma_K_eta"][i, :, :],
            res["elts"]["Gamma_K_eta_c"][i, :, :],
            res["elts"]["Gamma_eta"][i, :, :],
            res["elts"]["Gamma_eta_c"][i, :, :],
            res["elts"]["Gamma_eta_c2"][i, :, :],
            res["elts"]["Gamma_K_jp"][i, :, :],
            res["elts"]["Gamma_Kj_etap"][i, :, :],
            res["elts"]["Gamma_Kj_etap_c"][i, :, :],
            res["elts"]["Gamma_Kp_etaj"][i, :, :],
            res["elts"]["Gamma_Kp_etaj_c"][i, :, :],
            res["elts"]["Gamma_eta_jp"][i, :],
            res["elts"]["Gamma_eta_jp_c"][i, :],
            res["elts"]["Gamma_eta_jp_c2"][i, :],
            res["elts"]["g_K"][i, :],
            res["elts"]["g_eta"][i, :],
            res["elts"]["g_eta_c"][i, :],
            diagonal_multiplier=res["elts"]["diagonal_multiplier"],
            cov=cov,
            sum_zero=res["elts"]["sum_to_zero"],
            aug_method="man"
        )
        diffs.append((g_i - np.einsum("jk, j -> k", gamma_i, sol)))
    if verbose > 0:
        print("testing")
    diff = np.column_stack(diffs)

    Sig0 = (diff @ diff.T) / n

    gamma_inv = np.linalg.inv(gamma)
    var0 = np.diag((gamma_inv @ Sig0 @ gamma_inv) / n).copy()

    if sum_zero:
        for j in range(p):
            sol = np.insert(sol, j * p + j, -np.sum(sol[j * p:(j + 1) * p]))
            var0 = np.insert(var0, j * p + j, np.mean(var0[j * p:((j + 1) * p - 1)]))

    std = np.sqrt(var0)

    test_stat = -np.abs(sol / std)
    # test_stat = sol**2 / var0
    pval = sp.stats.norm.cdf(test_stat) * 2

    # pval = sp.stats.t.cdf(test_stat, df=n-3) * 2

    qval = mt.multipletests(
        pval[-2 * p:-p], method="fdr_bh")[1].tolist() + mt.multipletests(pval[-p:],
    method="fdr_bh")[1].tolist()

    parameters = [f"eta_0_{i}" for i in range(p)] + [f"eta_c_{i}" for i in range(p)]
    param_df_x_full = pd.DataFrame(
        {"Parameter": parameters, "estimate": sol[-2 * p:], "std": std[-2 * p:], "pval": pval[-2 * p:], "qval": qval})

    return param_df_x_full


def get_K_eta_cv(
        data: np.ndarray,
        est: dict,
        se: bool = True
) -> Union[Tuple[int, float, np.ndarray, np.ndarray], Tuple[int, float, np.ndarray, np.ndarray, np.ndarray]]:
    """
    Evaluate regularization to find best value for lambda_1
    :param data: Input data
    :param est: Estimation results
    :param se: If True, use 1-standard-error rule
    :return: Index of best lambda_1, value of best lambda_1, K corresponding to best lambda_1,
    eta_0 corresponding to best lambda_1, eta_1 corresponding to best lambda_1 (only if covariate was used)
    """
    n, p = data.shape
    cv_losses = np.mean(est["cv_losses"], axis=1)

    lambda_cv_id = np.where(cv_losses == np.min(cv_losses))[0][0]
    lambda_cv = est["lambda1s"][lambda_cv_id]

    if se:
        cv_stds = np.std(est["cv_losses"], axis=1) / np.sqrt(2 * n)
        lambda_cv_id = np.where(cv_losses <= (np.min(cv_losses) + cv_stds[lambda_cv_id]))[0][0]
        lambda_cv = est["lambda1s"][lambda_cv_id]

    K_opt = est["raw_estimates"][lambda_cv_id]
    eta_0_opt = est["etas"][lambda_cv_id]
    if "eta_cs" in est.keys():
        eta_c_opt = est["eta_cs"][lambda_cv_id]

        return lambda_cv_id, lambda_cv, K_opt, eta_0_opt, eta_c_opt
    else:
        return lambda_cv_id, lambda_cv, K_opt, eta_0_opt
