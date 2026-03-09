#!/usr/bin/env python3
"""
Histogram Generator - Genera istogrammi diversificati con immagini e JSON
"""

import os
import json
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.gridspec as gridspec
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

IMG_OUTPUT_DIR = "data/images/synthetic/histogram"
JSON_OUTPUT_DIR = "data/groundtruth/synthetic/histogram"
os.makedirs(IMG_OUTPUT_DIR, exist_ok=True)
os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# PALETTE & STYLE TEMPLATES
# ─────────────────────────────────────────────

STYLE_TEMPLATES = [
    {
        "name": "dark_neon",
        "bg_color": "#0d0d0d",
        "axes_bg": "#1a1a2e",
        "text_color": "#e0e0e0",
        "grid_color": "#2a2a4a",
        "palettes": [["#00f5ff", "#ff006e", "#fb5607", "#8338ec", "#3a86ff"]],
        "edge_color": "#ffffff22",
        "bar_alpha": 0.85,
    },
    {
        "name": "pastel_soft",
        "bg_color": "#fafafa",
        "axes_bg": "#ffffff",
        "text_color": "#333333",
        "grid_color": "#eeeeee",
        "palettes": [["#ffb3c1", "#a8dadc", "#b7e4c7", "#ffd166", "#c77dff"]],
        "edge_color": "#cccccc",
        "bar_alpha": 0.80,
    },
    {
        "name": "corporate_blue",
        "bg_color": "#f0f4f8",
        "axes_bg": "#ffffff",
        "text_color": "#1a2b4a",
        "grid_color": "#dce7f0",
        "palettes": [["#003f88", "#0077b6", "#00b4d8", "#48cae4", "#90e0ef"]],
        "edge_color": "#0077b6",
        "bar_alpha": 0.88,
    },
    {
        "name": "earthy_warm",
        "bg_color": "#fdf6ec",
        "axes_bg": "#fff9f0",
        "text_color": "#3d2c1e",
        "grid_color": "#ede0d0",
        "palettes": [["#6b4226", "#c97c3a", "#e8b86d", "#a3c4a8", "#5c7a5c"]],
        "edge_color": "#c97c3a",
        "bar_alpha": 0.85,
    },
    {
        "name": "high_contrast",
        "bg_color": "#ffffff",
        "axes_bg": "#f8f8f8",
        "text_color": "#000000",
        "grid_color": "#cccccc",
        "palettes": [["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"]],
        "edge_color": "#000000",
        "bar_alpha": 0.90,
    },
    {
        "name": "midnight_gradient",
        "bg_color": "#0b1120",
        "axes_bg": "#111827",
        "text_color": "#f9fafb",
        "grid_color": "#1f2937",
        "palettes": [["#34d399", "#60a5fa", "#f472b6", "#fbbf24", "#a78bfa"]],
        "edge_color": "#374151",
        "bar_alpha": 0.82,
    },
    {
        "name": "vintage_print",
        "bg_color": "#f2ead8",
        "axes_bg": "#f5edd5",
        "text_color": "#2d1b0e",
        "grid_color": "#d6c9a8",
        "palettes": [["#8b2500", "#c0501a", "#e07b39", "#5b8a6e", "#2e5944"]],
        "edge_color": "#8b2500",
        "bar_alpha": 0.85,
    },
    {
        "name": "neon_minimal",
        "bg_color": "#fefefe",
        "axes_bg": "#ffffff",
        "text_color": "#111111",
        "grid_color": "#f0f0f0",
        "palettes": [["#ff3366", "#00ccff", "#00ff99", "#ff9900", "#cc00ff"]],
        "edge_color": "#eeeeee",
        "bar_alpha": 0.75,
    },
]

# ─────────────────────────────────────────────
# DATA GENERATORS
# ─────────────────────────────────────────────

def gen_normal(n):
    mu, sigma = random.uniform(40, 160), random.uniform(5, 30)
    return np.random.normal(mu, sigma, n), f"Normal(μ={mu:.0f}, σ={sigma:.0f})"

def gen_bimodal(n):
    mu1, mu2 = random.uniform(30, 80), random.uniform(100, 170)
    s = random.uniform(8, 18)
    d = np.concatenate([np.random.normal(mu1, s, n//2), np.random.normal(mu2, s, n//2)])
    return d, f"Bimodale({mu1:.0f}/{mu2:.0f})"

def gen_skewed(n):
    a = random.choice([3, 5, 8, -3, -5])
    d = stats.skewnorm.rvs(a, loc=random.uniform(50, 120), scale=random.uniform(10, 25), size=n)
    label = "Asimmetrica destra" if a > 0 else "Asimmetrica sinistra"
    return d, label

def gen_uniform(n):
    lo, hi = random.uniform(0, 50), random.uniform(100, 200)
    return np.random.uniform(lo, hi, n), f"Uniforme[{lo:.0f},{hi:.0f}]"

def gen_exponential(n):
    scale = random.uniform(10, 40)
    return np.random.exponential(scale, n), f"Esponenziale(λ={1/scale:.3f})"

def gen_lognormal(n):
    mu, sigma = random.uniform(3, 5), random.uniform(0.3, 0.8)
    return np.random.lognormal(mu, sigma, n), f"LogNormale(μ={mu:.1f})"

def gen_multimodal(n):
    k = random.randint(3, 5)
    centers = sorted(random.sample(range(20, 200), k))
    parts = [np.random.normal(c, random.uniform(4, 12), n//k) for c in centers]
    return np.concatenate(parts), f"Multimodale({k} mode)"

def gen_categorical_counts():
    """Ritorna categorie e conteggi per bar-style histograms"""
    datasets = [
        ("Generi musicali", ["Rock", "Pop", "Jazz", "Classical", "Hip-Hop", "Electronic", "R&B"]),
        ("Fasce d'età", ["0-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61+"]),
        ("Voti esami", ["18", "19-20", "21-22", "23-24", "25-26", "27-28", "29-30", "30L"]),
        ("Lingue parlate", ["Italiano", "Inglese", "Spagnolo", "Francese", "Tedesco", "Arabo", "Cinese"]),
        ("Reparti azienda", ["IT", "HR", "Finance", "Sales", "Marketing", "Operations", "R&D"]),
        ("Mesi dell'anno", ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]),
        ("Pianeti", ["Mercurio", "Venere", "Terra", "Marte", "Giove", "Saturno", "Urano", "Nettuno"]),
        ("Tipi di errore", ["TypeError", "ValueError", "KeyError", "IndexError", "AttributeError", "RuntimeError"]),
    ]
    name, cats = random.choice(datasets)
    counts = [random.randint(5, 200) for _ in cats]
    return name, cats, counts

DATA_GENERATORS = [gen_normal, gen_bimodal, gen_skewed, gen_uniform,
                   gen_exponential, gen_lognormal, gen_multimodal]

# ─────────────────────────────────────────────
# CHART TYPES
# ─────────────────────────────────────────────

CHART_TYPES = [
    "standard_histogram",
    "stacked_histogram",
    "side_by_side_histogram",
    "kde_overlay",
    "cumulative_histogram",
    "horizontal_histogram",
    "step_histogram",
    "categorical_bar_histogram",
    "density_comparison",
]

# ─────────────────────────────────────────────
# PLOT FUNCTIONS
# ─────────────────────────────────────────────

def apply_style(fig, ax, style, title, xlabel, ylabel):
    fig.patch.set_facecolor(style["bg_color"])
    ax.set_facecolor(style["axes_bg"])
    ax.tick_params(colors=style["text_color"], labelsize=10)
    for spine in ax.spines.values():
        spine.set_edgecolor(style["grid_color"])
    ax.xaxis.label.set_color(style["text_color"])
    ax.yaxis.label.set_color(style["text_color"])
    ax.title.set_color(style["text_color"])
    ax.grid(True, color=style["grid_color"], linewidth=0.6, alpha=0.7, linestyle='--')
    ax.set_axisbelow(True)
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=14, color=style["text_color"])
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11)


def build_json(chart_title, x_label, y_label, categorical_axis, series_list):
    """
    series_list: list of (series_name, x_values, y_values)
    """
    data_points = []
    for series_name, xs, ys in series_list:
        for x, y in zip(xs, ys):
            data_points.append({
                "series_name": series_name,
                "x_value": float(round(x, 4)) if isinstance(x, float) else x,
                "y_value": float(round(y, 4)) if isinstance(y, float) else y,
            })
    return {
        "chart_title": chart_title,
        "x_axis_label": x_label,
        "y_axis_label": y_label,
        "categorical_axis": categorical_axis,
        "data_points": data_points,
    }


# ---- Individual chart builders ----

def plot_standard_histogram(style, idx):
    n = random.randint(200, 2000)
    bins = random.randint(10, 50)
    data, dist_label = random.choice(DATA_GENERATORS)(n)
    color = random.choice(style["palettes"][0])
    title = f"Istogramma – {dist_label}"
    xlabel = random.choice(["Valore", "Misura (cm)", "Punteggio", "Età (anni)", "Peso (kg)"])
    ylabel = random.choice(["Frequenza", "Conteggio", "Occorrenze"])

    fig, ax = plt.subplots(figsize=(10, 6))
    counts, edges, patches = ax.hist(data, bins=bins, color=color,
                                     edgecolor=style["edge_color"], alpha=style["bar_alpha"])
    apply_style(fig, ax, style, title, xlabel, ylabel)
    # optionally add mean line
    if random.random() > 0.5:
        ax.axvline(np.mean(data), color='white' if style["bg_color"] < '#888888' else 'black',
                   linestyle='--', linewidth=1.5, label=f"Media: {np.mean(data):.1f}")
        ax.legend(facecolor=style["axes_bg"], labelcolor=style["text_color"])

    # JSON: bin midpoints
    midpoints = [(edges[i] + edges[i+1]) / 2 for i in range(len(counts))]
    json_data = build_json(title, xlabel, ylabel, "x",
                           [("Main", midpoints, counts.tolist())])
    return fig, json_data


def plot_stacked_histogram(style, idx):
    n = random.randint(300, 1500)
    bins = random.randint(15, 40)
    k = random.randint(2, 4)
    colors = style["palettes"][0][:k]
    series_labels = random.sample(["Gruppo A", "Gruppo B", "Gruppo C", "Gruppo D",
                                   "2022", "2023", "2024", "Serie 1", "Serie 2", "Serie 3"], k)
    datas = []
    gen = random.choice(DATA_GENERATORS)
    for _ in range(k):
        d, _ = gen(n)
        datas.append(d)

    title = "Istogramma Impilato – Confronto Distribuzioni"
    xlabel = random.choice(["Intervallo", "Valore"])
    ylabel = "Frequenza Cumulata"

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.hist(datas, bins=bins, stacked=True, color=colors, alpha=style["bar_alpha"],
            edgecolor=style["edge_color"], label=series_labels)
    ax.legend(facecolor=style["axes_bg"], labelcolor=style["text_color"])
    apply_style(fig, ax, style, title, xlabel, ylabel)

    # JSON
    all_edges = np.histogram(datas[0], bins=bins)[1]
    midpoints = [(all_edges[i] + all_edges[i+1]) / 2 for i in range(len(all_edges)-1)]
    series_list = []
    for label, d in zip(series_labels, datas):
        counts, _ = np.histogram(d, bins=all_edges)
        series_list.append((label, midpoints, counts.tolist()))
    json_data = build_json(title, xlabel, ylabel, "x", series_list)
    return fig, json_data


def plot_side_by_side_histogram(style, idx):
    n = random.randint(300, 1200)
    bins = random.randint(12, 30)
    k = random.randint(2, 3)
    colors = style["palettes"][0][:k]
    series_labels = random.sample(["Maschi", "Femmine", "Under 30", "Over 30",
                                   "Urbano", "Rurale", "Nord", "Sud", "Est"], k)
    gen1, gen2 = random.sample(DATA_GENERATORS, 2)
    datas = []
    for i, g in enumerate([gen1, gen2] + ([random.choice(DATA_GENERATORS)] if k == 3 else [])):
        d, _ = g(n)
        datas.append(d)

    title = "Istogramma Affiancato"
    xlabel = "Valore"
    ylabel = "Densità" if random.random() > 0.5 else "Frequenza"
    density = ylabel == "Densità"

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.hist(datas, bins=bins, density=density, color=colors, alpha=style["bar_alpha"],
            edgecolor=style["edge_color"], label=series_labels)
    ax.legend(facecolor=style["axes_bg"], labelcolor=style["text_color"])
    apply_style(fig, ax, style, title, xlabel, ylabel)

    all_edges = np.histogram(datas[0], bins=bins)[1]
    midpoints = [(all_edges[i] + all_edges[i+1]) / 2 for i in range(len(all_edges)-1)]
    series_list = []
    for label, d in zip(series_labels, datas):
        counts, _ = np.histogram(d, bins=all_edges, density=density)
        series_list.append((label, midpoints, counts.tolist()))
    json_data = build_json(title, xlabel, ylabel, "x", series_list)
    return fig, json_data


def plot_kde_overlay(style, idx):
    n = random.randint(500, 2000)
    bins = random.randint(20, 50)
    data, dist_label = random.choice(DATA_GENERATORS)(n)
    color = random.choice(style["palettes"][0])
    kde_color = [c for c in style["palettes"][0] if c != color][0] if len(style["palettes"][0]) > 1 else "#ff0000"

    title = f"Istogramma con KDE – {dist_label}"
    xlabel = "Valore"
    ylabel = "Densità"

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data, bins=bins, density=True, color=color,
            edgecolor=style["edge_color"], alpha=style["bar_alpha"], label="Istogramma")
    kde = stats.gaussian_kde(data)
    x_range = np.linspace(data.min(), data.max(), 400)
    ax.plot(x_range, kde(x_range), color=kde_color, linewidth=2.5, label="KDE")
    ax.legend(facecolor=style["axes_bg"], labelcolor=style["text_color"])
    apply_style(fig, ax, style, title, xlabel, ylabel)

    counts, edges = np.histogram(data, bins=bins, density=True)
    midpoints = [(edges[i] + edges[i+1]) / 2 for i in range(len(counts))]
    kde_vals = kde(x_range).tolist()
    series_list = [
        ("Istogramma", midpoints, counts.tolist()),
        ("KDE", x_range.tolist()[::8], kde_vals[::8]),
    ]
    json_data = build_json(title, xlabel, ylabel, "x", series_list)
    return fig, json_data


def plot_cumulative_histogram(style, idx):
    n = random.randint(400, 1500)
    bins = random.randint(15, 40)
    data, dist_label = random.choice(DATA_GENERATORS)(n)
    color = random.choice(style["palettes"][0])

    title = f"Istogramma Cumulativo – {dist_label}"
    xlabel = "Valore"
    ylabel = "Frequenza Cumulata"

    fig, ax = plt.subplots(figsize=(10, 6))
    counts, edges, _ = ax.hist(data, bins=bins, cumulative=True, color=color,
                                edgecolor=style["edge_color"], alpha=style["bar_alpha"])
    apply_style(fig, ax, style, title, xlabel, ylabel)

    midpoints = [(edges[i] + edges[i+1]) / 2 for i in range(len(counts))]
    json_data = build_json(title, xlabel, ylabel, "x",
                           [("Cumulativo", midpoints, counts.tolist())])
    return fig, json_data


def plot_horizontal_histogram(style, idx):
    n = random.randint(300, 1200)
    bins = random.randint(10, 35)
    data, dist_label = random.choice(DATA_GENERATORS)(n)
    color = random.choice(style["palettes"][0])

    title = f"Istogramma Orizzontale – {dist_label}"
    ylabel = random.choice(["Intervallo", "Classe", "Valore"])
    xlabel = "Frequenza"

    fig, ax = plt.subplots(figsize=(10, 7))
    counts, edges, _ = ax.hist(data, bins=bins, orientation='horizontal',
                                color=color, edgecolor=style["edge_color"], alpha=style["bar_alpha"])
    apply_style(fig, ax, style, title, xlabel, ylabel)

    midpoints = [(edges[i] + edges[i+1]) / 2 for i in range(len(counts))]
    # In horizontal: x=counts, y=midpoints
    json_data = build_json(title, xlabel, ylabel, "y",
                           [("Main", counts.tolist(), midpoints)])
    return fig, json_data


def plot_step_histogram(style, idx):
    n = random.randint(400, 1800)
    bins = random.randint(15, 45)
    k = random.randint(2, 4)
    colors = style["palettes"][0][:k]
    labels = [f"Serie {chr(65+i)}" for i in range(k)]
    datas = [random.choice(DATA_GENERATORS)(n)[0] for _ in range(k)]

    title = "Step Histogram – Confronto Serie"
    xlabel = "Valore"
    ylabel = "Frequenza"

    fig, ax = plt.subplots(figsize=(11, 6))
    for d, c, lbl in zip(datas, colors, labels):
        ax.hist(d, bins=bins, histtype='step', color=c, linewidth=2.0, label=lbl)
    ax.legend(facecolor=style["axes_bg"], labelcolor=style["text_color"])
    apply_style(fig, ax, style, title, xlabel, ylabel)

    all_edges = np.histogram(datas[0], bins=bins)[1]
    midpoints = [(all_edges[i] + all_edges[i+1]) / 2 for i in range(len(all_edges)-1)]
    series_list = []
    for lbl, d in zip(labels, datas):
        counts, _ = np.histogram(d, bins=all_edges)
        series_list.append((lbl, midpoints, counts.tolist()))
    json_data = build_json(title, xlabel, ylabel, "x", series_list)
    return fig, json_data


def plot_categorical_bar_histogram(style, idx):
    name, cats, counts = gen_categorical_counts()
    colors = (style["palettes"][0] * 3)[:len(cats)]

    title = f"Distribuzione – {name}"
    xlabel = name
    ylabel = "Conteggio"

    # random orientation
    horizontal = random.random() > 0.5
    fig, ax = plt.subplots(figsize=(11, 6))
    x_pos = np.arange(len(cats))

    if horizontal:
        bars = ax.barh(x_pos, counts, color=colors, edgecolor=style["edge_color"],
                       alpha=style["bar_alpha"])
        ax.set_yticks(x_pos)
        ax.set_yticklabels(cats, color=style["text_color"])
        categorical_axis = "y"
        ax.set_xlabel(ylabel, fontsize=11)
        ax.set_ylabel(xlabel, fontsize=11)
        apply_style(fig, ax, style, title, ylabel, xlabel)
        json_data = build_json(title, ylabel, xlabel, "y",
                               [("Main", counts, cats)])
    else:
        bars = ax.bar(x_pos, counts, color=colors, edgecolor=style["edge_color"],
                      alpha=style["bar_alpha"])
        ax.set_xticks(x_pos)
        ax.set_xticklabels(cats, rotation=random.choice([0, 30, 45, 60]),
                           ha='right', color=style["text_color"])
        apply_style(fig, ax, style, title, xlabel, ylabel)
        json_data = build_json(title, xlabel, ylabel, "x",
                               [("Main", cats, counts)])
    return fig, json_data


def plot_frequency_polygon(style, idx):
    n = random.randint(400, 1800)
    bins = random.randint(15, 40)
    k = random.randint(2, 4)
    colors = style["palettes"][0][:k]
    labels = [f"Gruppo {chr(65+i)}" for i in range(k)]
    datas = [random.choice(DATA_GENERATORS)(n)[0] for _ in range(k)]

    title = "Poligono di Frequenza"
    xlabel = "Valore"
    ylabel = "Frequenza"

    fig, ax = plt.subplots(figsize=(11, 6))
    for d, c, lbl in zip(datas, colors, labels):
        counts, edges = np.histogram(d, bins=bins)
        midpoints = [(edges[i]+edges[i+1])/2 for i in range(len(counts))]
        ax.plot(midpoints, counts, color=c, linewidth=2.2, marker='o',
                markersize=4, label=lbl, alpha=style["bar_alpha"])
        ax.fill_between(midpoints, counts, alpha=0.15, color=c)
    ax.legend(facecolor=style["axes_bg"], labelcolor=style["text_color"])
    apply_style(fig, ax, style, title, xlabel, ylabel)

    all_edges = np.histogram(datas[0], bins=bins)[1]
    midpoints = [(all_edges[i]+all_edges[i+1])/2 for i in range(len(all_edges)-1)]
    series_list = []
    for lbl, d in zip(labels, datas):
        counts, _ = np.histogram(d, bins=all_edges)
        series_list.append((lbl, midpoints, counts.tolist()))
    json_data = build_json(title, xlabel, ylabel, "x", series_list)
    return fig, json_data


def plot_polar_histogram(style, idx):
    n_bins = random.randint(12, 36)
    n = random.randint(500, 2000)
    data = np.random.vonmises(random.uniform(0, np.pi),
                               random.uniform(0.5, 3.0), n)
    data = (data + np.pi) % (2 * np.pi)
    counts, bin_edges = np.histogram(data, bins=n_bins, range=(0, 2*np.pi))
    theta = (bin_edges[:-1] + bin_edges[1:]) / 2
    width = (2 * np.pi) / n_bins

    colors_list = plt.cm.hsv(np.linspace(0, 1, n_bins))

    title = "Istogramma Polare (Rosa dei Venti)"
    fig = plt.figure(figsize=(9, 9))
    fig.patch.set_facecolor(style["bg_color"])
    ax = fig.add_subplot(111, projection='polar')
    ax.set_facecolor(style["axes_bg"])
    bars_plot = ax.bar(theta, counts, width=width, bottom=0.0,
                       color=colors_list, alpha=style["bar_alpha"],
                       edgecolor=style["edge_color"])
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20, color=style["text_color"])
    ax.tick_params(colors=style["text_color"])
    ax.yaxis.label.set_color(style["text_color"])

    # degrees for JSON
    theta_deg = np.degrees(theta).tolist()
    json_data = build_json(title, "Angolo (°)", "Frequenza", None,
                           [("Main", theta_deg, counts.tolist())])
    return fig, json_data


def plot_2d_histogram(style, idx):
    n = random.randint(1000, 5000)
    gen1, gen2 = random.sample(DATA_GENERATORS[:5], 2)
    data1, lbl1 = gen1(n)
    data2, lbl2 = gen2(n)
    bins = random.randint(20, 50)

    # add some correlation
    rho = random.uniform(-0.7, 0.7)
    data2 = rho * (data1 - data1.mean()) / data1.std() * data2.std() + data2.mean() + \
            np.sqrt(1 - rho**2) * (data2 - data2.mean())

    title = f"Istogramma 2D (ρ≈{rho:.2f})"
    xlabel = lbl1
    ylabel = lbl2

    cmap = random.choice(['viridis', 'plasma', 'inferno', 'hot', 'YlOrRd', 'Blues',
                          'RdYlBu_r', 'coolwarm', 'magma'])
    fig, ax = plt.subplots(figsize=(10, 8))
    h = ax.hist2d(data1, data2, bins=bins, cmap=cmap)
    plt.colorbar(h[3], ax=ax, label="Conteggio")
    apply_style(fig, ax, style, title, xlabel, ylabel)

    # JSON: sampled scatter points
    sample_idx = np.random.choice(n, min(200, n), replace=False)
    xs = data1[sample_idx].tolist()
    ys = data2[sample_idx].tolist()
    json_data = build_json(title, xlabel, ylabel, None,
                           [("Main", xs, ys)])
    return fig, json_data


def plot_density_comparison(style, idx):
    n = random.randint(500, 2000)
    bins = random.randint(20, 45)
    k = random.randint(2, 4)
    colors = style["palettes"][0][:k]
    labels = [f"Campione {i+1}" for i in range(k)]
    datas = [random.choice(DATA_GENERATORS)(n)[0] for _ in range(k)]

    title = "Confronto Densità – Distribuzioni Multiple"
    xlabel = "Valore"
    ylabel = "Densità"

    fig, axes = plt.subplots(1, k, figsize=(5*k, 6), sharey=True)
    fig.patch.set_facecolor(style["bg_color"])
    if k == 1:
        axes = [axes]
    fig.suptitle(title, fontsize=14, fontweight='bold', color=style["text_color"], y=1.02)

    all_series = []
    for i, (ax, d, c, lbl) in enumerate(zip(axes, datas, colors, labels)):
        counts, edges, _ = ax.hist(d, bins=bins, density=True, color=c,
                                   edgecolor=style["edge_color"], alpha=style["bar_alpha"])
        kde = stats.gaussian_kde(d)
        xr = np.linspace(d.min(), d.max(), 300)
        ax.plot(xr, kde(xr), color='white' if style["bg_color"] < '#888888' else 'black',
                linewidth=2)
        ax.set_title(lbl, color=style["text_color"], fontsize=11)
        ax.set_facecolor(style["axes_bg"])
        ax.tick_params(colors=style["text_color"])
        ax.set_xlabel(xlabel, color=style["text_color"])
        if i == 0:
            ax.set_ylabel(ylabel, color=style["text_color"])
        ax.grid(True, color=style["grid_color"], linewidth=0.5, alpha=0.7)

        midpoints = [(edges[i2]+edges[i2+1])/2 for i2 in range(len(counts))]
        all_series.append((lbl, midpoints, counts.tolist()))

    plt.tight_layout()
    json_data = build_json(title, xlabel, ylabel, "x", all_series)
    return fig, json_data


CHART_BUILDERS = {
    "standard_histogram": plot_standard_histogram,
    "stacked_histogram": plot_stacked_histogram,
    "side_by_side_histogram": plot_side_by_side_histogram,
    "kde_overlay": plot_kde_overlay,
    "cumulative_histogram": plot_cumulative_histogram,
    "horizontal_histogram": plot_horizontal_histogram,
    "step_histogram": plot_step_histogram,
    "categorical_bar_histogram": plot_categorical_bar_histogram,
    "density_comparison": plot_density_comparison,
}

# ─────────────────────────────────────────────
# MAIN GENERATION LOOP
# ─────────────────────────────────────────────

def generate_histograms(num_charts):
    # Cycle through styles and chart types to maximize diversity
    styles_cycle = random.sample(STYLE_TEMPLATES, len(STYLE_TEMPLATES))
    chart_types_cycle = random.sample(CHART_TYPES, len(CHART_TYPES))

    generated = []
    for i in range(num_charts):
        style = styles_cycle[i % len(styles_cycle)]
        chart_type = chart_types_cycle[i % len(chart_types_cycle)]

        print(f"  [{i+1}/{num_charts}] Tipo: {chart_type:30s} | Stile: {style['name']}")

        try:
            builder = CHART_BUILDERS[chart_type]
            fig, json_data = builder(style, i)

            base_name = f"histogram_{i+1:03d}_{chart_type}_{style['name']}"
            img_path = os.path.join(IMG_OUTPUT_DIR, base_name + ".png")
            json_path = os.path.join(JSON_OUTPUT_DIR, base_name + ".json")

            fig.savefig(img_path, dpi=150, bbox_inches='tight',
                        facecolor=fig.get_facecolor())
            plt.close(fig)

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

            generated.append((img_path, json_path))
            print(f"       ✓ Salvato: {base_name}")

        except Exception as e:
            print(f"       ✗ Errore: {e}")

    return generated


def main():
    print("=" * 60)
    print("     GENERATORE DI ISTOGRAMMI DIVERSIFICATI")
    print("=" * 60)
    print(f"\nTipi di grafico disponibili: {len(CHART_TYPES)}")
    print(f"Template di stile disponibili: {len(STYLE_TEMPLATES)}")
    print(f"Generatori di dati disponibili: {len(DATA_GENERATORS)}\n")

    while True:
        try:
            raw = input("Quanti istogrammi vuoi generare? (1-100): ").strip()
            num = int(raw)
            if 1 <= num <= 100:
                break
            else:
                print("  Inserisci un numero tra 1 e 100.")
        except ValueError:
            print("  Input non valido. Inserisci un numero intero.")

    print(f"\nGenerazione di {num} istogrammi in corso...\n")
    results = generate_histograms(num)

    print(f"\n{'='*60}")
    print(f"  COMPLETATO! Generati {len(results)} grafici.")
    print(f"  Ogni grafico ha: 1 file PNG + 1 file JSON")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
