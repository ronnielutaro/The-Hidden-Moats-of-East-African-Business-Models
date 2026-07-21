# The Schema Blueprint: Open-Source East African Market Intelligence Dataset

This document serves as the formal schema definition for Ronnie's benchmark database of East African tech startups and FMCG/manufacturing business models. It details the engineered columns, categorical lists, and the quantitative logic behind why these metrics matter for regional strategic analysis.

## Core Objective
To quantitatively audit business models across the East African Community (EAC) by measuring:
1. **Financial Velocity:** proximity to cash flows.
2. **Logistics & Route-to-Market (RTM) Moats:** distribution channel mix, cold-chain assets, and visibility.
3. **Strategic Defensibility:** operational lock-in and switching costs.

---

## Unified Core Schema Definition

### 1. Corporate Identity & Domain Positioning

#### `company_name`
* **Data Type:** String
* **Logic:** The verified legal or trading name of the commercial entity operating within East Africa.

#### `hq_location`
* **Data Type:** Categorical
* **Allowed Values:** `Kampala`, `Nairobi`, `Dar es Salaam`, `Kigali`, etc.
* **Logic:** Primary regional operational headquarters. Limited to specific regional growth hubs.

#### `primary_model`
* **Data Type:** Categorical
* **Allowed Values:** `SaaS`, `Transactional`, `Marketplace`, `E-commerce`, `Advertising`, `Hardware`, `Value-Added Services (VAS)`, `FMCG Manufacturing`
* **Logic:** The foundational business model dictating how the company operates. Adapted from the Silicon Valley / YC framework to include traditional industrial realities like FMCG.

#### `target_segment`
* **Data Type:** Categorical
* **Allowed Values:** `B2B`, `B2C`, `B2B2C`
* **Logic:** The primary customer base served by the commercial pipeline. `B2B2C` is highly prevalent in regional retail supply chain tech due to fragmented distribution networks.

---

### 2. Financial Velocity & Scale Architecture

#### `proximity_to_transaction`
* **Data Type:** Ordinal (Scale of 1 to 5)
* **Allowed Values:**
  * `1` = Far away from cash exchange (e.g., pure Content, Ad-supported, or Affiliate structures).
  * `3` = Traditional invoicing or net-payment terms (e.g., standard B2B wholesale orders with credit terms).
  * `5` = Directly in the mobile money/cash handling rail (e.g., Telecom switches, payment gateways, MoMo APIs, checkouts).
* **Logic:** Measures how closely the business model sits next to the literal flow of funds. In East Africa, proximity to cash is survival; businesses at `5` capture value much more efficiently than those at `1` or `2`.

#### `revenue_type`
* **Data Type:** Categorical
* **Allowed Values:** `Recurring` (SaaS subscriptions), `Usage-Based` (Transactional take-rates/commissions), `One-Off` (Standard per-unit physical/digital sales)
* **Logic:** The structural nature of the incoming cash flow.

#### `funding_archetype`
* **Data Type:** Categorical
* **Allowed Values:** `Venture Backed`, `Donor/Grant Funded` (capturing crucial development agency/NGO ecosystem layers), `Bootstrapped/Profitable`
* **Logic:** The capital engine backing the operations. Donor-funded layers can distort pricing mechanics.

#### `estimated_scale_tier`
* **Data Type:** Ordinal
* **Allowed Values:**
  * `1` = Seed / Pre-revenue / Early concept validation.
  * `2` = Growth stage / Steady local operations.
  * `3` = Dominant multi-market industry leader.
* **Logic:** High-level grouping of operational volume and regional presence.

---

### 3. Last-Mile Logistics & Route-to-Market (RTM) Features

#### `distribution_channel_mix`
* **Data Type:** Categorical / Combined String
* **Allowed Values:** `Direct-to-Consumer (D2C)`, `Modern Trade` (supermarkets, malls), `Traditional Trade` (duukas, kiosks, open markets), `B2B Wholesaler Push`
* **Logic:** The physical or digital delivery pathway. In East Africa, 80%+ of retail flows through Traditional Trade.

#### `route_to_market_ops`
* **Data Type:** Categorical
* **Allowed Values:** `Asset-Heavy` (owns distribution trucks, cold warehouses, dedicated delivery fleets) vs. `Asset-Light` (outsources entirely to independent third-party logistics, boda networks, or standard postal services)
* **Logic:** Identifies capital expenditure profiles. Asset-heavy operations require higher initial capital but establish stronger control.

#### `cold_chain_requirement`
* **Data Type:** Boolean (`True`/`False`)
* **Logic:** Critical indicator for food science, dairy, and pharmaceutical models. Continuous refrigeration dependencies heavily inflate physical operational risk and capital overhead.

#### `distributor_credit_terms`
* **Data Type:** Categorical
* **Allowed Values:** `Cash on Delivery (COD)`, `Short-term Credit (1-7 Days)`, `Long-term Credit (30+ Days)`
* **Logic:** Payment credit loops offered to down-market merchants. High credit duration raises exposure to local currency default risks.

#### `last_mile_ownership`
* **Data Type:** Categorical
* **Allowed Values:** `Proprietary Fleet`, `Aggregated 3PL`, `Merchant Pickup`
* **Logic:** Captures the degree of operational control over final physical transit.

#### `retail_distribution_reach`
* **Data Type:** Ordinal
* **Allowed Values:** `1` (Localized: <100 POS), `2` (Moderate: 100-1000 POS), `3` (Extensive: 1000+ POS)
* **Logic:** The physical reach and distribution network scale density of the firm.

#### `exclusivity_enforcement`
* **Data Type:** Boolean (`True`/`False`)
* **Logic:** Legal constraint preventing wholesale/distribution agents from carrying competing products.

---

### 4. Defensibility & Hidden Moat Metrics

#### `switching_cost_moat`
* **Data Type:** Boolean (`True`/`False`)
* **Logic:** Indicator of operational customer lock-in. Evaluates if tearing out the product causes catastrophic workflow data loss (e.g., proprietary ledger data, integrated billing) or extreme physical supply chain disruption.

#### `supply_chain_visibility`
* **Data Type:** Ordinal (Scale of 1 to 5)
* **Allowed Values:**
  * `1` = **Deep Black Hole:** Selling blind to middleman wholesalers/traders down in markets like Kikuubo; zero tracking past initial sale.
  * `3` = **Lagging Visibility:** Monthly or weekly manual aggregator/field reports; delayed feedback loops.
  * `5` = **Real-Time Stream:** Live stock velocity and instant shelf visibility verified via an integrated digital pipe directly from retail points.
* **Logic:** How cleanly data flows from the retail endpoint back to the manufacturer/brand owner. The core thesis of the "Hidden Moats" project is that capturing the *pipes* that move real-time data is the ultimate value-unlock.
