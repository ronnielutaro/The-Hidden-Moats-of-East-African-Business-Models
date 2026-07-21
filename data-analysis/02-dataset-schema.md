# Dataset Schema (East African Business Model Survival Analysis)

This document defines the relational schema for the proprietary East African Business Model dataset. To avoid data redundancy and maintain database integrity, the dataset is normalized into 5 relational tables stored in the `dataset/` directory.

---

## Relational Tables Schema

### 1. companies.csv (Static Core Metadata)
Defines the unchanging core attributes of each business entity.

| Column Name | Data Type | Key | Description | Allowed Values / Rubric | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **company_id** | string | PK | Unique identifier based on company name slug | String | `safeboda` |
| **company_name** | string | | Full trading name of the company | String | `SafeBoda` |
| **hq_location** | categorical | | Primary operational headquarters in East Africa | `Kampala`, `Nairobi`, `Dar es Salaam`, `Kigali` | `Kampala` |
| **primary_model** | categorical | | Core business model classification | `SaaS`, `Transactional`, `Marketplace`, `E-commerce`, `FMCG Manufacturing`, `Services`, `Traditional Retail` | `Marketplace` |
| **target_segment** | categorical | | Main customer target profile | `B2B`, `B2C`, `B2B2C` | `B2C` |
| **cold_chain_requirement** | boolean | | Requires continuous refrigeration for operations | `True`, `False` | `False` |
| **disintermediation_risk** | categorical | | Risk of users taking transactions offline | `Low`, `Medium`, `High` (See Rubric) | `High` |
| **pricing_strategy** | categorical | | Primary strategy used for setting price | `Value-Based`, `Cost-Plus`, `Underpricing` | `Underpricing` |
| **industry_sector** | categorical | | Domain economic sector | `Fintech`, `Agtech / Food Logistics`, `Mobility / Transport`, `Healthtech`, `FMCG / Manufacturing`, `Proptech / E-commerce`, `E-commerce / Retail` | `Fintech` |
| **founder_count** | integer | | Number of co-founders at founding | Integer (1, 2, 3, 4+) | `2` |
| **target_income_tier** | categorical | | Target consumer/client economic bracket | `Low Income (<150k UGX/mo)`, `Middle Income (150k-1M UGX/mo)`, `High Income (>1M UGX/mo)`, `B2B Institutional` | `Low Income (<150k UGX/mo)` |

---

### 2. operations.csv (Operational Metrics & Levers)
Defines the operational scale, route-to-market structure, and transaction characteristics.

| Column Name | Data Type | Key | Description | Allowed Values / Rubric | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **company_id** | string | FK | References `companies.company_id` | String | `safeboda` |
| **estimated_scale_tier** | ordinal | | Operational and geographical scale class | `1` (Seed/Pre-rev), `2` (Growth/Steady), `3` (Dominant Leader) | `3` |
| **route_to_market_ops** | categorical | | CapEx profile of Route-To-Market operations | `Asset-Heavy`, `Asset-Light` | `Asset-Light` |
| **distribution_channel_mix**| categorical | | Primary delivery pathway to retail shelf | `D2C`, `Modern Trade`, `Traditional Trade`, `B2B Wholesaler Push` | `Traditional Trade` |
| **supply_chain_visibility** | ordinal | | Level of real-time visibility from shelf to brand | `1` to `5` (1 = Black Hole, 5 = Real-Time) | `5` |
| **switching_cost_moat** | boolean | | Customer lock-in via databases or proprietary hardware | `True`, `False` | `False` |
| **proximity_to_transaction** | ordinal | | Closeness to the actual flow of funds | `1` to `5` (1 = Far, 5 = Direct/MoMo Rail) | `5` |
| **customer_retention_rate_annual** | float | | Estimated annual customer retention rate % | Decimal number (0.0 to 100.0) | `40.0` |
| **regulatory_barrier_level**| ordinal | | Level of compliance/licensing complexity | `1` (Low/None), `3` (Medium/Licensing), `5` (Strict Audit) | `3` |
| **gross_margin_tier** | categorical | | Estimated operational gross margins | `Low` (<20%), `Medium` (20-50%), `High` (>50%) | `High` |
| **distributor_credit_terms**| categorical | | Payment terms offered to downstream traders | `Cash on Delivery (COD)`, `Short-term Credit (1-7 Days)`, `Long-term Credit (30+ Days)` | `Cash on Delivery (COD)` |
| **last_mile_ownership** | categorical | | Physical transit fleet ownership status | `Proprietary Fleet`, `Aggregated 3PL`, `Merchant Pickup` | `Proprietary Fleet` |
| **retail_distribution_reach**| ordinal | | Physical density scale of active retail outlets | `1` (Localized: <100), `2` (Moderate: 100-1000), `3` (Extensive: 1000+) | `3` |
| **exclusivity_enforcement** | boolean | | Prevents distributors from selling competitor items | `True`, `False` | `False` |
| **revenue_stream_count** | integer | | Total active monetized revenue streams | Integer (1, 2, 3+) | `2` |
| **estimated_annual_revenue_range_usd** | categorical | | Estimated annual revenue bracket in USD | `<$100k`, `$100k-$1M`, `$1M-$5M`, `$5M-$20M`, `$20M+` | `$5M-$20M` |

---

### 3. lifespans.csv (Survival Outcomes)
Tracks firm duration, survival status, and exit characteristics.

| Column Name | Data Type | Key | Description | Allowed Values / Rubric | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **company_id** | string | FK | References `companies.company_id` | String | `safeboda` |
| **lifespan_years** | float | | Total years company has been operational | Decimal number | `9.0` |
| **survival_status** | categorical | | Current state of the business entity | `Active`, `Failed`, `Pivoted` | `Active` |
| **exit_outcome** | categorical | | Ultimate operational outcome | `Active`, `Acquired`, `Shut Down`, `IPO` | `Active` |
| **primary_failure_reason** | categorical | | Primary driver of firm shutdown or restructuring | `N/A (Active)`, `Runway Exhaustion / Illiquidity`, `Unit Economics Collapse`, `Disintermediation Churn`, `Founder Conflict`, `Macro Currency Shock` | `Disintermediation Churn` |


---

### 4. funding_rounds.csv (Funding History Transactions)
A transactional table recording funding events (1-to-many relationship with companies).

| Column Name | Data Type | Key | Description | Allowed Values / Rubric | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **company_id** | string | FK | References `companies.company_id` | String | `safeboda` |
| **round_type** | categorical | | Type of funding transaction | `Seed`, `Series A`, `Series B`, `Series C`, `Debt`, `Corporate Allocation`, `Grant` | `Series A` |
| **amount_usd** | float | | Amount of capital raised in USD | Float | `1100000.0` |
| **year** | integer | | Year the transaction occurred | Integer | `2016` |

---

### 5. pivots_and_events.csv (Chronological Strategic Events)
Tracks historical milestones, pivots, expansions, and restructuring events (1-to-many relationship).

| Column Name | Data Type | Key | Description | Allowed Values / Rubric | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **company_id** | string | FK | References `companies.company_id` | String | `safeboda` |
| **event_type** | categorical | | Nature of the strategic event | `Launch`, `Expansion`, `Pivot`, `Restructure`, `Shutdown` | `Pivot` |
| **year** | integer | | Year of the event | Integer | `2020` |
| **details** | string | | Narrative description of the event | String | `Launched food delivery and cashless wallet payments` |

---

## Column Rubrics

### proximity_to_transaction (ordinal)
* **1:** Far away from cash exchange. Revenue is based on indirect methods like advertising, affiliate commissions, or delayed sponsorships.
* **3:** Traditional invoicing or net-payment terms. B2B transactions with 30-to-90 day payment delays.
* **5:** Directly in the flow of cash. Mobile money API integrations, telecom billing rails, or direct cash-at-checkout.

### supply_chain_visibility (ordinal)
* **1: Deep Black Hole:** Zero retail terminal tracking. Selling blind to wholesalers (e.g. Kikuubo traders) who handle downstream retail.
* **3: Lagging Visibility:** Relying on monthly or weekly manual sales aggregator audits and distributor stock counts.
* **5: Real-Time Stream:** Live stock velocity and instant shelf visibility verified via digital POS or integrated barcode scanning.

### disintermediation_risk (categorical)
* **Low:** Negligible risk of users bypassing the platform (e.g. payment gateway or API tools where the utility is in the technology itself).
* **Medium:** Moderate risk of bypass, usually prevented by convenience or escrow protection (e.g., telemedicine or specialty prescription delivery).
* **High:** Extreme risk of bypass. Once buyers and service providers make the first contact on the marketplace (e.g. ride-hailing bodas, housekeeping, general handymen), they routinely transact offline to bypass the platform's take-rate.

### distributor_credit_terms (categorical)
* **Cash on Delivery (COD):** The standard zero-credit payment model. Retailers must pay instantly upon delivery.
* **Short-term Credit (1-7 Days):** Short credit windows designed to ease retail cash-flow loops between restocking deliveries.
* **Long-term Credit (30+ Days):** Formal invoice finance. Highly prevalent in corporate Modern Trade (supermarkets), but carries default risks for early-stage B2B players during currency dips.

### last_mile_ownership (categorical)
* **Proprietary Fleet:** The company owns and directly operates the delivery vehicles (trucks, vans, motorcycles), maintaining absolute route-to-market control.
* **Aggregated 3PL:** The company matches orders to a third-party logistics network (e.g. contracting independent boda riders), keeping assets light.
* **Merchant Pickup:** Zero delivery service. Merchants/retailers must travel to the company's central depots or warehouses to collect products.

### retail_distribution_reach (ordinal)
* **1: Localized:** The network reaches less than 100 active retail points of sale.
* **2: Moderate:** The network regularly distributes to 100–1,000 retail outlets.
* **3: Extensive:** The network commands national distribution, active in over 1,000 retail outlets.

