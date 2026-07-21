# Academic Literature Review: East African Startup Survival and Platform Economics

This document compiles the theoretical and empirical academic frameworks that anchor our quantitative business model analysis. It transitions our research design from standard commercial insights to a rigorous, **DeepMind Business Development Lab style framework**.

---

## 1. Survival Analysis & Firm Duration Theory

To evaluate startup lifespans, we draw on **Industrial Organization Economics** and **Duration Modeling** frameworks. 

### Core Concepts
* **Right-Censoring:** Traditional classification models (e.g., standard logistic regression predicting bankruptcy) suffer from truncation bias because they treat currently active startups the same as long-term survivors. We resolve this by using the non-parametric **Kaplan-Meier estimator** to compute time-to-event survival curves.
* **Proportional Hazards:** To evaluate covariate effects (e.g., funding size, cash proximity, regulatory barriers) on the risk of shutdown, we leverage the hazard rate concept:
  $$\lambda(t | X) = \lambda_0(t) \exp(\beta X)$$
  where $\lambda_0(t)$ is the baseline hazard rate and $X$ represents our business model features.

### Academic Anchors
* **Audretsch, D. B. (1991).** *"New-firm survival and the technological regime."* *Review of Economic Studies*.
  * *Application:* Establishes that firm survival is driven by post-entry adjustment and learning rather than initial scale, justifying our inclusion of **historical pivot counts** as a covariate.
* **Mata, J., & Portugal, P. (1994).** *"Life duration of new firms."* *Journal of Industrial Economics*.
  * *Application:* Proves that financing structures and industry barriers significantly shift the shape of survival curves over a 10-year horizon.

---

## 2. Bilateral Matching Markets & Platform Disintermediation

A core focus of our research is why marketplaces fail to scale and retain users in developing markets. We model this using **Platform Disintermediation** and **Leakage Theory**.

### Core Concepts
* **Disintermediation / Leakage:** In a bilateral matching market (buyers and sellers), users coordinate to take subsequent transactions off-platform to bypass commission fees (take-rates).
* **Mitigation Mechanics:** Platforms can combat disintermediation through:
  1. *Pricing Remedies:* Front-loaded transaction pricing or transition to subscription models.
  2. *Operational Bundling:* Providing ongoing value that cannot be replicated offline (e.g., smartphone asset locking, escrow protection, real-time supply chain visibility).

### Academic Anchors
* **Sekar, S., & Siddiq, A. (2023).** *"Platform Disintermediation: Information Effects and Pricing Remedies."* *Operations Research*.
  * *Application:* Models how information asymmetry and fee structures drive users offline, supporting our finding that **High Disintermediation Risk** causes annual customer retention to collapse to **35%** for matching-only platforms.
* **Rhodes, A., Zhou, J., & Zhu, M. (2021).** *"Platform Disintermediation with Repeated Transactions."* *Management Science*.
  * *Application:* Explores how repeated interactions lead to transaction leakage and proves that platforms must bundle transactional services with physical utilities to retain users.

---

## 3. Transaction Cost Economics (TCE) & Resource-Based View (RBV)

To explain why asset-heavy physical manufacturers outlive asset-light software platforms in East Africa, we integrate **Transaction Cost Economics** and the **Resource-Based View (RBV)**.

### Core Concepts
* **The Make-or-Buy Decision:** In fragmented markets with high institutional voids (e.g., logistics unreliability, cold-chain breakdowns), the transaction costs of outsourcing physical delivery are higher than the internal coordination costs of owning assets.
* **VRIO Moats:** Physical distribution assets (e.g., Jesa's cold chain vans, Mukwano's depot networks) are Rare, Imperfectly Imitable, and Organized (VRIO), creating a sustainable competitive advantage compared to replicable software code.

### Academic Anchors
* **Coase, R. H. (1937).** *"The Nature of the Firm."* *Economica*.
  * *Application:* Explains why regional firms integrate vertically (going asset-heavy) to bypass highly fragmented, high-friction third-party logistics markets.
* **Barney, J. (1991).** *"Firm resources and sustained competitive advantage."* *Journal of Management*.
  * *Application:* Grounding our strategic matrix: physical RTM assets represent path-dependent, physical-capital resources that prevent competitor replication and secure shelf visibility.
