#!/usr/bin/env python3
"""
Bubble Chart Generator – v3.0
- 30% of charts have a categorical X or Y axis
- z_value is always numeric and shares the same range across ALL series
- High visual diversity across templates
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import numpy as np
import json, os, random
from datetime import datetime

IMG_OUTPUT_DIR  = "data/images/synthetic/bubble"
JSON_OUTPUT_DIR = "data/groundtruth/synthetic/bubble"
os.makedirs(IMG_OUTPUT_DIR,  exist_ok=True)
os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
#  NUMERIC TEMPLATES  (categorical_axis = None)
# ══════════════════════════════════════════════════════════════════════════════

NUMERIC_TEMPLATES = [
    {
        "name": "economic_comparison",
        "title": "GDP vs Life Expectancy by Country",
        "x_label": "GDP per Capita (USD)", "y_label": "Life Expectancy (years)",
        "categorical_axis": None,
        "style": "ggplot", "colormap": "RdYlGn", "bg_color": "#F7F7F7",
        "figsize": (13, 8), "alpha": 0.75, "edgecolor": "white", "linewidth": 1.2,
        "z_label": "Population (M)", "z_range": (1, 1500),
        "w_meaning": "HDI Index",
        "series": [
            {"name": "Africa",   "n": 8,  "x": (500, 8000),    "y": (45, 72)},
            {"name": "Asia",     "n": 9,  "x": (1000, 55000),  "y": (65, 85)},
            {"name": "Europe",   "n": 10, "x": (15000, 80000), "y": (75, 85)},
            {"name": "Americas", "n": 7,  "x": (3000, 65000),  "y": (68, 82)},
        ],
    },
    {
        "name": "tech_market",
        "title": "Tech Companies: Revenue vs R&D Spend",
        "x_label": "Annual Revenue (B$)", "y_label": "R&D Expenditure (B$)",
        "categorical_axis": None,
        "style": "dark_background", "colormap": "plasma", "bg_color": "#0D0D0D",
        "figsize": (13, 8), "alpha": 0.80, "edgecolor": "#FFFFFF", "linewidth": 0.6,
        "z_label": "Market Cap (B$)", "z_range": (10, 5000),
        "w_meaning": "Employees (K)",
        "series": [
            {"name": "Software",  "n": 7, "x": (5, 200),  "y": (1, 40)},
            {"name": "Hardware",  "n": 6, "x": (10, 300), "y": (2, 20)},
            {"name": "Cloud",     "n": 5, "x": (20, 400), "y": (5, 80)},
            {"name": "Semicon",   "n": 5, "x": (3, 100),  "y": (1, 15)},
        ],
    },
    {
        "name": "environmental",
        "title": "CO\u2082 Emissions vs Renewable Energy Share",
        "x_label": "Renewable Energy Share (%)", "y_label": "CO\u2082 Emissions per Capita (t)",
        "categorical_axis": None,
        "style": "seaborn-v0_8-whitegrid", "colormap": "YlOrRd", "bg_color": "#EAF4E8",
        "figsize": (13, 8), "alpha": 0.70, "edgecolor": "#336633", "linewidth": 1.0,
        "z_label": "Total Energy Use (TWh)", "z_range": (5, 2000),
        "w_meaning": "Coal Dependency (%)",
        "series": [
            {"name": "High Income", "n": 8, "x": (10, 80), "y": (3, 15)},
            {"name": "Mid Income",  "n": 9, "x": (5, 50),  "y": (2, 8)},
            {"name": "Low Income",  "n": 7, "x": (20, 90), "y": (0.2, 2)},
        ],
    },
    {
        "name": "social_media",
        "title": "Social Media: Followers vs Engagement Rate",
        "x_label": "Followers (Millions)", "y_label": "Engagement Rate (%)",
        "categorical_axis": None,
        "style": "seaborn-v0_8-pastel", "colormap": "cool", "bg_color": "#FDF6FF",
        "figsize": (12, 8), "alpha": 0.72, "edgecolor": "#AA00AA", "linewidth": 0.8,
        "z_label": "Avg Likes per Post (K)", "z_range": (0.5, 8000),
        "w_meaning": "Post Frequency / week",
        "series": [
            {"name": "Instagram", "n": 8, "x": (0.5, 250), "y": (0.5, 8)},
            {"name": "TikTok",    "n": 7, "x": (0.1, 150), "y": (2, 15)},
            {"name": "YouTube",   "n": 6, "x": (0.5, 100), "y": (1, 6)},
            {"name": "Twitter/X", "n": 6, "x": (0.1, 80),  "y": (0.1, 3)},
        ],
    },
    {
        "name": "sports_athletes",
        "title": "Athletes: Training Hours vs Performance Score",
        "x_label": "Weekly Training Hours", "y_label": "Season Performance Score",
        "categorical_axis": None,
        "style": "seaborn-v0_8-darkgrid", "colormap": "viridis", "bg_color": "#EEF2FF",
        "figsize": (13, 9), "alpha": 0.78, "edgecolor": "#FFFFFF", "linewidth": 0.8,
        "z_label": "Career Earnings (M$)", "z_range": (0.1, 500),
        "w_meaning": "Injury Rate (%)",
        "series": [
            {"name": "Football",  "n": 10, "x": (20, 40), "y": (60, 98)},
            {"name": "Swimming",  "n": 8,  "x": (25, 45), "y": (55, 95)},
            {"name": "Athletics", "n": 9,  "x": (15, 35), "y": (50, 99)},
            {"name": "Cycling",   "n": 7,  "x": (30, 50), "y": (65, 97)},
        ],
    },
    {
        "name": "startup_ecosystem",
        "title": "Startup Ecosystem: Funding vs Growth Rate",
        "x_label": "Total Funding (M$)", "y_label": "Annual Growth Rate (%)",
        "categorical_axis": None,
        "style": "bmh", "colormap": "Spectral", "bg_color": "#FFFDF0",
        "figsize": (14, 9), "alpha": 0.68, "edgecolor": "#333333", "linewidth": 0.7,
        "z_label": "Team Size", "z_range": (2, 300),
        "w_meaning": "Months to Profitability",
        "series": [
            {"name": "Fintech",    "n": 7, "x": (1, 500),   "y": (20, 400)},
            {"name": "HealthTech", "n": 6, "x": (0.5, 200), "y": (10, 300)},
            {"name": "EdTech",     "n": 6, "x": (0.5, 100), "y": (15, 250)},
            {"name": "CleanTech",  "n": 5, "x": (2, 300),   "y": (5, 200)},
            {"name": "AI/ML",      "n": 7, "x": (1, 800),   "y": (50, 600)},
        ],
    },
    {
        "name": "medical_research",
        "title": "Drug Trials: Efficacy vs Side Effect Profile",
        "x_label": "Efficacy Score (%)", "y_label": "Side Effect Severity Index",
        "categorical_axis": None,
        "style": "seaborn-v0_8-white", "colormap": "RdBu", "bg_color": "#F0F8FF",
        "figsize": (13, 8), "alpha": 0.73, "edgecolor": "#004488", "linewidth": 0.9,
        "z_label": "Trial Sample Size", "z_range": (20, 20000),
        "w_meaning": "Cost per Patient ($K)",
        "series": [
            {"name": "Phase I",   "n": 5, "x": (20, 60), "y": (1, 8)},
            {"name": "Phase II",  "n": 7, "x": (40, 80), "y": (0.5, 6)},
            {"name": "Phase III", "n": 6, "x": (60, 95), "y": (0.2, 4)},
            {"name": "Approved",  "n": 5, "x": (70, 98), "y": (0.1, 3)},
        ],
    },
    {
        "name": "energy_sources",
        "title": "Energy Sources: Capacity Factor vs Levelized Cost",
        "x_label": "Capacity Factor (%)", "y_label": "LCOE ($/MWh)",
        "categorical_axis": None,
        "style": "dark_background", "colormap": "rainbow", "bg_color": "#060610",
        "figsize": (13, 8), "alpha": 0.78, "edgecolor": "#AAAAAA", "linewidth": 0.6,
        "z_label": "Global Installed Capacity (GW)", "z_range": (20, 1500),
        "w_meaning": "CO2 Intensity (g/kWh)",
        "series": [
            {"name": "Solar PV",      "n": 6, "x": (10, 28), "y": (25, 75)},
            {"name": "Wind Onshore",  "n": 6, "x": (25, 45), "y": (20, 60)},
            {"name": "Wind Offshore", "n": 5, "x": (35, 55), "y": (50, 130)},
            {"name": "Nuclear",       "n": 4, "x": (80, 95), "y": (80, 180)},
            {"name": "Gas CCGT",      "n": 5, "x": (40, 65), "y": (40, 100)},
            {"name": "Hydro",         "n": 5, "x": (35, 60), "y": (20, 80)},
        ],
    },
    {
        "name": "real_estate",
        "title": "Real Estate: Price per m\u00b2 vs Rental Yield",
        "x_label": "Price per m\u00b2 (\u20ac)", "y_label": "Gross Rental Yield (%)",
        "categorical_axis": None,
        "style": "seaborn-v0_8-muted", "colormap": "copper", "bg_color": "#F5F0EB",
        "figsize": (13, 8), "alpha": 0.72, "edgecolor": "#663300", "linewidth": 0.9,
        "z_label": "Avg Property Size (m\u00b2)", "z_range": (35, 350),
        "w_meaning": "Vacancy Rate (%)",
        "series": [
            {"name": "City Centre", "n": 8, "x": (3000, 15000), "y": (2, 5.5)},
            {"name": "Suburbs",     "n": 9, "x": (1000, 5000),  "y": (3.5, 7)},
            {"name": "Rural",       "n": 7, "x": (400, 2000),   "y": (4, 9)},
            {"name": "Coastal",     "n": 6, "x": (2000, 12000), "y": (2.5, 6)},
        ],
    },
    {
        "name": "weather_stations",
        "title": "Weather Stations: Temperature vs Humidity",
        "x_label": "Average Temperature (\u00b0C)", "y_label": "Relative Humidity (%)",
        "categorical_axis": None,
        "style": "seaborn-v0_8-deep", "colormap": "coolwarm", "bg_color": "#EEF6FF",
        "figsize": (13, 8), "alpha": 0.70, "edgecolor": "none", "linewidth": 0,
        "z_label": "Annual Precipitation (mm)", "z_range": (100, 3000),
        "w_meaning": "Sunshine Hours / year",
        "series": [
            {"name": "Main", "n": 30, "x": (-10, 40), "y": (20, 95)},
        ],
    },
]

# ══════════════════════════════════════════════════════════════════════════════
#  CATEGORICAL TEMPLATES  (one axis is categorical)
# ══════════════════════════════════════════════════════════════════════════════

CATEGORICAL_TEMPLATES = [
    # ── CAT-X ─────────────────────────────────────────────────────────────────
    {
        "name": "industry_salary",
        "title": "Industry Salary vs Experience Level",
        "x_label": "Industry", "y_label": "Average Salary (K$)",
        "categorical_axis": "x",
        "style": "ggplot", "colormap": "tab10", "bg_color": "#F9F9F9",
        "figsize": (14, 8), "alpha": 0.75, "edgecolor": "#333333", "linewidth": 0.8,
        "z_label": "Job Openings (K)", "z_range": (1, 200),
        "w_meaning": "Remote Work %",
        "categories": ["Finance", "Tech", "Healthcare", "Education", "Retail", "Energy", "Media"],
        "series": [
            {"name": "Junior",  "y": (35, 65)},
            {"name": "Mid",     "y": (55, 95)},
            {"name": "Senior",  "y": (80, 160)},
            {"name": "Manager", "y": (100, 220)},
        ],
    },
    {
        "name": "country_happiness",
        "title": "Happiness Score by Region and Income",
        "x_label": "Region", "y_label": "World Happiness Score",
        "categorical_axis": "x",
        "style": "seaborn-v0_8-pastel", "colormap": "Set2", "bg_color": "#FAFFFE",
        "figsize": (14, 8), "alpha": 0.78, "edgecolor": "#555555", "linewidth": 0.7,
        "z_label": "GDP per Capita (K$)", "z_range": (1, 80),
        "w_meaning": "Social Support Index",
        "categories": ["W. Europe", "N. America", "E. Asia", "L. America", "M. East", "Africa", "S. Asia"],
        "series": [
            {"name": "Low Income",  "y": (3.5, 5.5)},
            {"name": "Mid Income",  "y": (4.5, 6.8)},
            {"name": "High Income", "y": (6.0, 8.0)},
        ],
    },
    {
        "name": "product_performance",
        "title": "Product Line: Revenue vs Margin by Category",
        "x_label": "Product Category", "y_label": "Gross Margin (%)",
        "categorical_axis": "x",
        "style": "bmh", "colormap": "Paired", "bg_color": "#FFFBF0",
        "figsize": (14, 8), "alpha": 0.72, "edgecolor": "#222222", "linewidth": 0.8,
        "z_label": "Revenue (M$)", "z_range": (5, 500),
        "w_meaning": "NPS Score",
        "categories": ["Electronics", "Apparel", "Food & Bev", "Home & Garden", "Sports", "Toys", "Automotive"],
        "series": [
            {"name": "Online",     "y": (15, 60)},
            {"name": "Wholesale",  "y": (8, 35)},
            {"name": "Retail",     "y": (10, 45)},
        ],
    },
    # ── CAT-Y ─────────────────────────────────────────────────────────────────
    {
        "name": "project_timeline",
        "title": "Project Phases: Duration vs Cost Overrun",
        "x_label": "Cost Overrun (%)", "y_label": "Project Phase",
        "categorical_axis": "y",
        "style": "seaborn-v0_8-whitegrid", "colormap": "RdYlGn_r", "bg_color": "#F4F8FF",
        "figsize": (13, 8), "alpha": 0.75, "edgecolor": "#003366", "linewidth": 0.8,
        "z_label": "Phase Duration (days)", "z_range": (10, 365),
        "w_meaning": "Risk Score",
        "categories": ["Initiation", "Planning", "Execution", "Monitoring", "Closure"],
        "series": [
            {"name": "IT Projects",           "x": (-5, 80)},
            {"name": "Construction Projects", "x": (0, 120)},
            {"name": "Research Projects",     "x": (-10, 60)},
        ],
    },
    {
        "name": "nutrient_by_food_group",
        "title": "Nutrient Profile by Food Group",
        "x_label": "Protein Content (g/100g)", "y_label": "Food Group",
        "categorical_axis": "y",
        "style": "seaborn-v0_8-colorblind", "colormap": "autumn", "bg_color": "#FFF8EE",
        "figsize": (13, 9), "alpha": 0.73, "edgecolor": "#884400", "linewidth": 0.8,
        "z_label": "Calories (kcal/100g)", "z_range": (10, 600),
        "w_meaning": "Fibre Content (g)",
        "categories": ["Dairy", "Meat & Fish", "Grains", "Legumes", "Vegetables", "Fruits", "Nuts & Seeds"],
        "series": [
            {"name": "Raw",       "x": (0, 40)},
            {"name": "Cooked",    "x": (0, 35)},
            {"name": "Processed", "x": (0, 30)},
        ],
    },
    {
        "name": "hospital_dept",
        "title": "Hospital Departments: Wait Time vs Patient Volume",
        "x_label": "Avg Wait Time (min)", "y_label": "Department",
        "categorical_axis": "y",
        "style": "seaborn-v0_8-white", "colormap": "Blues", "bg_color": "#EEF8FF",
        "figsize": (13, 8), "alpha": 0.75, "edgecolor": "#004488", "linewidth": 0.9,
        "z_label": "Daily Patient Volume", "z_range": (20, 500),
        "w_meaning": "Staff per Shift",
        "categories": ["Emergency", "Surgery", "Oncology", "Cardiology", "Pediatrics", "Radiology"],
        "series": [
            {"name": "Weekday", "x": (10, 180)},
            {"name": "Weekend", "x": (15, 240)},
            {"name": "Night",   "x": (5, 120)},
        ],
    },
]

# ══════════════════════════════════════════════════════════════════════════════
#  DATA GENERATION
# ══════════════════════════════════════════════════════════════════════════════

def build_data_points(template):
    z_lo, z_hi = template["z_range"]
    cat_axis   = template.get("categorical_axis")
    points     = []

    if cat_axis == "x":
        for s in template["series"]:
            for cat in template["categories"]:
                y = random.uniform(*s["y"])
                z = random.uniform(z_lo, z_hi)
                w = random.uniform(z_lo * 0.5, z_hi * 0.8)
                points.append({
                    "series_name": s["name"],
                    "x_value": cat,
                    "y_value": round(y, 4),
                    "z_value": round(z, 4),
                    "w_value": round(w, 4),
                })

    elif cat_axis == "y":
        for s in template["series"]:
            for cat in template["categories"]:
                x = random.uniform(*s["x"])
                z = random.uniform(z_lo, z_hi)
                w = random.uniform(z_lo * 0.5, z_hi * 0.8)
                points.append({
                    "series_name": s["name"],
                    "x_value": round(x, 4),
                    "y_value": cat,
                    "z_value": round(z, 4),
                    "w_value": round(w, 4),
                })

    else:
        for s in template["series"]:
            n  = s["n"]
            xs = np.random.uniform(*s["x"], n)
            ys = np.random.uniform(*s["y"], n)
            zs = np.random.uniform(z_lo, z_hi, n)
            ws = np.random.uniform(z_lo * 0.5, z_hi * 0.8, n)
            for x, y, z, w in zip(xs, ys, zs, ws):
                points.append({
                    "series_name": s["name"],
                    "x_value": round(float(x), 4),
                    "y_value": round(float(y), 4),
                    "z_value": round(float(z), 4),
                    "w_value": round(float(w), 4),
                })

    return points

# ══════════════════════════════════════════════════════════════════════════════
#  CHART RENDERING
# ══════════════════════════════════════════════════════════════════════════════

SERIES_COLORS = [
    "#E63946","#2196F3","#4CAF50","#FF9800","#9C27B0",
    "#00BCD4","#F44336","#8BC34A","#FF5722","#3F51B5",
]

def size_from_z(z_arr, z_range, s_min=50, s_max=1100):
    """Normalise z values against the template's shared range -> marker size."""
    lo, hi = z_range
    norm = (np.array(z_arr, dtype=float) - lo) / (hi - lo + 1e-9)
    return s_min + np.clip(norm, 0, 1) * (s_max - s_min)

def numeric_positions(points, cat_axis, categories=None):
    """Return (xs_num, ys_num) with jitter applied to categorical axis."""
    if cat_axis == "x":
        cat_pos = {c: i for i, c in enumerate(categories)}
        xs = np.array([cat_pos[p["x_value"]] + random.uniform(-0.18, 0.18) for p in points])
        ys = np.array([p["y_value"] for p in points])
    elif cat_axis == "y":
        cat_pos = {c: i for i, c in enumerate(categories)}
        xs = np.array([p["x_value"] for p in points])
        ys = np.array([cat_pos[p["y_value"]] + random.uniform(-0.18, 0.18) for p in points])
    else:
        xs = np.array([p["x_value"] for p in points])
        ys = np.array([p["y_value"] for p in points])
    return xs, ys

def _format_z(v):
    if v >= 1_000_000:  return f"{v/1_000_000:.1f}M"
    if v >= 1_000:      return f"{v/1_000:.1f}K"
    if v >= 100:        return f"{v:.0f}"
    if v >= 10:         return f"{v:.1f}"
    return f"{v:.2g}"


def _corner_density(xs_norm, ys_norm, cx, cy, radius=0.25):
    """Count normalised data points near a corner (cx,cy) within radius."""
    return int(np.sum((xs_norm - cx)**2 + (ys_norm - cy)**2 < radius**2))


def _best_series_legend_loc(xs_norm, ys_norm):
    """
    Pick the matplotlib legend loc string for the corner with fewest data pts.
    Considers only the four corners, avoids top-centre (title area).
    """
    candidates = [
        ("upper left",  0.0, 1.0),
        ("upper right", 1.0, 1.0),
        ("lower left",  0.0, 0.0),
        ("lower right", 1.0, 0.0),
    ]
    scores = [(loc, _corner_density(xs_norm, ys_norm, cx, cy))
              for loc, cx, cy in candidates]
    # sort by density ascending, then shuffle ties for variety
    scores.sort(key=lambda t: t[1])
    # pick randomly among the two least-dense corners
    top2 = scores[:2]
    random.shuffle(top2)
    return top2[0][0]


def _draw_size_legend(fig, ax, z_range, z_label, bg_color,
                      xs_norm, ys_norm, series_legend_loc):
    """
    Draw the bubble-size inset legend.

    Placement logic:
    - The inset lives in the figure's RIGHT margin (always outside the ax area)
      at one of three vertical bands: top / middle / bottom.
    - The vertical band is chosen as the one furthest from where the
      series-colour legend sits (upper/lower), so the two legends don't compete
      visually.
    - A small random jitter is added so repeated charts look different.
    """
    z_lo, z_hi = z_range
    fracs  = [0.0, 0.25, 0.65, 1.0]
    z_vals = [z_lo + f * (z_hi - z_lo) for f in fracs]
    s_vals = size_from_z(z_vals, z_range)

    dark      = bg_color.lower() < "#888888"
    txt_color = "#DDDDDD" if dark else "#333333"
    dot_color = "#BBBBBB" if dark else "#888888"
    border_c  = "#555555" if dark else "#CCCCCC"

    # ── choose vertical position ──────────────────────────────────────────────
    # If series legend is at "upper *", prefer the bottom band; else top band.
    # Then add a small random nudge (±0.04 in figure fraction).
    if "upper" in series_legend_loc:
        base_y = 0.04   # bottom band
    elif "lower" in series_legend_loc:
        base_y = 0.58   # top band
    else:
        base_y = 0.30   # middle fallback

    # jitter within ±0.06 while staying inside [0.02, 0.64]
    jitter_y = random.uniform(-0.06, 0.06)
    inset_y  = max(0.02, min(0.64, base_y + jitter_y))

    # fixed width / height in figure fraction
    iw, ih = 0.17, 0.32

    inset = fig.add_axes([0.80, inset_y, iw, ih])
    inset.set_facecolor(bg_color)
    inset.set_xlim(0, 1)
    n = len(z_vals)
    inset.set_ylim(-0.6, n - 0.4)
    inset.set_xticks([])
    inset.set_yticks([])
    for sp in inset.spines.values():
        sp.set_visible(True)
        sp.set_edgecolor(border_c)
        sp.set_linewidth(0.7)

    inset.set_title(z_label, fontsize=7, color=txt_color,
                    fontweight="bold", pad=4)

    for row, (zv, sz) in enumerate(zip(z_vals, s_vals)):
        inset.scatter([0.30], [row], s=sz * 0.50,
                      c=dot_color, alpha=0.80,
                      edgecolors=txt_color, linewidths=0.6,
                      zorder=3)
        inset.text(0.62, row, _format_z(zv),
                   va="center", ha="left",
                   fontsize=7.5, color=txt_color)


def _text_color(bg_color):
    """Return a readable foreground colour for the given hex bg_color."""
    c = bg_color.lstrip("#")
    r, g, b = int(c[0:2],16), int(c[2:4],16), int(c[4:6],16)
    luminance = (0.299*r + 0.587*g + 0.114*b) / 255
    return "#EEEEEE" if luminance < 0.45 else "#111111"


def _tick_color(bg_color):
    """Tick/spine colour: lighter contrast than full text."""
    c = bg_color.lstrip("#")
    r, g, b = int(c[0:2],16), int(c[2:4],16), int(c[4:6],16)
    luminance = (0.299*r + 0.587*g + 0.114*b) / 255
    return "#CCCCCC" if luminance < 0.45 else "#444444"


def _apply_label_visibility(ax, fig, bg_color):
    """
    Force all axis text (title, labels, ticks, spines) to be readable
    regardless of which matplotlib style was active.
    Called AFTER all plotting, so it always wins.
    """
    tc  = _text_color(bg_color)
    tkc = _tick_color(bg_color)

    ax.title.set_color(tc)
    ax.xaxis.label.set_color(tc)
    ax.yaxis.label.set_color(tc)
    ax.tick_params(colors=tkc, which="both")
    for spine in ax.spines.values():
        spine.set_edgecolor(tkc)
    # tick label colours
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_color(tc)


def render_chart(template, data_points, filename):
    try:
        plt.style.use(template["style"])
    except Exception:
        plt.style.use("default")

    fig, ax = plt.subplots(figsize=template["figsize"])
    bg = template["bg_color"]
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    cat_axis     = template.get("categorical_axis")
    series_names = list(dict.fromkeys(p["series_name"] for p in data_points))
    single       = len(series_names) == 1
    z_range      = template["z_range"]
    z_label      = template["z_label"]
    categories   = template.get("categories")

    # ── collect ALL numeric positions for density analysis ────────────────────
    all_xs, all_ys = numeric_positions(data_points, cat_axis, categories)

    def _norm(arr):
        lo, hi = arr.min(), arr.max()
        return (arr - lo) / (hi - lo + 1e-9) if hi > lo else np.zeros_like(arr)
    xs_n = _norm(all_xs)
    ys_n = _norm(all_ys)

    # ── decide rendering mode ─────────────────────────────────────────────────
    # "heatmap" mode: colour encodes w_value via a continuous colormap + colorbar
    # applied to ~50% of multi-series charts too (not just single-series)
    use_heatmap = single or (not single and random.random() < 0.50)

    if use_heatmap:
        # gather all points, colour by w_value across ALL series uniformly
        zs    = np.array([p["z_value"] for p in data_points])
        ws    = np.array([p["w_value"] for p in data_points])
        sizes = size_from_z(zs, z_range)
        xs, ys = numeric_positions(data_points, cat_axis, categories)

        cmap   = matplotlib.colormaps[template["colormap"]]
        w_norm_vals = (ws - ws.min()) / (np.ptp(ws) + 1e-9)
        colors = cmap(w_norm_vals)

        ax.scatter(xs, ys, s=sizes, c=colors,
                   alpha=template["alpha"],
                   edgecolors="none" if template["edgecolor"] == "none" else template["edgecolor"],
                   linewidths=template["linewidth"])

        sm = plt.cm.ScalarMappable(cmap=cmap,
                                   norm=mcolors.Normalize(ws.min(), ws.max()))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, shrink=0.72, pad=0.02)
        cbar.set_label(template["w_meaning"], fontsize=10,
                       color=_text_color(bg))
        cbar.ax.yaxis.set_tick_params(color=_tick_color(bg))
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color=_text_color(bg))

        series_legend_loc = random.choice(["upper left", "lower left",
                                           "upper right", "lower right"])

    else:
        # categorical colour per series
        patches = []
        for idx, sname in enumerate(series_names):
            pts   = [p for p in data_points if p["series_name"] == sname]
            zs    = np.array([p["z_value"] for p in pts])
            sizes = size_from_z(zs, z_range)
            color = SERIES_COLORS[idx % len(SERIES_COLORS)]
            xs, ys = numeric_positions(pts, cat_axis, categories)

            ax.scatter(xs, ys, s=sizes, c=color, label=sname,
                       alpha=template["alpha"],
                       edgecolors=template["edgecolor"],
                       linewidths=template["linewidth"])
            patches.append(mpatches.Patch(color=color, label=sname))

        series_legend_loc = _best_series_legend_loc(xs_n, ys_n)
        tc = _text_color(bg)
        leg = ax.legend(handles=patches, title="Series",
                        loc=series_legend_loc, fontsize=9,
                        framealpha=0.6, edgecolor="#AAAAAA")
        leg.get_title().set_color(tc)
        for txt in leg.get_texts():
            txt.set_color(tc)
        leg.get_frame().set_facecolor(bg)

    # ── shared size legend (inset, right margin) ──────────────────────────────
    fig.subplots_adjust(right=0.78)
    _draw_size_legend(fig, ax, z_range, z_label, bg,
                      xs_n, ys_n, series_legend_loc)

    # ── categorical axis ticks ────────────────────────────────────────────────
    if cat_axis == "x" and categories:
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories, rotation=30, ha="right", fontsize=9)
    elif cat_axis == "y" and categories:
        ax.set_yticks(range(len(categories)))
        ax.set_yticklabels(categories, fontsize=9)

    ax.set_title(template["title"], fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel(template["x_label"], fontsize=11)
    ax.set_ylabel(template["y_label"], fontsize=11)
    ax.tick_params(labelsize=9)
    ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.45)

    # ── FORCE label/tick visibility (must come last) ──────────────────────────
    _apply_label_visibility(ax, fig, bg)

    plt.savefig(filename, dpi=130, bbox_inches="tight")
    plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
#  JSON BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def build_json(template, data_points):
    series_names = list(dict.fromkeys(p["series_name"] for p in data_points))
    single       = len(series_names) == 1

    return {
        "chart_title":      template["title"],
        "x_axis_label":     template["x_label"],
        "y_axis_label":     template["y_label"],
        "categorical_axis": template.get("categorical_axis"),
        "data_points": [
            {
                "series_name": p["series_name"],
                "x_value":     p["x_value"],
                "y_value":     p["y_value"],
                "z_value":     p["z_value"],
                "w_value":     p["w_value"] if not single else p["w_value"],
            }
            for p in data_points
        ],
    }

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("╔══════════════════════════════════════════════╗")
    print("║       Bubble Chart Generator  v3.0           ║")
    print("╚══════════════════════════════════════════════╝")
    print(f"  Numeric templates    : {len(NUMERIC_TEMPLATES)}")
    print(f"  Categorical templates: {len(CATEGORICAL_TEMPLATES)}")

    while True:
        try:
            n_charts = int(input("\nQuanti grafici vuoi generare? "))
            if n_charts < 1:
                print("Inserisci un numero intero positivo.")
                continue
            break
        except ValueError:
            print("Input non valido.")

    # 30% categorici, 70% numerici
    n_cat = max(1, round(n_charts * 0.30)) if n_charts >= 2 else 0
    n_num = n_charts - n_cat

    num_pool = NUMERIC_TEMPLATES.copy()
    cat_pool = CATEGORICAL_TEMPLATES.copy()
    random.shuffle(num_pool)
    random.shuffle(cat_pool)

    chosen = []
    for i in range(n_num):
        chosen.append(num_pool[i % len(num_pool)])
    for i in range(n_cat):
        chosen.append(cat_pool[i % len(cat_pool)])
    random.shuffle(chosen)

    generated = []

    for i, tpl in enumerate(chosen):
        # deep-copy + jitter numeric ranges
        tpl_copy = {k: v for k, v in tpl.items() if k not in ("series", "categories")}
        tpl_copy["series"] = []
        for s in tpl["series"]:
            sc  = {k: v for k, v in s.items()}
            jit = random.uniform(0.88, 1.12)
            for axis_key in ("x", "y"):
                if axis_key in sc and isinstance(sc[axis_key], tuple):
                    sc[axis_key] = (sc[axis_key][0] * jit, sc[axis_key][1] * jit)
            tpl_copy["series"].append(sc)
        if "categories" in tpl:
            tpl_copy["categories"] = tpl["categories"]

        cat_tag = f"[CAT-{tpl_copy['categorical_axis'].upper()}]" \
                  if tpl_copy.get("categorical_axis") else "[NUM]"
        print(f"\n[{i+1}/{n_charts}] {cat_tag} '{tpl_copy['title']}' ...",
              end=" ", flush=True)

        data_points = build_data_points(tpl_copy)
        base_name   = f"chart{i+1:02d}_{tpl_copy['name']}"
        img_path    = os.path.join(IMG_OUTPUT_DIR,  base_name + ".png")
        json_path   = os.path.join(JSON_OUTPUT_DIR, base_name + ".json")

        render_chart(tpl_copy, data_points, img_path)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(build_json(tpl_copy, data_points), f, indent=2, ensure_ascii=False)

        generated.append((img_path, json_path))
        print("✓")

    n_cat_done = sum(1 for t in chosen if t.get("categorical_axis"))
    n_num_done = n_charts - n_cat_done
    print(f"\n{n_charts} grafici generati.")
    print(f"   Immagini   : {IMG_OUTPUT_DIR}")
    print(f"   JSON       : {JSON_OUTPUT_DIR}")
    print(f"   Numerici   : {n_num_done}  ({100*n_num_done//n_charts}%)")
    print(f"   Categorici : {n_cat_done}  ({100*n_cat_done//n_charts}%)")

if __name__ == "__main__":
    main()
