#!/usr/bin/env python3
"""
Sub-analyses and world map visualizations for global monarch Weibull analysis.
1. Sub-analysis 1: Elective vs Hereditary succession
2. Sub-analysis 2: By era (Ancient/Medieval/Early Modern/Modern/Contemporary)
3. World map visualization of main analysis
4. Box plots and ridge plots
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'DejaVu Sans'

# =============================================================================
# Reuse functions from main script
# =============================================================================

def weibull_mle_closed(data):
    """Fast closed-form Weibull MLE using Newton-Raphson."""
    data = data[data > 0]
    if len(data) < 5:
        return None, None
    n = len(data)
    ln_x = np.log(data)
    sorted_d = np.sort(data)
    F_i = (np.arange(1, n + 1) - 0.3) / (n + 0.4)
    try:
        slope, intercept, _, _, _ = stats.linregress(np.log(sorted_d), np.log(-np.log(1 - F_i)))
    except:
        return None, None
    k = max(slope, 0.5)
    for _ in range(100):
        xk = data ** k
        sum_xk = np.sum(xk)
        if sum_xk == 0:
            return None, None
        sum_xk_lnx = np.sum(xk * ln_x)
        f = np.sum(ln_x) / n + 1.0 / k - sum_xk_lnx / sum_xk
        sum_xk_lnx2 = np.sum(xk * ln_x ** 2)
        df = -1.0 / k**2 - (sum_xk_lnx2 * sum_xk - sum_xk_lnx**2) / sum_xk**2
        if abs(df) < 1e-15:
            break
        k_new = k - f / df
        if k_new <= 0:
            k_new = k / 2
        if abs(k_new - k) < 1e-8:
            k = k_new
            break
        k = k_new
    lam = (np.sum(data ** k) / n) ** (1.0 / k)
    return k, lam


def fit_region(durations):
    """Fit Weibull to a region's reign durations and return metrics."""
    durations = np.array(durations, dtype=float)
    durations = durations[durations > 0]
    n = len(durations)
    if n < 5:
        return None
    try:
        shape, loc, scale = stats.weibull_min.fit(durations, floc=0)
    except:
        shape, scale = weibull_mle_closed(durations)
        if shape is None:
            return None
        loc = 0
    ks_stat, ks_p = stats.kstest(durations, 'weibull_min', args=(shape, 0, scale))
    sorted_d = np.sort(durations)
    F_i = (np.arange(1, n + 1) - 0.3) / (n + 0.4)
    try:
        x_plot = np.log(sorted_d)
        y_plot = np.log(-np.log(1 - F_i))
        _, _, r_value, _, _ = stats.linregress(x_plot, y_plot)
        r2 = r_value**2
    except:
        r2 = 0
    k_boots = []
    np.random.seed(42)
    for _ in range(500):
        bs = np.random.choice(durations, size=n, replace=True)
        bs = bs[bs > 0]
        if len(bs) >= 5:
            try:
                s, _, sc = stats.weibull_min.fit(bs, floc=0)
                if 0.05 < s < 30:
                    k_boots.append(s)
            except:
                k_b, _ = weibull_mle_closed(bs)
                if k_b and 0.05 < k_b < 30:
                    k_boots.append(k_b)
    k_boots = np.array(k_boots)
    k_ci = np.percentile(k_boots, [2.5, 97.5]) if len(k_boots) > 10 else [np.nan, np.nan]
    return {
        'k': shape, 'lambda': scale, 'n': n,
        'ks_p': ks_p, 'r2': r2,
        'k_ci_low': k_ci[0], 'k_ci_high': k_ci[1],
        'mean_reign': np.mean(durations),
        'median_reign': np.median(durations),
    }


# =============================================================================
# DATA: Region metadata with selection type + era + coordinates
# =============================================================================

# Each region: durations, region_category, selection_type, approximate_era_range, map_coords (lat, lon)
# selection_type: 'elective' or 'hereditary'
# era_range: (start_year, end_year) for assigning to eras

REGIONS = {}

# --- EUROPE ---
REGIONS["Roman Empire"] = {
    'durations': [41, 23, 4, 14, 1, 1, 0.5, 0.5, 10, 2, 15, 2, 1, 21, 23,
                  19, 8, 13, 1, 4, 4, 13, 6, 3, 0.25, 2, 3, 0.5, 3, 15,
                  5, 1, 6, 2, 1, 2, 1, 21, 1, 13, 24, 2, 3, 2, 8,
                  16, 4, 13, 1, 15, 5, 1, 5, 1, 1],
    'region_category': 'Europe', 'selection': 'elective',
    'era': (-27, 476), 'coords': (41.9, 12.5),  # Rome
}

REGIONS["England/Britain"] = {
    'durations': [21, 13, 35, 19, 10, 10, 17, 3, 56, 20, 50, 22, 2, 13, 10,
                  22, 2, 22, 24, 38, 6, 5, 45, 22, 6, 11, 25, 3, 13, 12,
                  13, 33, 60, 10, 26, 64, 9, 26, 16, 70],
    'region_category': 'Europe', 'selection': 'hereditary',
    'era': (1066, 2022), 'coords': (51.5, -0.1),  # London
}

REGIONS["France"] = {
    'durations': [9, 26, 29, 29, 48, 43, 44, 3, 17, 6, 29, 6, 6, 5, 33,
                  22, 14, 42, 39, 3, 22, 15, 33, 12, 72, 1, 14, 19, 22, 4,
                  72, 5, 59, 16, 10, 6, 10, 18],
    'region_category': 'Europe', 'selection': 'hereditary',
    'era': (987, 1870), 'coords': (48.9, 2.3),  # Paris
}

REGIONS["Holy Roman Empire"] = {
    'durations': [37, 23, 22, 2, 17, 17, 39, 20, 18, 2, 38, 7, 18, 4, 37,
                  2, 17, 6, 37, 12, 32, 1, 10, 53, 27, 3, 53, 12, 10, 6,
                  12, 25, 5, 20, 7, 47, 6, 1, 29, 5, 10, 2, 14],
    'region_category': 'Europe', 'selection': 'elective',
    'era': (962, 1806), 'coords': (50.1, 8.7),  # Frankfurt
}

REGIONS["Denmark"] = {
    'durations': [28, 27, 8, 42, 5, 7, 22, 25, 23, 18, 17, 3, 13, 8, 16,
                  20, 12, 9, 7, 9, 19, 33, 20, 43, 16, 16, 18, 31, 24, 17,
                  11, 26, 24, 3, 11, 29, 31, 12, 20, 40, 31, 9, 28, 17, 57,
                  6, 35, 27, 52],
    'region_category': 'Europe', 'selection': 'hereditary',
    'era': (936, 2024), 'coords': (55.7, 12.6),  # Copenhagen
}

REGIONS["Sweden"] = {
    'durations': [37, 29, 3, 43, 25, 21, 6, 38, 5, 21, 36, 20, 19, 23, 28,
                  5, 26, 37, 57, 23, 43, 23, 52],
    'region_category': 'Europe', 'selection': 'hereditary',
    'era': (1523, 2024), 'coords': (59.3, 18.1),  # Stockholm
}

REGIONS["Scotland"] = {
    'durations': [24, 19, 16, 15, 8, 9, 43, 5, 9, 12, 4, 25, 8, 29, 17,
                  17, 24, 35, 16, 4, 17, 25, 11, 36, 19, 35, 4, 23, 42, 28,
                  16, 11, 13, 25, 26, 29, 26, 19, 6, 37],
    'region_category': 'Europe', 'selection': 'hereditary',
    'era': (843, 1603), 'coords': (55.9, -3.2),  # Edinburgh
}

REGIONS["Spain"] = {
    'durations': [12, 26, 40, 42, 23, 35, 5, 13, 46, 23, 21, 5, 25, 35, 2,
                  17, 41, 39],
    'region_category': 'Europe', 'selection': 'hereditary',
    'era': (1479, 2024), 'coords': (40.4, -3.7),  # Madrid
}

REGIONS["Portugal"] = {
    'durations': [28, 27, 38, 6, 46, 46, 6, 12, 38, 28, 5, 6, 38, 14, 3,
                  26, 37, 4, 3, 22, 16, 13, 27, 44, 5, 10, 21, 7, 2, 19, 2],
    'region_category': 'Europe', 'selection': 'hereditary',
    'era': (1139, 1910), 'coords': (38.7, -9.1),  # Lisbon
}

REGIONS["Poland"] = {
    'durations': [33, 34, 13, 6, 13, 36, 8, 24, 44, 8, 32, 7, 33, 37, 3,
                  14, 2, 48, 6, 5, 42, 24, 5, 20, 24, 16, 20, 5, 22, 31,
                  30, 31],
    'region_category': 'Europe', 'selection': 'elective',
    'era': (960, 1795), 'coords': (52.2, 21.0),  # Warsaw
}

REGIONS["Russia"] = {
    'durations': [43, 3, 51, 3, 5, 2, 0.5, 32, 8, 3, 7, 36, 2, 25, 20,
                  1, 21, 6, 34, 5, 25, 30, 13, 26, 23],
    'region_category': 'Europe', 'selection': 'hereditary',
    'era': (1462, 1917), 'coords': (55.8, 37.6),  # Moscow
}

# --- MIDDLE EAST ---
REGIONS["Ottoman Empire"] = {
    'durations': [27, 36, 23, 10, 2, 30, 31, 2, 31, 8, 46, 8, 21, 3, 20,
                  14, 1, 4, 18, 4, 39, 8, 27, 24, 3, 27, 17, 3, 16, 24,
                  4, 31, 1, 15, 33, 33, 9, 6, 4],
    'region_category': 'Middle East', 'selection': 'hereditary',
    'era': (1299, 1922), 'coords': (41.0, 29.0),  # Istanbul
}

REGIONS["Islamic Caliphate"] = {
    'durations': [2, 10, 12, 5, 19, 3, 1, 21, 4, 20, 2, 3, 20, 1, 19, 1, 1, 1, 6,
                  4, 22, 10, 10, 23, 5, 20, 1, 15, 14, 1, 6, 0.5, 10, 23,
                  9, 15, 24, 1, 6, 4, 1, 2, 5, 29, 41, 13, 23, 12, 35,
                  17, 12, 1, 36, 1, 17],
    'region_category': 'Middle East', 'selection': 'elective',
    'era': (632, 1258), 'coords': (33.3, 44.4),  # Baghdad
}

REGIONS["Mamluk Sultanate"] = {
    'durations': [7, 17, 2, 1, 12, 1, 9, 42, 1, 0.5, 2, 3, 6, 2, 1,
                  13, 1, 6, 21, 1, 7, 1, 5, 15, 1, 16, 1],
    'region_category': 'Middle East', 'selection': 'elective',
    'era': (1250, 1517), 'coords': (30.0, 31.2),  # Cairo
}

REGIONS["Persia/Iran"] = {
    'durations': [24, 10, 52, 14, 17, 17, 13, 5, 7, 2, 11, 0.5, 1,
                  16, 37, 48, 1, 16, 6, 16, 16, 38],
    'region_category': 'Middle East', 'selection': 'hereditary',
    'era': (1501, 1979), 'coords': (35.7, 51.4),  # Tehran
}

# --- ASIA ---
REGIONS["Japan (Emperors)"] = {
    'durations': [32, 13, 2, 5, 35, 12, 9, 4, 14, 7, 7, 10, 8, 9, 25,
                  9, 6, 11, 3, 13, 25, 3, 14, 10, 17, 8, 18, 8, 3, 10,
                  33, 16, 21, 2, 15, 2, 25, 5, 20, 9, 14, 20, 16, 19, 16,
                  3, 15, 12, 11, 0.5, 11, 10, 14, 13, 9, 13, 11, 3, 10, 21,
                  29, 15, 9, 20, 16, 36, 36, 26, 30, 25, 18, 14, 11, 9, 24,
                  22, 26, 12, 15, 9, 37, 29, 21, 45, 14, 30],
    'region_category': 'Asia', 'selection': 'hereditary',
    'era': (539, 2019), 'coords': (35.7, 139.7),  # Tokyo
}

REGIONS["China (Tang)"] = {
    'durations': [9, 23, 1, 22, 34, 6, 2, 29, 6, 14, 26, 1, 15, 1, 7,
                  14, 6, 13, 1, 16, 15, 4],
    'region_category': 'Asia', 'selection': 'hereditary',
    'era': (618, 907), 'coords': (34.3, 108.9),  # Xi'an
}

REGIONS["China (Ming)"] = {
    'durations': [31, 4, 22, 1, 10, 14, 8, 23, 6, 18, 16, 45, 6, 48, 29, 7, 17],
    'region_category': 'Asia', 'selection': 'hereditary',
    'era': (1368, 1644), 'coords': (39.9, 116.4),  # Beijing
}

REGIONS["China (Qing)"] = {
    'durations': [18, 8, 61, 13, 45, 25, 7, 30, 11, 2, 3],
    'region_category': 'Asia', 'selection': 'hereditary',
    'era': (1644, 1912), 'coords': (39.9, 116.4),  # Beijing (offset in plot)
}

REGIONS["Korea (Joseon)"] = {
    'durations': [6, 18, 32, 22, 4, 2, 13, 1, 25, 12, 38, 12, 2, 34, 8,
                  16, 27, 10, 15, 46, 4, 52, 15, 3, 14, 34, 10, 13],
    'region_category': 'Asia', 'selection': 'hereditary',
    'era': (1392, 1897), 'coords': (37.6, 127.0),  # Seoul
}

REGIONS["Korea (Goryeo)"] = {
    'durations': [26, 4, 26, 16, 6, 4, 12, 12, 2, 13, 12, 9, 1, 17, 23,
                  24, 23, 46, 7, 2, 24, 34, 11, 10, 4, 13, 10, 5, 8, 24,
                  14, 3, 2],
    'region_category': 'Asia', 'selection': 'hereditary',
    'era': (918, 1392), 'coords': (37.9, 126.6),  # Kaesong
}

REGIONS["Mughal Empire"] = {
    'durations': [4, 10, 13, 49, 22, 49, 1, 17, 0.5, 8, 29, 6, 1, 7, 19],
    'region_category': 'Asia', 'selection': 'hereditary',
    'era': (1526, 1857), 'coords': (28.6, 77.2),  # Delhi
}

REGIONS["Khmer Empire"] = {
    'durations': [48, 35, 13, 7, 6, 28, 30, 12, 15, 50, 37, 25, 4, 10, 2,
                  16, 5, 8, 12, 20],
    'region_category': 'Asia', 'selection': 'hereditary',
    'era': (802, 1431), 'coords': (13.4, 103.9),  # Angkor
}

REGIONS["Thailand (Chakri)"] = {
    'durations': [27, 15, 27, 47, 16, 15, 9, 18, 70, 7],
    'region_category': 'Asia', 'selection': 'hereditary',
    'era': (1782, 2024), 'coords': (13.8, 100.5),  # Bangkok
}

# --- AFRICA / ANCIENT ---
REGIONS["Egypt (New Kingdom)"] = {
    'durations': [21, 13, 22, 54, 9, 22, 54, 10, 26, 38, 17, 3, 1, 10, 67,
                  11, 67, 10, 34, 6, 2, 19, 7, 32, 25, 8, 7, 8, 1, 9, 27],
    'region_category': 'Africa/Middle East', 'selection': 'hereditary',
    'era': (-1550, -1077), 'coords': (25.7, 32.6),  # Luxor
}

REGIONS["Ethiopia"] = {
    'durations': [15, 14, 6, 29, 2, 5, 10, 1, 15, 33, 4, 16, 1, 12, 2,
                  19, 7, 23, 3, 38, 5, 11, 24, 9, 7, 4, 44],
    'region_category': 'Africa', 'selection': 'hereditary',
    'era': (1270, 1974), 'coords': (9.0, 38.7),  # Addis Ababa
}

REGIONS["Byzantine Empire"] = {
    'durations': [11, 27, 8, 9, 12, 9, 27, 38, 3, 4, 20, 8, 2, 13, 33,
                  17, 6, 1, 31, 7, 34, 5, 5, 10, 5, 7, 9, 2, 25, 23,
                  26, 6, 46, 2, 49, 6, 3, 14, 12, 25, 7, 4, 6, 2, 23,
                  3, 3, 37, 3, 7, 37, 25, 5, 3, 33, 9, 4, 1, 57, 6,
                  33, 18, 3, 24, 6, 6, 9, 5, 21, 4, 4],
    'region_category': 'Europe', 'selection': 'elective',
    'era': (395, 1453), 'coords': (41.0, 28.9),  # Constantinople
}

# --- RELIGIOUS ---
REGIONS["Papacy (post-1000)"] = {
    'durations': [4, 12, 1, 8, 6, 12, 1, 9, 23, 13, 6, 2, 12, 1, 0.5,
                  13, 16, 0.5, 1, 8, 5, 14, 8, 3, 4, 1, 5, 22, 0.5, 5,
                  6, 18, 11, 1, 15, 14, 2, 0.5, 3, 4, 3, 10, 3, 2, 2,
                  3, 4, 2, 9, 11, 9, 1, 7, 19, 2, 10, 1, 9, 16, 12,
                  2, 12, 3, 14, 8, 3, 6, 13, 0.5, 26, 8, 11, 10, 2, 21,
                  11, 15, 5, 0.3, 4, 6, 13, 1, 6, 15, 1, 8, 26, 3, 2,
                  21, 10, 7, 2, 13, 13, 2, 5, 21, 8, 6, 10, 8, 17, 6,
                  23, 7, 2, 32, 4, 32, 25, 3, 10, 17, 19, 5, 15, 34, 8, 11],
    'region_category': 'Europe', 'selection': 'elective',
    'era': (1000, 2024), 'coords': (41.9, 12.45),  # Vatican
}

# --- AMERICAS ---
REGIONS["USA (Presidents)"] = {
    'durations': [8, 4, 8, 8, 4, 4, 4, 8, 4, 4, 4, 3, 4, 8, 4,
                  4, 4, 8, 4, 4, 4, 4, 4, 8, 7, 4, 8, 4, 12, 4,
                  8, 8, 3, 5, 4, 4, 8, 4, 8, 8, 4, 4],
    'region_category': 'Americas', 'selection': 'elective',
    'era': (1789, 2024), 'coords': (38.9, -77.0),  # Washington DC
}


# =============================================================================
# FIT ALL REGIONS
# =============================================================================

print("=" * 70)
print("  SUB-ANALYSES: ELECTIVE vs HEREDITARY + ERA-BASED")
print("=" * 70)

results = {}
for name, info in sorted(REGIONS.items()):
    durs = np.array(info['durations'], dtype=float)
    fit = fit_region(durs)
    if fit:
        fit['region_category'] = info['region_category']
        fit['selection'] = info['selection']
        fit['era'] = info['era']
        fit['coords'] = info['coords']
        results[name] = fit
        print(f"  {name:30s}  N={fit['n']:3d}  k={fit['k']:.3f}  [{info['selection']:10s}]  {info['era']}")

# =============================================================================
# SUB-ANALYSIS 1: ELECTIVE vs HEREDITARY
# =============================================================================

print("\n" + "=" * 70)
print("  SUB-ANALYSIS 1: ELECTIVE vs HEREDITARY SUCCESSION")
print("=" * 70)

elective_regions = {n: r for n, r in results.items() if r['selection'] == 'elective'}
hereditary_regions = {n: r for n, r in results.items() if r['selection'] == 'hereditary'}

# Pool all durations
elective_durs = []
for name in elective_regions:
    elective_durs.extend(REGIONS[name]['durations'])
elective_durs = np.array(elective_durs, dtype=float)
elective_durs = elective_durs[elective_durs > 0]

hereditary_durs = []
for name in hereditary_regions:
    hereditary_durs.extend(REGIONS[name]['durations'])
hereditary_durs = np.array(hereditary_durs, dtype=float)
hereditary_durs = hereditary_durs[hereditary_durs > 0]

elective_fit = fit_region(elective_durs)
hereditary_fit = fit_region(hereditary_durs)

print(f"\n  Elective/Selection-based ({len(elective_regions)} regions):")
for n, r in sorted(elective_regions.items(), key=lambda x: x[1]['k']):
    print(f"    {n:30s}  k={r['k']:.3f}  N={r['n']}")
print(f"    {'POOLED':30s}  k={elective_fit['k']:.3f}  N={elective_fit['n']}  "
      f"mean={elective_fit['mean_reign']:.1f}y  KS p={elective_fit['ks_p']:.3f}")

print(f"\n  Hereditary ({len(hereditary_regions)} regions):")
for n, r in sorted(hereditary_regions.items(), key=lambda x: x[1]['k']):
    print(f"    {n:30s}  k={r['k']:.3f}  N={r['n']}")
print(f"    {'POOLED':30s}  k={hereditary_fit['k']:.3f}  N={hereditary_fit['n']}  "
      f"mean={hereditary_fit['mean_reign']:.1f}y  KS p={hereditary_fit['ks_p']:.3f}")

# Two-sample KS test
ks_stat_sel, ks_p_sel = stats.ks_2samp(elective_durs, hereditary_durs)
# Mann-Whitney U test
u_stat, u_p = stats.mannwhitneyu(elective_durs, hereditary_durs, alternative='two-sided')
print(f"\n  Two-sample comparison:")
print(f"    KS test: D={ks_stat_sel:.4f}, p={ks_p_sel:.4f}")
print(f"    Mann-Whitney U: U={u_stat:.0f}, p={u_p:.4f}")
print(f"    Elective k={elective_fit['k']:.3f} vs Hereditary k={hereditary_fit['k']:.3f}")

# Bootstrap test for k difference
print("  Bootstrap test for k difference (1000 resamples)...")
np.random.seed(42)
k_diff_boots = []
for _ in range(1000):
    bs_e = np.random.choice(elective_durs, size=len(elective_durs), replace=True)
    bs_e = bs_e[bs_e > 0]
    bs_h = np.random.choice(hereditary_durs, size=len(hereditary_durs), replace=True)
    bs_h = bs_h[bs_h > 0]
    if len(bs_e) >= 5 and len(bs_h) >= 5:
        ke, _ = weibull_mle_closed(bs_e)
        kh, _ = weibull_mle_closed(bs_h)
        if ke and kh and 0.05 < ke < 30 and 0.05 < kh < 30:
            k_diff_boots.append(kh - ke)
k_diff_boots = np.array(k_diff_boots)
if len(k_diff_boots) > 10:
    ci = np.percentile(k_diff_boots, [2.5, 97.5])
    prob_h_gt_e = np.mean(k_diff_boots > 0)
    print(f"    P(k_hereditary > k_elective) = {prob_h_gt_e:.3f}")
    print(f"    Difference 95% CI: [{ci[0]:.3f}, {ci[1]:.3f}]")


# =============================================================================
# SUB-ANALYSIS 2: BY ERA
# =============================================================================

print("\n" + "=" * 70)
print("  SUB-ANALYSIS 2: BY ERA")
print("=" * 70)

# Era definitions
ERAS = {
    'Ancient': (-5000, 476),
    'Medieval': (476, 1453),
    'Early Modern': (1453, 1789),
    'Modern': (1789, 1945),
    'Contemporary': (1945, 2100),
}

ERA_COLORS = {
    'Ancient': '#8B4513',
    'Medieval': '#2E86C1',
    'Early Modern': '#27AE60',
    'Modern': '#E74C3C',
    'Contemporary': '#8E44AD',
}

# For each region, assign individual reign durations to eras based on approximate timing
# We'll use the region's era range and distribute monarchs proportionally
# More precise: assign based on estimated start year of each reign

def assign_to_eras_proportional(region_name, info, durations):
    """Assign durations to eras based on region's time range."""
    era_start, era_end = info['era']
    n = len(durations)
    total_years = era_end - era_start
    if total_years <= 0:
        total_years = 1
    
    # Estimate each monarch's approximate start year
    cumulative = 0
    assignments = {}
    for era_name, (e_start, e_end) in ERAS.items():
        assignments[era_name] = []
    
    for i, dur in enumerate(durations):
        # Approximate start year of this reign
        start_year = era_start + (cumulative / max(sum(durations), 1)) * total_years
        # Assign to era
        for era_name, (e_start, e_end) in ERAS.items():
            if e_start <= start_year < e_end:
                if dur > 0:
                    assignments[era_name].append(dur)
                break
        else:
            # If before Ancient or after Contemporary, assign to nearest
            if start_year < -5000:
                if dur > 0:
                    assignments['Ancient'].append(dur)
            else:
                if dur > 0:
                    assignments['Contemporary'].append(dur)
        cumulative += dur
    
    return assignments


era_data = {era: [] for era in ERAS}
era_regions = {era: [] for era in ERAS}

for name, info in REGIONS.items():
    durs = [d for d in info['durations'] if d > 0]
    assignments = assign_to_eras_proportional(name, info, durs)
    for era_name, era_durs in assignments.items():
        if era_durs:
            era_data[era_name].extend(era_durs)
            era_regions[era_name].append(name)

print("\nEra-based pooled Weibull fits:")
era_fits = {}
for era_name in ERAS:
    durs = np.array(era_data[era_name], dtype=float)
    if len(durs) >= 5:
        fit = fit_region(durs)
        if fit:
            era_fits[era_name] = fit
            unique_regions = len(set(era_regions[era_name]))
            print(f"  {era_name:15s}  N={fit['n']:4d}  k={fit['k']:.3f}  "
                  f"CI=[{fit['k_ci_low']:.2f}-{fit['k_ci_high']:.2f}]  "
                  f"lambda={fit['lambda']:.1f}y  mean={fit['mean_reign']:.1f}y  "
                  f"KS p={fit['ks_p']:.3f}  R2={fit['r2']:.3f}  "
                  f"(from {unique_regions} regions)")
    else:
        print(f"  {era_name:15s}  N={len(durs):4d}  INSUFFICIENT DATA")

# Also fit individual regions within each era (where N>=5)
print("\nIndividual region fits by era (N>=5 only):")
era_region_fits = {era: {} for era in ERAS}
for name, info in REGIONS.items():
    durs = [d for d in info['durations'] if d > 0]
    assignments = assign_to_eras_proportional(name, info, durs)
    for era_name, era_durs in assignments.items():
        if len(era_durs) >= 5:
            fit = fit_region(np.array(era_durs, dtype=float))
            if fit:
                era_region_fits[era_name][name] = fit
                print(f"  {era_name:15s} | {name:30s}  N={fit['n']:3d}  k={fit['k']:.3f}")

# Sensitivity: Modern+Contemporary combined
print("\n  Sensitivity: Modern+Contemporary combined:")
modern_combined = era_data['Modern'] + era_data['Contemporary']
if len(modern_combined) >= 5:
    mc_fit = fit_region(np.array(modern_combined, dtype=float))
    if mc_fit:
        print(f"    Modern+Contemporary  N={mc_fit['n']}  k={mc_fit['k']:.3f}  "
              f"CI=[{mc_fit['k_ci_low']:.2f}-{mc_fit['k_ci_high']:.2f}]")


# =============================================================================
# FIGURE 1: WORLD MAP - MAIN ANALYSIS
# =============================================================================

print("\n--- Creating world map ---")

try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    HAS_CARTOPY = True
except ImportError:
    HAS_CARTOPY = False
    print("  Cartopy not available, using scatter-based map")

region_colors_map = {
    'Europe': '#2E86C1',
    'Asia': '#E74C3C',
    'Middle East': '#F39C12',
    'Africa': '#27AE60',
    'Africa/Middle East': '#D4AC0D',
    'Americas': '#8E44AD',
}

if HAS_CARTOPY:
    fig_map = plt.figure(figsize=(20, 12))
    ax_map = fig_map.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax_map.set_global()
    ax_map.add_feature(cfeature.LAND, facecolor='#f0f0f0', edgecolor='#cccccc', linewidth=0.5)
    ax_map.add_feature(cfeature.OCEAN, facecolor='#e6f2ff')
    ax_map.add_feature(cfeature.COASTLINE, linewidth=0.5, color='#999999')
    ax_map.add_feature(cfeature.BORDERS, linewidth=0.3, color='#cccccc')
    ax_map.set_title('Global Weibull Analysis: Shape Parameter k by Region\n'
                     'Bubble size = sample size N | Color intensity = k value',
                     fontsize=14, fontweight='bold', pad=20)
    
    # Colormap for k values
    import matplotlib.cm as cm
    from matplotlib.colors import Normalize
    k_vals_all = [r['k'] for r in results.values()]
    norm = Normalize(vmin=min(k_vals_all) - 0.1, vmax=max(k_vals_all) + 0.1)
    cmap = cm.RdYlGn  # Red=low k (chaotic), Green=high k (stable)
    
    # Small offsets for overlapping regions
    offsets = {
        'China (Qing)': (5, 5),
        'China (Ming)': (-5, -5),
        'Byzantine Empire': (3, 3),
        'Papacy (post-1000)': (-3, -3),
        'Korea (Goryeo)': (-3, 3),
    }
    
    for name, fit in results.items():
        lat, lon = fit['coords']
        off = offsets.get(name, (0, 0))
        lat += off[0]
        lon += off[1]
        
        color = cmap(norm(fit['k']))
        size = fit['n'] * 2 + 30
        
        ax_map.scatter(lon, lat, s=size, c=[color], alpha=0.8,
                      edgecolors='black', linewidth=0.8, zorder=5,
                      transform=ccrs.PlateCarree())
        
        # Label
        ax_map.text(lon + 2, lat + 2, f"{name}\nk={fit['k']:.2f}",
                   fontsize=6, transform=ccrs.PlateCarree(),
                   ha='left', va='bottom',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, linewidth=0.3))
    
    # Colorbar
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax_map, orientation='horizontal', pad=0.05, shrink=0.6, aspect=30)
    cbar.set_label('Weibull Shape Parameter k\n(low = chaotic/coup-prone | high = stable/orderly)',
                   fontsize=10)
    
    # Legend for region categories
    legend_elements = [Patch(facecolor=c, label=r, edgecolor='black', linewidth=0.5) 
                       for r, c in region_colors_map.items()]
    ax_map.legend(handles=legend_elements, loc='lower left', fontsize=8, title='Region Category')
    
    plt.savefig('/home/ubuntu/monarch_worldmap_main.png', dpi=150, bbox_inches='tight')
    print("Saved: monarch_worldmap_main.png")
    plt.close()

    # --- World map for sub-analysis 1: Elective vs Hereditary ---
    fig_map2, axes_map2 = plt.subplots(1, 2, figsize=(24, 10),
                                        subplot_kw={'projection': ccrs.Robinson()})
    
    for idx, (sel_type, sel_label, ax) in enumerate([
        ('elective', 'Elective/Selection-based', axes_map2[0]),
        ('hereditary', 'Hereditary', axes_map2[1])
    ]):
        ax.set_global()
        ax.add_feature(cfeature.LAND, facecolor='#f0f0f0', edgecolor='#cccccc', linewidth=0.5)
        ax.add_feature(cfeature.OCEAN, facecolor='#e6f2ff')
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5, color='#999999')
        ax.add_feature(cfeature.BORDERS, linewidth=0.3, color='#cccccc')
        
        sel_results = {n: r for n, r in results.items() if r['selection'] == sel_type}
        k_vals_sel = [r['k'] for r in sel_results.values()]
        
        for name, fit in sel_results.items():
            lat, lon = fit['coords']
            off = offsets.get(name, (0, 0))
            lat += off[0]; lon += off[1]
            color = cmap(norm(fit['k']))
            size = fit['n'] * 2 + 30
            ax.scatter(lon, lat, s=size, c=[color], alpha=0.8,
                      edgecolors='black', linewidth=0.8, zorder=5,
                      transform=ccrs.PlateCarree())
            ax.text(lon + 2, lat + 2, f"{name}\nk={fit['k']:.2f}",
                   fontsize=6, transform=ccrs.PlateCarree(), ha='left', va='bottom',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, linewidth=0.3))
        
        pooled_fit = elective_fit if sel_type == 'elective' else hereditary_fit
        ax.set_title(f'{sel_label}\n(N={len(sel_results)} regions, '
                     f'pooled k={pooled_fit["k"]:.3f}, mean reign={pooled_fit["mean_reign"]:.1f}y)',
                     fontsize=11, fontweight='bold')
    
    fig_map2.suptitle('Sub-analysis 1: Elective vs Hereditary Succession\n'
                      'World Map of Weibull Shape Parameter k',
                      fontsize=14, fontweight='bold')
    
    sm2 = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm2.set_array([])
    cbar2 = fig_map2.colorbar(sm2, ax=axes_map2, orientation='horizontal', 
                               pad=0.08, shrink=0.5, aspect=30)
    cbar2.set_label('Weibull Shape Parameter k', fontsize=10)
    
    plt.savefig('/home/ubuntu/monarch_worldmap_subanalysis1.png', dpi=150, bbox_inches='tight')
    print("Saved: monarch_worldmap_subanalysis1.png")
    plt.close()

else:
    print("  Skipping cartopy maps - using matplotlib scatter fallback")
    # Simple scatter plot as fallback
    fig_map, ax_map = plt.subplots(1, 1, figsize=(18, 10))
    for name, fit in results.items():
        lat, lon = fit['coords']
        color = region_colors_map.get(fit['region_category'], '#95A5A6')
        size = fit['n'] * 3 + 30
        ax_map.scatter(lon, lat, s=size, c=color, alpha=0.7,
                      edgecolors='black', linewidth=0.5)
        ax_map.annotate(f"{name}\nk={fit['k']:.2f}", (lon, lat),
                       fontsize=6, ha='left', xytext=(5, 5), textcoords='offset points')
    ax_map.set_xlabel('Longitude')
    ax_map.set_ylabel('Latitude')
    ax_map.set_title('Global Weibull Analysis: Shape Parameter k by Region', fontsize=14, fontweight='bold')
    ax_map.grid(True, alpha=0.3)
    plt.savefig('/home/ubuntu/monarch_worldmap_main.png', dpi=150, bbox_inches='tight')
    print("Saved: monarch_worldmap_main.png (scatter fallback)")
    plt.close()


# =============================================================================
# FIGURE 2: SUB-ANALYSIS 1 - BOX PLOTS + BAR CHARTS (Elective vs Hereditary)
# =============================================================================

print("--- Creating sub-analysis 1 figures ---")

fig_sub1, axes_sub1 = plt.subplots(2, 2, figsize=(20, 16))
fig_sub1.suptitle('Sub-analysis 1: Elective vs Hereditary Succession\n'
                  'Weibull Shape Parameter k Comparison',
                  fontsize=14, fontweight='bold')

# Panel 1: Bar chart - k values by selection type
ax = axes_sub1[0, 0]
elective_sorted = sorted(elective_regions.items(), key=lambda x: x[1]['k'])
hereditary_sorted = sorted(hereditary_regions.items(), key=lambda x: x[1]['k'])

all_sorted = []
for n, r in elective_sorted:
    all_sorted.append((n, r, 'elective'))
for n, r in hereditary_sorted:
    all_sorted.append((n, r, 'hereditary'))
all_sorted.sort(key=lambda x: x[1]['k'])

y_pos = np.arange(len(all_sorted))
colors_bar = ['#E74C3C' if s == 'elective' else '#2E86C1' for _, _, s in all_sorted]
k_vals_bar = [r['k'] for _, r, _ in all_sorted]
names_bar = [n for n, _, _ in all_sorted]

ax.barh(y_pos, k_vals_bar, color=colors_bar, alpha=0.8, height=0.7, edgecolor='white')
for i, (n, r, s) in enumerate(all_sorted):
    ax.text(r['k'] + 0.03, i, f"k={r['k']:.2f} N={r['n']}", va='center', fontsize=7)
ax.set_yticks(y_pos)
ax.set_yticklabels(names_bar, fontsize=8)
ax.axvline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel('Weibull Shape Parameter k')
ax.set_title('k by Region (colored by succession type)')
ax.legend(handles=[Patch(facecolor='#E74C3C', label='Elective'),
                   Patch(facecolor='#2E86C1', label='Hereditary')],
          fontsize=9, loc='lower right')

# Panel 2: Box plot comparison
ax = axes_sub1[0, 1]
elective_k = [r['k'] for r in elective_regions.values()]
hereditary_k = [r['k'] for r in hereditary_regions.values()]

bp = ax.boxplot([elective_k, hereditary_k], labels=['Elective\n(N_regions={})'.format(len(elective_k)),
                                                      'Hereditary\n(N_regions={})'.format(len(hereditary_k))],
                patch_artist=True, widths=0.5)
bp['boxes'][0].set_facecolor('#E74C3C')
bp['boxes'][0].set_alpha(0.6)
bp['boxes'][1].set_facecolor('#2E86C1')
bp['boxes'][1].set_alpha(0.6)

# Overlay individual points
for i, (data, color) in enumerate([(elective_k, '#E74C3C'), (hereditary_k, '#2E86C1')]):
    x = np.random.normal(i + 1, 0.04, size=len(data))
    ax.scatter(x, data, c=color, alpha=0.7, s=50, edgecolors='black', linewidth=0.5, zorder=5)

ax.axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='k=1')
ax.set_ylabel('Weibull Shape Parameter k')
ax.set_title('Distribution of k: Elective vs Hereditary')
ax.grid(axis='y', alpha=0.3)

# Panel 3: Pooled survival curves
ax = axes_sub1[1, 0]
x = np.linspace(0.1, 80, 500)

S_e = np.exp(-(x / elective_fit['lambda']) ** elective_fit['k'])
S_h = np.exp(-(x / hereditary_fit['lambda']) ** hereditary_fit['k'])

ax.plot(x, S_e, linewidth=3, color='#E74C3C', label=f"Elective (k={elective_fit['k']:.3f}, N={elective_fit['n']})")
ax.plot(x, S_h, linewidth=3, color='#2E86C1', label=f"Hereditary (k={hereditary_fit['k']:.3f}, N={hereditary_fit['n']})")

# Empirical survival
for durs, color, label in [(elective_durs, '#E74C3C', 'Elective (empirical)'),
                            (hereditary_durs, '#2E86C1', 'Hereditary (empirical)')]:
    sorted_d = np.sort(durs)
    S_emp = 1 - np.arange(1, len(sorted_d) + 1) / len(sorted_d)
    ax.step(sorted_d, S_emp, color=color, alpha=0.3, linewidth=1, linestyle='--')

ax.set_xlabel('Reign Duration (years)')
ax.set_ylabel('Survival Probability')
ax.set_title('Pooled Survival Curves: Elective vs Hereditary')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 80)

# Panel 4: Hazard functions
ax = axes_sub1[1, 1]
h_e = (elective_fit['k'] / elective_fit['lambda']) * (x / elective_fit['lambda']) ** (elective_fit['k'] - 1)
h_h = (hereditary_fit['k'] / hereditary_fit['lambda']) * (x / hereditary_fit['lambda']) ** (hereditary_fit['k'] - 1)

ax.plot(x, h_e, linewidth=3, color='#E74C3C', label=f"Elective (k={elective_fit['k']:.3f})")
ax.plot(x, h_h, linewidth=3, color='#2E86C1', label=f"Hereditary (k={hereditary_fit['k']:.3f})")

ax.set_xlabel('Reign Duration (years)')
ax.set_ylabel('Hazard Rate h(t)')
ax.set_title('Hazard Functions: Elective vs Hereditary')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 60)
ax.set_ylim(0, min(0.3, max(max(h_e[:400]), max(h_h[:400])) * 1.2))

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig('/home/ubuntu/monarch_sub1_elective_hereditary.png', dpi=150, bbox_inches='tight')
print("Saved: monarch_sub1_elective_hereditary.png")
plt.close()


# =============================================================================
# FIGURE 3: SUB-ANALYSIS 2 - ERA-BASED
# =============================================================================

print("--- Creating sub-analysis 2 figures ---")

fig_sub2 = plt.figure(figsize=(24, 20))
gs = gridspec.GridSpec(3, 2, figure=fig_sub2, hspace=0.35, wspace=0.3)
fig_sub2.suptitle('Sub-analysis 2: Weibull Shape Parameter k by Historical Era\n'
                  '(Ancient ~476 | Medieval 476-1453 | Early Modern 1453-1789 | Modern 1789-1945 | Contemporary 1945~)',
                  fontsize=14, fontweight='bold')

# Panel 1: Timeline bubble chart
ax1 = fig_sub2.add_subplot(gs[0, :])
era_midpoints = {
    'Ancient': -750, 'Medieval': 960, 'Early Modern': 1620,
    'Modern': 1867, 'Contemporary': 1985
}
for era_name, fit in era_fits.items():
    mid = era_midpoints[era_name]
    color = ERA_COLORS[era_name]
    ax1.scatter(mid, fit['k'], s=fit['n'] * 3 + 50, c=color, alpha=0.8,
               edgecolors='black', linewidth=1, zorder=5)
    ax1.annotate(f"{era_name}\nk={fit['k']:.3f}\nN={fit['n']}",
                (mid, fit['k']), fontsize=9, ha='center', va='bottom',
                xytext=(0, 15), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.3))
    # CI whiskers
    if not np.isnan(fit['k_ci_low']):
        ax1.plot([mid, mid], [fit['k_ci_low'], fit['k_ci_high']],
                color=color, linewidth=2, alpha=0.5)

ax1.axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax1.set_xlabel('Approximate Era Midpoint (year)', fontsize=11)
ax1.set_ylabel('Weibull Shape Parameter k', fontsize=11)
ax1.set_title('Timeline: k Parameter by Era (bubble size = N)', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Add era boundaries
for year, label in [(476, '476\nFall of Rome'), (1453, '1453\nFall of\nConstantinople'),
                     (1789, '1789\nFrench\nRevolution'), (1945, '1945\nEnd of\nWWII')]:
    ax1.axvline(year, color='gray', linestyle=':', linewidth=0.8, alpha=0.5)
    ax1.text(year, ax1.get_ylim()[0] + 0.02, label, fontsize=7, ha='center', va='bottom', color='gray')

# Panel 2: Box plot by era
ax2 = fig_sub2.add_subplot(gs[1, 0])
era_k_data = []
era_labels = []
era_colors_list = []
for era_name in ERAS:
    if era_name in era_region_fits and era_region_fits[era_name]:
        k_vals = [r['k'] for r in era_region_fits[era_name].values()]
        era_k_data.append(k_vals)
        era_labels.append(f"{era_name}\n(N_reg={len(k_vals)})")
        era_colors_list.append(ERA_COLORS[era_name])
    elif era_name in era_fits:
        # Only pooled fit available
        era_k_data.append([era_fits[era_name]['k']])
        era_labels.append(f"{era_name}\n(pooled)")
        era_colors_list.append(ERA_COLORS[era_name])

if era_k_data:
    bp2 = ax2.boxplot(era_k_data, labels=era_labels, patch_artist=True, widths=0.5)
    for patch, color in zip(bp2['boxes'], era_colors_list):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
    # Overlay points
    for i, (data, color) in enumerate(zip(era_k_data, era_colors_list)):
        x = np.random.normal(i + 1, 0.04, size=len(data))
        ax2.scatter(x, data, c=color, alpha=0.8, s=40, edgecolors='black', linewidth=0.5, zorder=5)
    ax2.axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax2.set_ylabel('Weibull Shape Parameter k')
    ax2.set_title('Distribution of k by Era\n(individual region fits)', fontsize=11, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)

# Panel 3: Pooled survival curves by era
ax3 = fig_sub2.add_subplot(gs[1, 1])
x = np.linspace(0.1, 80, 500)
for era_name, fit in era_fits.items():
    S = np.exp(-(x / fit['lambda']) ** fit['k'])
    color = ERA_COLORS[era_name]
    ax3.plot(x, S, linewidth=2.5, color=color,
            label=f"{era_name} (k={fit['k']:.3f}, N={fit['n']})")
ax3.set_xlabel('Reign Duration (years)')
ax3.set_ylabel('Survival Probability')
ax3.set_title('Pooled Survival Curves by Era', fontsize=11, fontweight='bold')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(0, 80)

# Panel 4: Ridge plot (Joy plot) - reign duration distributions by era
ax4 = fig_sub2.add_subplot(gs[2, 0])
era_names_order = ['Ancient', 'Medieval', 'Early Modern', 'Modern', 'Contemporary']
y_offset = 0
y_ticks = []
y_labels = []
for i, era_name in enumerate(era_names_order):
    if era_name in era_fits and era_data[era_name]:
        durs = np.array(era_data[era_name], dtype=float)
        durs = durs[durs > 0]
        if len(durs) < 3:
            continue
        
        # KDE
        try:
            from scipy.stats import gaussian_kde
            kde = gaussian_kde(durs, bw_method=0.3)
            x_kde = np.linspace(0, 80, 300)
            density = kde(x_kde)
            density = density / density.max() * 0.8  # normalize height
            
            color = ERA_COLORS[era_name]
            ax4.fill_between(x_kde, y_offset, y_offset + density, alpha=0.5, color=color)
            ax4.plot(x_kde, y_offset + density, color=color, linewidth=1.5)
            ax4.axhline(y_offset, color='gray', linewidth=0.3, alpha=0.3)
            
            y_ticks.append(y_offset + 0.2)
            y_labels.append(f"{era_name} (N={len(durs)})")
            y_offset += 1.0
        except:
            pass

ax4.set_yticks(y_ticks)
ax4.set_yticklabels(y_labels)
ax4.set_xlabel('Reign Duration (years)')
ax4.set_title('Ridge Plot: Reign Duration Distributions by Era', fontsize=11, fontweight='bold')
ax4.set_xlim(0, 80)

# Panel 5: Hazard functions by era
ax5 = fig_sub2.add_subplot(gs[2, 1])
x = np.linspace(0.5, 60, 500)
for era_name, fit in era_fits.items():
    k, lam = fit['k'], fit['lambda']
    h = (k / lam) * (x / lam) ** (k - 1)
    color = ERA_COLORS[era_name]
    ax5.plot(x, h, linewidth=2.5, color=color,
            label=f"{era_name} (k={k:.3f})")
ax5.set_xlabel('Reign Duration (years)')
ax5.set_ylabel('Hazard Rate h(t)')
ax5.set_title('Hazard Functions by Era', fontsize=11, fontweight='bold')
ax5.legend(fontsize=8)
ax5.grid(True, alpha=0.3)
ax5.set_xlim(0, 60)
ax5.set_ylim(0, 0.3)

plt.savefig('/home/ubuntu/monarch_sub2_era.png', dpi=150, bbox_inches='tight')
print("Saved: monarch_sub2_era.png")
plt.close()


# =============================================================================
# FIGURE 4: MAIN ANALYSIS BOX PLOTS (by region category)
# =============================================================================

print("--- Creating main analysis box plots ---")

fig_box, axes_box = plt.subplots(1, 3, figsize=(22, 8))
fig_box.suptitle('Box Plot Comparisons of Weibull Shape Parameter k',
                 fontsize=14, fontweight='bold')

# Panel 1: By region category
ax = axes_box[0]
cat_data = {}
for name, r in results.items():
    cat = r['region_category']
    if cat not in cat_data:
        cat_data[cat] = []
    cat_data[cat].append(r['k'])

cat_names = sorted(cat_data.keys())
cat_k_lists = [cat_data[c] for c in cat_names]
cat_colors = [region_colors_map.get(c, '#95A5A6') for c in cat_names]

bp3 = ax.boxplot(cat_k_lists, labels=[f"{c}\n(n={len(d)})" for c, d in zip(cat_names, cat_k_lists)],
                 patch_artist=True, widths=0.5)
for patch, color in zip(bp3['boxes'], cat_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.5)
for i, (data, color) in enumerate(zip(cat_k_lists, cat_colors)):
    x = np.random.normal(i + 1, 0.04, size=len(data))
    ax.scatter(x, data, c=color, alpha=0.8, s=50, edgecolors='black', linewidth=0.5, zorder=5)
ax.axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_ylabel('Weibull Shape Parameter k')
ax.set_title('By Geographic Region')
ax.grid(axis='y', alpha=0.3)

# Panel 2: Elective vs Hereditary
ax = axes_box[1]
bp4 = ax.boxplot([elective_k, hereditary_k],
                 labels=[f'Elective\n(n={len(elective_k)})', f'Hereditary\n(n={len(hereditary_k)})'],
                 patch_artist=True, widths=0.5)
bp4['boxes'][0].set_facecolor('#E74C3C'); bp4['boxes'][0].set_alpha(0.5)
bp4['boxes'][1].set_facecolor('#2E86C1'); bp4['boxes'][1].set_alpha(0.5)
for i, (data, color) in enumerate([(elective_k, '#E74C3C'), (hereditary_k, '#2E86C1')]):
    x = np.random.normal(i + 1, 0.04, size=len(data))
    ax.scatter(x, data, c=color, alpha=0.8, s=50, edgecolors='black', linewidth=0.5, zorder=5)
ax.axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_ylabel('Weibull Shape Parameter k')
ax.set_title('By Succession Type')
ax.grid(axis='y', alpha=0.3)

# Panel 3: By era (pooled k)
ax = axes_box[2]
era_k_pooled = []
era_pooled_labels = []
era_pooled_colors = []
for era_name in ['Ancient', 'Medieval', 'Early Modern', 'Modern', 'Contemporary']:
    if era_name in era_fits:
        era_k_pooled.append([era_fits[era_name]['k']])
        era_pooled_labels.append(era_name)
        era_pooled_colors.append(ERA_COLORS[era_name])
# Use individual region fits where available
era_k_ind = []
for era_name in ['Ancient', 'Medieval', 'Early Modern', 'Modern', 'Contemporary']:
    if era_name in era_region_fits and era_region_fits[era_name]:
        k_vals = [r['k'] for r in era_region_fits[era_name].values()]
        era_k_ind.append(k_vals)
    elif era_name in era_fits:
        era_k_ind.append([era_fits[era_name]['k']])
    else:
        continue

era_labels_final = []
era_colors_final = []
for era_name in ['Ancient', 'Medieval', 'Early Modern', 'Modern', 'Contemporary']:
    if era_name in era_region_fits and era_region_fits[era_name]:
        n = len(era_region_fits[era_name])
        era_labels_final.append(f"{era_name}\n(n={n})")
        era_colors_final.append(ERA_COLORS[era_name])
    elif era_name in era_fits:
        era_labels_final.append(f"{era_name}\n(pooled)")
        era_colors_final.append(ERA_COLORS[era_name])

if era_k_ind:
    bp5 = ax.boxplot(era_k_ind, labels=era_labels_final, patch_artist=True, widths=0.5)
    for patch, color in zip(bp5['boxes'], era_colors_final):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
    for i, (data, color) in enumerate(zip(era_k_ind, era_colors_final)):
        x = np.random.normal(i + 1, 0.04, size=len(data))
        ax.scatter(x, data, c=color, alpha=0.8, s=50, edgecolors='black', linewidth=0.5, zorder=5)
ax.axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_ylabel('Weibull Shape Parameter k')
ax.set_title('By Historical Era')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig('/home/ubuntu/monarch_boxplots.png', dpi=150, bbox_inches='tight')
print("Saved: monarch_boxplots.png")
plt.close()


# =============================================================================
# SUMMARY TABLES
# =============================================================================

print("\n" + "=" * 100)
print("  COMPLETE SUMMARY")
print("=" * 100)

print("\n--- Main Analysis (31 regions) ---")
print(f"{'Region':<30s} {'k':>6s} {'CI':>16s} {'N':>4s} {'Selection':>12s} {'Category':>15s}")
print("-" * 90)
for name, fit in sorted(results.items(), key=lambda x: x[1]['k']):
    ci = f"[{fit['k_ci_low']:.2f}-{fit['k_ci_high']:.2f}]" if not np.isnan(fit['k_ci_low']) else "N/A"
    print(f"{name:<30s} {fit['k']:>6.3f} {ci:>16s} {fit['n']:>4d} {fit['selection']:>12s} {fit['region_category']:>15s}")

print(f"\n--- Sub-analysis 1: Elective vs Hereditary ---")
print(f"  Elective (pooled):   k={elective_fit['k']:.3f}, N={elective_fit['n']}, mean={elective_fit['mean_reign']:.1f}y")
print(f"  Hereditary (pooled): k={hereditary_fit['k']:.3f}, N={hereditary_fit['n']}, mean={hereditary_fit['mean_reign']:.1f}y")
print(f"  KS 2-sample p={ks_p_sel:.4f}, Mann-Whitney p={u_p:.4f}")

print(f"\n--- Sub-analysis 2: By Era ---")
for era_name in ['Ancient', 'Medieval', 'Early Modern', 'Modern', 'Contemporary']:
    if era_name in era_fits:
        f = era_fits[era_name]
        ci = f"[{f['k_ci_low']:.2f}-{f['k_ci_high']:.2f}]" if not np.isnan(f['k_ci_low']) else "N/A"
        print(f"  {era_name:15s}  k={f['k']:.3f} {ci:>16s}  N={f['n']:4d}  mean={f['mean_reign']:.1f}y  KS p={f['ks_p']:.3f}")

print("\nAll figures saved successfully.")
print("Files:")
print("  monarch_worldmap_main.png          - World map (main analysis)")
print("  monarch_worldmap_subanalysis1.png   - World map (elective vs hereditary)")
print("  monarch_sub1_elective_hereditary.png - Sub-analysis 1 detailed")
print("  monarch_sub2_era.png               - Sub-analysis 2 (era-based)")
print("  monarch_boxplots.png               - Box plot comparisons (all)")
