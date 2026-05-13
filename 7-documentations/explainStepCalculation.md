## Step Distance Calculation 

## Overview

---
## Data
- **Anchor corpus:** ~150 core scholarly works  
- **Expanded corpus:** 2,103 sources (via snowball citation expansion)  
- **Primary sources:** archaeological excavation reports  
- **Format:** CSV (nodes, edges, metadata)

---
###  Step-Distance Classification
Each source is assigned a `step_distance` representing its distance to primary sources. How close source to the facts described in primery sources
>Primary Sources in this analyses  sources are closest to fact-based primary data such as i.e. archaeological reports. 

#### Step 1 — Direct Sources
Works that directly belong to primary archaeological reports.  
**Criteria:** Manually collected data.

#### Step 2 — Mediators
Interpretative works that formulate hypotheses based on primary data.
**Criteria:**
- Betweenness centrality in the **top 15%**
- Cites at least one Step-1 source
This step identifies sources that mediate between data and broader interpretation.

#### Step 3 — Authorities
Canonical works whose interpretations have stabilized.
**Criteria:**
- In-degree in the **top 10%**
- Cited by **≥ 2 Step-2 sources**
- Publication age **≥ 10 years**
Authority is defined as stabilized interpretation rather than simple popularity.

#### Step 4 — Mediated (Synthetic) Sources
Secondary syntheses such as textbooks and review articles.
**Criteria:**
- Do **not** cite Step-1 sources
- Cite **≥ 2 Step-3 authorities**
- Out-degree **≥ 2**
These sources integrate established interpretations rather than primary data.

#### Step 5 — Peripheral Sources
All remaining sources that do not meet the criteria above.  
This category reflects both peripheral scholarship and corpus incompleteness and prevents artificial inflation of centrality measures.

---

## Network Analysis
- Directed citation graph construction  
- Centrality measures (in-degree, betweenness)  
- Step-distance assignment  
- Closed trust triangle detection  
- Subgraph extraction and visualization  

---

## Output
- CSV files with epistemic roles and centrality metrics  
- Network visualizations highlighting closed trust triangles  
- Console output listing most reliable and top-ranked sources  

---

## Notes
This model infers epistemic roles structurally rather than through semantic or content-based evaluation.  
Thresholds are chosen to balance interpretability and robustness in a sparse citation network.

