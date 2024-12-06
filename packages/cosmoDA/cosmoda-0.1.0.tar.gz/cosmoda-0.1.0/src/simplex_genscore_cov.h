//
//  simplex_genscore_cov.h
//
//
//  Created by Johannes Ostner on 2024-07-03.
//
//

#ifndef FUNCTIONS_H_INCLUDED
#define FUNCTIONS_H_INCLUDED
#endif

// void elts_loglog_simplex_c(int *nIn, int *pIn, double *hx, double *hpx, double *x, int *sum_to_zero, double *g_K, double *Gamma_K, double *Gamma_K_jp, double *Gamma_eta, double *Gamma_eta_jp, double *diagonal_multiplier, double *diagonals_with_multiplier, double *logx, double *h_over_xsq_nop, double *minus_h_over_x_xp_nop, double *sum_h_over_xmsq, double *hp_over_x_nop, double *sum_hp_over_xm, double *mean_sum_h_over_xmsq);
void test_loss_loglog_simplex_full_penalized_cov(double *out, int *pIn, double *Gamma_K, double *Gamma_K_eta, double *Gamma_K_eta_c, double *Gamma_K_jp, double *Gamma_Kj_etap, double *Gamma_Kj_etap_c, double *Gamma_Kp_etaj, double *Gamma_Kp_etaj_c, double *Gamma_eta, double *Gamma_eta_c, double *Gamma_eta_c2, double *Gamma_eta_jp, double *Gamma_eta_jp_c, double *Gamma_eta_jp_c2, double *g_K, double *g_eta, double *g_eta_c, double *K, double *eta, double *eta_c, double *diagonals_with_multiplier, double *lambda_1, double *lambda_2);

void simplex_full_cov(int *pIn, int *sum_to_zero, double *Gamma_K, double *Gamma_K_eta, double *Gamma_K_eta_c, double *Gamma_K_jp, double *Gamma_Kj_etap, double *Gamma_Kj_etap_c, double *Gamma_Kp_etaj, double *Gamma_Kp_etaj_c, double *Gamma_eta, double *Gamma_eta_c, double *Gamma_eta_c2, double *Gamma_eta_jp, double *Gamma_eta_jp_c, double *Gamma_eta_jp_c2, double *g_K, double *g_eta, double *g_eta_c, double *K, double *eta, double *eta_c, double *lambda1In, double *lambda2In, double *tol, int *maxit, int *iters, int *converged, double *crit, int *exclude, int *exclude_eta, double *previous_lambda1, int *is_refit, double *diagonals_with_multiplier);
void estimator_simplex_full_cov(int *pIn, int *sum_to_zero, double *Gamma_K, double *Gamma_K_eta, double *Gamma_K_eta_c, double *Gamma_K_jp, double *Gamma_Kj_etap, double *Gamma_Kj_etap_c, double *Gamma_Kp_etaj, double *Gamma_Kp_etaj_c, double *Gamma_eta, double *Gamma_eta_c, double *Gamma_eta_c2, double *Gamma_eta_jp, double *Gamma_eta_jp_c, double *Gamma_eta_jp_c2, double *g_K, double *g_eta, double *g_eta_c, double *K, double *eta, double *eta_c, double *lambda1In, double *lambda2In, double *tol, int *maxit, int *iters, int *converged, int *exclude, int *exclude_eta, double *diagonals_with_multiplier);
