# Data Practicality and Feasibility Audit

Collecting granular business model data in the East African Community (EAC) requires navigating high levels of information asymmetry, private ownership structures, and regulatory secrecy. This audit evaluates the practicality of collecting each database variable and establishes data-gathering protocols.

---

## Variable Feasibility Assessment

### 1. High Feasibility (Publicly Verifiable)
* **`company_name` / `hq_location`:** Verifiable via company registry lookups, LinkedIn profiles, and news filings.
* **`primary_model` / `target_segment`:** Determined by reviewing company websites and customer-facing interfaces.
* **`funding_archetype`:** Tracked through databases like Crunchbase, Baobab Insights, Techpoint Africa, and local news releases.
* **`regulatory_barrier_level`:** Inferred directly from regional licensing frameworks (e.g., Central Bank approvals for fintechs vs. standard municipal trading licenses for retail).

### 2. Medium Feasibility (Requires Proxy Analysis)
* **`route_to_market_ops` / `cold_chain_requirement`:** Verified via job postings (e.g., hiring fleet managers vs. delivery contractors) and app user pathways.
* **`proximity_to_transaction`:** Audited by testing checkout flows inside the product (e.g., checking if mobile money payment goes straight to a paybill/merchant code or requires manual bank confirmation).
* **`estimated_scale_tier`:** Estimated using public proxies: Google Play Store download volumes, active location footprint, and employee headcounts on LinkedIn.
* **`disintermediation_risk`:** Audited by conducting field tests on B2B/B2C marketplace interfaces to check if transaction lock-in mechanisms (like internal wallets or insurance) exist to prevent users from transacting directly.
* **`pricing_strategy`:** Audited by scraping publicly available pricing pages or conducting secret-shopper calls for B2B products to evaluate pricing quotes.

### 3. Low Feasibility (Confidential Internal Data)
* **`switching_cost_moat` / `supply_chain_visibility`:** Requires internal software architecture audits. Mitigated by using external indicators (e.g., checking if the company requires customers to import proprietary hardware/ledgers or uses digital agent portals).
* **`customer_retention_rate_annual`:** Typically protected behind strict B2B/B2C NDAs. 
  * *Mitigation Protocol:* We estimate this using:
    1. Public statements in pitch decks, investor reports, or accelerator case studies.
    2. cohort user activity tracking (e.g. comparing month-on-month active driver/rider numbers or app usage indicators).
    3. Anonymous founder surveys and local developer network polls.

---

## Key Confounders & Mitigations

### 1. The "Nairobi Effect" (Country-Level Bias)
* **Confounder:** Kenya receives a disproportionate share of VC funding in East Africa, distorting startup lifespan data regardless of underlying business model quality (since companies can survive on runway alone rather than cash-flow fit).
* **Mitigation:** Include `hq_location` as a stratifying variable and contrast lifespan against `funding_archetype` (VC-backed vs. bootstrapped) to check if VC funding masks terminal business model weaknesses.

### 2. Disintermediation Leakage Bias
* **Confounder:** Founders of marketplaces frequently overstate transaction volumes by counting matching events rather than closed checkouts, hiding massive offline leakage.
* **Mitigation:** We classify `disintermediation_risk` using structural platform checkouts. A platform that does not control the payment gateway or physical logistics delivery is automatically labeled as having **High** disintermediation risk.
