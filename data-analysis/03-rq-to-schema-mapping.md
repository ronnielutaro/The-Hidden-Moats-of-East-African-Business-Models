# Research Question to Schema Mapping (Updated Design)

This document maps our DeepMind-style strategic research questions (RQs) to their corresponding database columns, computational methods, and academic literature frameworks.

---

## Mapping Matrix

| Research Question | Database Columns | Analysis / Computational Method | Academic Literature Reference |
| :--- | :--- | :--- | :--- |
| **RQ1. The Venture Subsidy Decay Curve** | `total_funding_usd`, `pricing_strategy`, `lifespan_years`, `survival_status` | **Stratified Lifespan Decay Curve:** Kaplan-Meier survival curves comparing firms using "Underpricing" with VC funding against value-based, bootstrapped operations. | *Mata & Portugal (1994)* — Financing constraints, startup capital size, and firm duration curves. |
| **RQ2. Mobile Money Disintermediation** | `disintermediation_risk`, `customer_retention_rate_annual`, `switching_cost_moat` | **Churn Boundary Logistics:** Correlation matrix and logistic regression modeling the probability of high customer retention ($y \ge 60\%$) as a function of bypass risk. | *Sekar & Siddiq (2023)* — Information asymmetry, transaction fee bypass, and pricing remedies. |
| **RQ3. The Regulatory Moat** | `regulatory_barrier_level`, `lifespan_years`, `survival_status` | **Hazard Ratio Modeling:** Cox Proportional Hazards modeling to evaluate if high regulatory audit requirements increase the survival coefficient. | *Audretsch (1991)* — Post-entry learning, market entry barriers, and firm longevity. |
| **RQ4. Route-to-Market CapEx Trade-off** | `route_to_market_ops`, `switching_cost_moat`, `customer_retention_rate_annual` | **Factorial ANOVA Interaction:** Evaluating the interaction effects of physical footprints (Asset-Heavy) and digital databases (Switching Moat) on retention. | *Coase (1937)* — Transaction Cost Economics and make-or-buy vertical integration. |
| **RQ5. The Pivot Limit** | `pivot_count`, `expansion_count`, `restructure_count`, `lifespan_years` | **Polynomial Quadratic Fitting:** Fitting a quadratic curve to test if the hazard rate rises exponentially past 3 strategic shifts (Strategic Drift). | *Strategic Adaptability Literature* — Cognitive flexibility vs. resource exhaustion in startups. |
| **RQ6. Dollar-Shilling Capital Mismatch** | `funding_archetype`, `restructure_count`, `lifespan_years`, `survival_status` | **Restructure Frequency Correlation:** Evaluating correlation coefficients between foreign equity funding structures and firm restructuring events. | *Macro-Financial Vulnerability Theory* — Currency mismatches in emerging market corporate capital. |

---

## Statistical Details

### 1. Kaplan-Meier Survival Curves
*   **Implementation:** Step-wise survivor probability estimation:
  $$S(t) = \prod_{t_i \le t} \left(1 - \frac{d_i}{n_i}\right)$$
  where $d_i$ is the number of business failures at time $t_i$, and $n_i$ is the total count of firms at risk just prior to $t_i$.

### 2. Cox Proportional Hazards Model
*   **Implementation:** Evaluating covariate hazard coefficients:
  $$\lambda(t | X) = \lambda_0(t) \exp(\beta_1 X_1 + \beta_2 X_2 + \dots)$$
  where $X_1$ is `regulatory_barrier_level` and $X_2$ is `proximity_to_transaction`.

### 3. Gini Feature Importance (Random Forest Classifier)
*   **Implementation:** Fit a random forest predicting `survival_status == 'Active'` to extract the relative split decision weights (Mean Decrease in Impurity) of all operational features.
