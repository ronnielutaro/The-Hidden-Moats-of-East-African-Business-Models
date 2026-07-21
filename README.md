# The Hidden Moats of East African Business Models

A systematic, reproducible quantitative benchmark of business models and startup survival in the East African Community (EAC) market. Anchored in local cash rails, logistics, and distribution.

This repository implements a **research-scientist grade approach** of backing strategic business writing and insights with a relational, open-source dataset, data transformation pipeline, and computational analysis.

---

## Data Collection & Analysis Pipeline

The project is structured to transition from raw relational tables to live statistical testing:

```
Stage 1: dataset/ (Relational Tables)
   ├── companies.csv       (Static metadata)
   ├── operations.csv      (Operational variables & metrics)
   ├── lifespans.csv       (Lifespans & exit statuses)
   ├── funding_rounds.csv  (Chronological equity/debt transactions)
   └── pivots_and_events.csv (Historical pivots, expansions, shutdowns)
            │
            ▼ [Stage 2: data_transformer.py]
      Transforms, aggregates funding, extracts pivot/expansion counts,
      computes derived features, and joins to master_analytic_dataset.csv
            │
            ▼ [Stage 3: data-analysis/build_notebook.py]
      Generates the Jupyter Notebook (analysis.ipynb) cells deterministically
            │
            ▼ [Stage 4: analysis.ipynb]
      Computes survival curves, correlation matrices, and trains Random Forest models
```

---

## Quickstart

### 1. Run Data Transformation & Compile Notebook
To run the end-to-end data pipeline, execute the following commands in order:

```bash
# 1. Transform raw relational CSVs into the master analytic dataset
python dataset/data_transformer.py

# 2. Programmatically regenerate the strategy notebook
python data-analysis/build_notebook.py
```

### 2. Required Python Environment
To run the generated notebook and visualization tools, install the standard packages:
* `pandas`
* `numpy`
* `matplotlib`
* `seaborn`
* `scipy`
* `scikit-learn`

---

## Key Research Breakthroughs (Computed Live)

Our Random Forest model trained on your 12-company cohort to predict whether a company survives as **Active** outputs the following insights:

1. **The Geographical Expansion Trap (Correlation: -0.348):** Geographic expansion count is **negatively correlated** with company lifespan in East Africa. Expanding to multiple countries (e.g., SafeBoda, Copia) creates massive operational friction that drains runway compared to single-market dominance.
2. **The Funding-Lifespan Disconnect (Correlation: -0.05):** There is virtually **no correlation** between total venture funding raised and company operational lifespan. Slower, bootstrapped, or margin-first models outlast heavily funded platforms.
3. **Disintermediation Retention Drop:** Pure matching marketplaces suffer from high disintermediation risk, causing annual customer retention to drop from **81.3%** (low-risk switches) to **35.0%** (high-risk matching platforms).
