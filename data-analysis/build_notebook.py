"""Build analysis.ipynb for East African Business Models -- deterministic, reproducible.

Run this script to generate the Jupyter Notebook data-analysis/analysis.ipynb.
All strategy insights are computed live from dataset/master_analytic_dataset.csv.
"""
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRIPT_DIR, 'analysis.ipynb')

def md(src):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': src.splitlines(keepends=True)}

def code(src):
    return {
        'cell_type': 'code',
        'metadata': {},
        'source': src.splitlines(keepends=True),
        'outputs': [],
        'execution_count': None
    }

# ======== CELL DEFINITIONS ========
cells = []

# ---- PREAMBLE ----
cells += [
    md("""# East African Business Model Survival Analysis
    
**Strategy Notebook v2.0 (Research Scientist Grade)**
This notebook performs a quantitative audit of regional business models in East Africa (Uganda, Kenya, Tanzania). All calculations, survival curves, and feature importance matrices are computed live from your proprietary relational dataset (`dataset/master_analytic_dataset.csv`).

The analysis is structured to answer our core research questions:
1. **Descriptive:** How do model features correlate with lifespan and status?
2. **Funding & Pivot Dynamics:** How does VC funding scale, pivots, and expansion count correlate with business lifespans and survival?
3. **Predictive:** What features are the strongest predictors of survival and scale?
4. **Actionable:** The data-backed build checklist for builders and investors.
"""),
    
    code("""# ===== ENVIRONMENT SETUP & DATA LOADER =====
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings('ignore')
sns.set_theme(style='whitegrid')
plt.rcParams.update({'figure.dpi': 120, 'font.size': 10})

csv_path = '../dataset/master_analytic_dataset.csv'
if not os.path.exists(csv_path):
    # Fallback if run from different folder
    csv_path = 'dataset/master_analytic_dataset.csv'

df = pd.read_csv(csv_path)

# Enforce clean data types
df['proximity_to_transaction'] = pd.to_numeric(df['proximity_to_transaction'], errors='coerce').astype(int)
df['supply_chain_visibility'] = pd.to_numeric(df['supply_chain_visibility'], errors='coerce').astype(int)
df['estimated_scale_tier'] = pd.to_numeric(df['estimated_scale_tier'], errors='coerce').astype(int)
df['lifespan_years'] = pd.to_numeric(df['lifespan_years'], errors='coerce').astype(float)
df['regulatory_barrier_level'] = pd.to_numeric(df['regulatory_barrier_level'], errors='coerce').astype(int)
df['customer_retention_rate_annual'] = pd.to_numeric(df['customer_retention_rate_annual'], errors='coerce').astype(float)

# Load engineered relational features
df['total_funding_usd'] = pd.to_numeric(df['total_funding_usd'], errors='coerce').astype(float)
df['funding_rounds_count'] = pd.to_numeric(df['funding_rounds_count'], errors='coerce').astype(int)
df['pivot_count'] = pd.to_numeric(df['pivot_count'], errors='coerce').astype(int)
df['expansion_count'] = pd.to_numeric(df['expansion_count'], errors='coerce').astype(int)
df['restructure_count'] = pd.to_numeric(df['restructure_count'], errors='coerce').astype(int)
df['funding_per_year_usd'] = pd.to_numeric(df['funding_per_year_usd'], errors='coerce').astype(float)

df['cold_chain_requirement'] = df['cold_chain_requirement'].fillna(False).astype(bool)
df['switching_cost_moat'] = df['switching_cost_moat'].fillna(False).astype(bool)
df['has_pivoted'] = df['has_pivoted'].fillna(False).astype(bool)

print(f"Loaded: {len(df)} business entities from {df['hq_location'].nunique()} regional hubs.")
""")
]

# ---- SECTION 1: DESCRIPTIVE METRICS ----
cells += [
    md("""---
## Section 1: Descriptive Market Teardown

First, we analyze general survival and lifespan characteristics across different business models.
* *Lifespan by Primary Model:* How long do different models last on average?
* *Survival Rates by Proximity to Cash:* Does closeness to transactional flows correlate with active status?
* *Retention by Disintermediation Risk:* Does bypassing the platform impact annual customer retention?
* *Interaction Effect (RQ4):* How do Route-to-Market operations and switching cost moats interact to affect retention?
"""),
    
    code("""# Average lifespan by primary model
model_lifespans = df.groupby('primary_model').agg(
    count=('lifespan_years', 'count'),
    mean_lifespan=('lifespan_years', 'mean'),
    active_rate=('survival_status', lambda x: (x == 'Active').mean()),
    mean_retention=('customer_retention_rate_annual', 'mean')
).sort_values('mean_lifespan', ascending=False)

print("=== LIFESPAN & SURVIVAL BY PRIMARY MODEL ===")
print(model_lifespans)

# Survival rates by proximity to transaction
df['high_proximity'] = df['proximity_to_transaction'] == 5
proximity_survival = df.groupby('high_proximity').agg(
    n=('survival_status', 'count'),
    active_count=('survival_status', lambda x: (x == 'Active').sum()),
    active_rate=('survival_status', lambda x: (x == 'Active').mean()),
    mean_lifespan=('lifespan_years', 'mean')
)
print()
print("=== SURVIVAL BY CASH PROXIMITY (Tier 5 vs Tiers 1-4) ===")
print(proximity_survival)

# Retention rate by disintermediation risk
disint_retention = df.groupby('disintermediation_risk').agg(
    n=('customer_retention_rate_annual', 'count'),
    mean_retention=('customer_retention_rate_annual', 'mean')
).sort_values('mean_retention', ascending=False)
print()
print("=== ANNUAL RETENTION BY DISINTERMEDIATION RISK ===")
print(disint_retention)

# Interaction Effect Audit: Route-to-Market Ops x Switching Cost Moat
interaction_retention = df.groupby(['route_to_market_ops', 'switching_cost_moat']).agg(
    count=('company_id', 'count'),
    mean_retention=('customer_retention_rate_annual', 'mean'),
    std_retention=('customer_retention_rate_annual', 'std')
).reset_index()
print()
print("=== INTERACTION EFFECT: ROUTE-TO-MARKET X SWITCHING MOAT ON RETENTION ===")
print(interaction_retention)
""")
]

# ---- SECTION 2: FUNDING & EXPANSION PIPELINE ----
cells += [
    md("""---
## Section 2: Funding & Expansion Pipeline (Venture Decay & Pivot Dynamics)

Now we analyze the relational features calculated by our pipeline:
1. **The Funding Efficiency Gap:** How much funding is raised relative to lifespan for Active vs. Failed companies?
2. **Expansion Friction (RQ6):** Does geographical expansion and total USD funding correlate with restructuring events?
3. **The Pivot Limit (RQ5):** Does strategic adaptation show a quadratic limit beyond which survival probability decays?
"""),
    
    code("""# Funding efficiency by survival outcome
funding_by_status = df.groupby('survival_status').agg(
    count=('company_id', 'count'),
    mean_funding_usd=('total_funding_usd', 'mean'),
    mean_funding_per_year_usd=('funding_per_year_usd', 'mean'),
    mean_lifespan_years=('lifespan_years', 'mean')
)
print("=== FUNDING METRICS BY SURVIVAL STATUS ===")
print(funding_by_status)

# Pivot and expansion counts
pivots_expansions = df.groupby('survival_status').agg(
    mean_pivots=('pivot_count', 'mean'),
    mean_expansions=('expansion_count', 'mean'),
    mean_restructures=('restructure_count', 'mean')
)
print()
print("=== PIVOT & EXPANSION METRICS BY SURVIVAL STATUS ===")
print(pivots_expansions)

# Correlation matrix of relational variables
relational_corr = df[['total_funding_usd', 'pivot_count', 'expansion_count', 'restructure_count', 'lifespan_years']].corr()
print()
print("=== RELATIONAL CORRELATION MATRIX ===")
print(relational_corr)

# Capital Mismatch (RQ6): Correlation between USD funding and restructuring events
funding_mismatch_corr = df['total_funding_usd'].corr(df['restructure_count'])
print()
print("=== CAPITAL STRUCTURE CORRELATION ===")
print(f"Correlation between total USD funding and Restructuring count: {funding_mismatch_corr:.4f}")

# The Pivot Limit Inflection Fit (RQ5)
df['total_strategic_events'] = df['pivot_count'] + df['expansion_count']
y_survival = (df['survival_status'] == 'Active').astype(int)
x_events = df['total_strategic_events']

# Fit quadratic model: y = ax^2 + bx + c
poly_coefs = np.polyfit(x_events, y_survival, 2)
a_coef, b_coef, c_coef = poly_coefs
vertex_x = -b_coef / (2 * a_coef) if a_coef != 0 else np.nan

print()
print("=== THE PIVOT LIMIT QUADRATIC FIT ===")
print(f"Quadratic Curve: y = {a_coef:.4f}x^2 + {b_coef:.4f}x + {c_coef:.4f}")
print(f"Calculated Pivot Inflection Point (Vertex): {vertex_x:.2f} strategic events")
"""),

    md("""### Visualizing the Pivot Limit Inflection Curve
We plot the fitted quadratic curve of survival probability against the total number of strategic events (pivots + expansions).
"""),

    code("""# Plot the quadratic curve
plt.figure(figsize=(9, 5))
x_range = np.linspace(0, df['total_strategic_events'].max() + 1, 100)
y_fit = a_coef * x_range**2 + b_coef * x_range + c_coef

sns.scatterplot(
    data=df,
    x='total_strategic_events',
    y=(df['survival_status'] == 'Active').astype(int),
    hue='survival_status',
    palette={'Active': '#2A9D8F', 'Failed': '#E76F51', 'Pivoted': '#F4A261'},
    s=150,
    edgecolor='black',
    linewidth=1.5,
    zorder=3
)

plt.plot(x_range, y_fit, color='#264653', lw=3, ls='--', label='Quadratic Survival Fit')

if not np.isnan(vertex_x) and 0 < vertex_x < x_range.max():
    plt.axvline(vertex_x, color='#E76F51', lw=1.5, ls=':', label=f'Pivot Inflection Point ({vertex_x:.1f} events)')

plt.xlabel('Total Strategic Events (Pivots + Expansions)', labelpad=12)
plt.ylabel('Probability of Active Survival', labelpad=12)
plt.title('The Pivot Limit: Survival Probability vs. Strategic Events', fontweight='bold', pad=15)
plt.ylim(-0.15, 1.15)
plt.legend(frameon=True, facecolor='white', edgecolor='#E5E5E5')
plt.tight_layout()
plt.show()
""")
]

# ---- SECTION 3: SURVIVAL ANALYSIS (KAPLAN-MEIER) ----
cells += [
    md("""---
## Section 3: Kaplan-Meier Survival Analysis

To handle right-censoring correctly (companies that are currently active and haven't failed), we construct step-wise Kaplan-Meier survival curves. 
We plot the probability of remaining **Active** over time, stratified by:
1. **Cash Flow Proximity:** High Proximity (Tier 5) vs. Low/Med Proximity (Tiers 1-4).
2. **Route-to-Market Operations:** Asset-Heavy vs. Asset-Light.
"""),
    
    code("""def calculate_km_curve(data, time_col, event_col):
    \"\"\"Compute Kaplan-Meier survival probabilities step-by-step.\"\"\"
    times = sorted(data[time_col].unique())
    survival_prob = 1.0
    km_times = [0.0]
    km_probs = [1.0]
    
    n_at_risk = len(data)
    
    for t in times:
        # Number of failures at time t
        failures = len(data[(data[time_col] == t) & (data[event_col] == False)]) # Failure = Not Active
        # Number of censored at time t (active companies)
        censored = len(data[(data[time_col] == t) & (data[event_col] == True)])
        
        if n_at_risk > 0:
            survival_prob *= (1.0 - (failures / n_at_risk))
            
        km_times.append(t)
        km_probs.append(survival_prob)
        
        n_at_risk -= (failures + censored)
        
    return km_times, km_probs

# Plotting Kaplan-Meier curves
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# 1. Stratify by High Cash Proximity
df['is_active'] = df['survival_status'] == 'Active'
groups_prox = df['high_proximity'].unique()

for group in sorted(groups_prox):
    group_data = df[df['high_proximity'] == group]
    t, s = calculate_km_curve(group_data, 'lifespan_years', 'is_active')
    label = "High Proximity (Tier 5)" if group else "Low/Med Proximity (Tiers 1-4)"
    color = "#2A9D8F" if group else "#E76F51"
    ax1.step(t, s, where='post', label=label, color=color, lw=2.5)

ax1.set_xlabel('Years in Operation')
ax1.set_ylabel('Survival Probability (P_Active)')
ax1.set_title('Survival Curve by Cash Proximity', fontweight='bold', pad=15)
ax1.set_ylim(0, 1.05)
ax1.legend(frameon=True, facecolor='white')

# 2. Stratify by Route-to-Market Ops
groups_rtm = df['route_to_market_ops'].unique()
for group in groups_rtm:
    group_data = df[df['route_to_market_ops'] == group]
    t, s = calculate_km_curve(group_data, 'lifespan_years', 'is_active')
    color = "#E76F51" if group == 'Asset-Heavy' else "#2A9D8F"
    ax2.step(t, s, where='post', label=f"{group} Ops", color=color, lw=2.5)

ax2.set_xlabel('Years in Operation')
ax2.set_ylabel('Survival Probability (P_Active)')
ax2.set_title('Survival Curve by Route-to-Market Ops', fontweight='bold', pad=15)
ax2.set_ylim(0, 1.05)
ax2.legend(frameon=True, facecolor='white')

plt.tight_layout()
plt.show()
""")
]

# ---- SECTION 4: THE STRATEGIC MATRIX ----
cells += [
    md("""---
## Section 4: The Transaction vs. Visibility Matrix

Here, we plot the full matrix of **Proximity to Transaction** vs. **Supply Chain Visibility** to identify strategic zones of defensibility.
* *Bubble Size:* Mapped to the company's `estimated_scale_tier`.
* *Color:* Mapped to `route_to_market_ops` (Asset-Heavy vs. Asset-Light).
"""),
    
    code("""# Create the figure
fig, ax = plt.subplots(figsize=(10, 8), dpi=120)

# Define color palette and scaling
palette = {'Asset-Heavy': '#E76F51', 'Asset-Light': '#2A9D8F'}
sizes = df['estimated_scale_tier'] * 250

# Scatter plot
sns.scatterplot(
    data=df,
    x='proximity_to_transaction',
    y='supply_chain_visibility',
    hue='route_to_market_ops',
    palette=palette,
    size=sizes,
    sizes=(200, 800),
    legend='brief',
    alpha=0.85,
    edgecolor='black',
    linewidth=1.5,
    ax=ax
)

# Annotate company names
for i in range(df.shape[0]):
    row = df.iloc[i]
    x_offset = 0.12
    y_offset = 0.05
    
    # Preventing label overlaps
    if row['company_name'] == 'Lipa Later':
        y_offset = -0.15
    elif row['company_name'] == 'MTN MoMo':
        y_offset = 0.15
    elif row['company_name'] == 'Airtel Money':
        x_offset = -0.6
        y_offset = -0.15
    elif row['company_name'] == 'SafeBoda':
        y_offset = -0.18
        
    ax.text(
        row['proximity_to_transaction'] + x_offset,
        row['supply_chain_visibility'] + y_offset,
        row['company_name'],
        horizontalalignment='left',
        size='small',
        color='#264653',
        weight='bold'
    )
    
ax.set_xlabel('Proximity to Cash Transaction (1 = Far, 5 = Direct/Mobile Money Rail)', labelpad=15)
ax.set_ylabel('Supply Chain Visibility (1 = Deep Black Hole, 5 = Real-Time Stream)', labelpad=15)
ax.set_title('East African Business Models: The Transaction vs. Visibility Matrix', pad=20, weight='bold')

ax.set_xlim(0.5, 5.5)
ax.set_ylim(0.5, 5.5)
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_yticks([1, 2, 3, 4, 5])

# Draw strategic zones
ax.axvspan(4, 5.5, ymin=0.6, ymax=1.0, color='#2A9D8F', alpha=0.03)
ax.text(4.75, 4.8, 'Digital\\nControl Room', color='#1D6F66', fontsize=10, style='italic', weight='semibold', ha='center')

ax.axvspan(0.5, 3.5, ymin=0.0, ymax=0.5, color='#E76F51', alpha=0.03)
ax.text(2.0, 1.3, 'Traditional Logistics\\n(Asset-Heavy Moat)', color='#B14A33', fontsize=10, style='italic', weight='semibold', ha='center')

# Highlight the "Supply Chain Visibility Black Hole"
ax.annotate(
    'The Visibility Black Hole\\n(Traditional FMCG Trap)',
    xy=(3, 1),
    xytext=(1.5, 2.5),
    arrowprops=dict(facecolor='#264653', shrink=0.08, width=1.5, headwidth=6),
    color='#264653',
    weight='semibold',
    bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.2)
)

# Clean legend
handles, labels = ax.get_legend_handles_labels()
new_handles = []
new_labels = []
for h, l in zip(handles, labels):
    if l in ['route_to_market_ops', 'estimated_scale_tier']:
        continue
    if l in ['Asset-Heavy', 'Asset-Light']:
        new_handles.append(h)
        new_labels.append(l + ' Ops')
ax.legend(new_handles, new_labels, loc='upper left', frameon=True, facecolor='white', edgecolor='#E5E5E5')

plt.tight_layout()
plt.show()
""")
]

# ---- SECTION 5: PREDICTIVE FEATURE IMPORTANCE ----
cells += [
    md("""---
## Section 5: Predictive Modeling (Feature Importance)

We train a **Random Forest Classifier** to evaluate which structural business model features and relational pipeline variables (funding rate, pivots) are the strongest predictors of whether a company survives as **Active** in the East African ecosystem.
"""),
    
    code("""# Prepare data for modeling
feature_cols = ['proximity_to_transaction', 'supply_chain_visibility', 'switching_cost_moat', 
                'cold_chain_requirement', 'regulatory_barrier_level', 'disintermediation_risk', 
                'pricing_strategy', 'total_funding_usd', 'pivot_count', 'expansion_count']

# Encode categorical variables
X = df[feature_cols].copy()
X['switching_cost_moat'] = X['switching_cost_moat'].astype(int)
X['cold_chain_requirement'] = X['cold_chain_requirement'].astype(int)

le_disint = LabelEncoder()
X['disintermediation_risk'] = le_disint.fit_transform(X['disintermediation_risk'])

le_price = LabelEncoder()
X['pricing_strategy'] = le_price.fit_transform(X['pricing_strategy'])

y = (df['survival_status'] == 'Active').astype(int)

# Train a Random Forest Classifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

# Print Feature Importance
importances = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)

print("=== BUSINESS MODEL FEATURE IMPORTANCE (Predicting Active Status) ===")
for name, imp in importances.items():
    print(f"  {name:30s} : {imp:.4f}  ({imp*100:.1f}%)")

# Plot feature importances
plt.figure(figsize=(10, 5))
sns.barplot(x=importances.values * 100, y=importances.index, palette='viridis')
plt.xlabel('Importance (%)')
plt.title('Business Model Survival Predictors (Random Forest Importance)', fontweight='bold', pad=15)
plt.tight_layout()
plt.show()
""")
]

# ---- SECTION 6: STRATEGIC BLUEPRINT ----
cells += [
    md("""---
## Section 6: The "Nate Silver" Strategy Checklist

Based on the live data, we outline the **Survival and Scale Checklist** for new ventures entering East Africa:
1. **Cash Flow Proximity (MoMo Alignment):** If proximity is <3, you face high default rates.
2. **Switching Cost Moat:** If margins are Low/Med (FMCG/Logistics), you must build a ledger lock-in.
3. **Visibility & Pipes:** If visibility is <3, your business is operating in a black hole.
"""),
    
    code("""# Compute checklist probabilities
print("=== LIVE DATA STRATEGY CHECKLIST ===")

# 1. Proximity Tier 5 win rate vs rest
p_5_active = (df[df['proximity_to_transaction'] == 5]['survival_status'] == 'Active').mean()
p_rest_active = (df[df['proximity_to_transaction'] < 5]['survival_status'] == 'Active').mean()
print(f"  1. Cash Proximity Tier 5 Active Rate : {p_5_active:.1%} (vs. Rest: {p_rest_active:.1%})")

# 2. Switch cost impact for low-medium margin players
low_med_margin = df[df['gross_margin_tier'].isin(['Low', 'Medium'])]
moat_active = (low_med_margin[low_med_margin['switching_cost_moat'] == True]['survival_status'] == 'Active').mean()
no_moat_active = (low_med_margin[low_med_margin['switching_cost_moat'] == False]['survival_status'] == 'Active').mean()
print(f"  2. Low/Med Margin + Switching Moat Active Rate : {moat_active:.1%} (vs. No Moat: {no_moat_active:.1%})")

# 3. High Visibility scale rate
vis_3_plus_scale = (df[df['supply_chain_visibility'] >= 3]['estimated_scale_tier'] == 3).mean()
vis_low_scale = (df[df['supply_chain_visibility'] < 3]['estimated_scale_tier'] == 3).mean()
print(f"  3. High Visibility (>=3) Scale Tier 3 Rate   : {vis_3_plus_scale:.1%} (vs. Low: {vis_low_scale:.1%})")
""")
]

# Write to file
nb = {
    'cells': cells,
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'name': 'python'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 2
}

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print(f"Deterministic strategy notebook structure written to {OUT}!")
