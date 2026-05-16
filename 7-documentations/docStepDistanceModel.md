## Step-Distance Model 

## Overview
The Step-Distance Model is a structural framework designed to classify scholarly publications according to their proximity(closenss) to primary archaeological data within a citation network
The model treats academic publications as nodes in a directed graph, where citations represent pathways of knowledge transmission. Using centrality measures and citation patterns, each source is assigned to one of five epistemic steps, ranging from direct archaeological evidence (Step 1) to peripheral or weakly connected scholarship (Step 5).

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
Works that directly belong to primary archaeological reports. Publications that introduce primary empirical material into scholarly discourse.  
This category includes archaeological excavation reports, editions of cuneiform tablets, catalogues, and primary corpora  
**Criteria:** Manually collected data.

#### Step 2 — Mediators
Publications that actively transform empirical material into scholarly interpretation and connect different regions of the knowledge network.  
These sources function as epistemic bridges between data production and theoretical development.
Interpretative works that formulate hypotheses based on primary data.
**Criteria:**
- Betweenness centrality in the **top 15%**
- Cites at least one Step-1 source
This step identifies sources that mediate between data and broader interpretation.

#### Step 3 — Authorities
Publications in which interpretative knowledge becomes stabilized and canonized within the scholarly discourse.  
These works serve as reference points, theoretical frameworks, or standard interpretations to which subsequent research repeatedly refers.
**Criteria:**
- In-degree in the **top 10%**
- Cited by **≥ 2 Step-2 sources**
- Publication age **≥ 10 years**
Authority is defined as stabilized interpretation rather than simple popularity.

#### Step 4 — Mediated (Synthetic) Sources
Secondary literature such as textbooks, handbooks, review articles, and synthetic overviews.  
These publications do not directly engage with primary data but instead integrate multiple stabilized interpretations.
**Criteria:**
- Do **not** cite Step-1 sources
- Cite **≥ 2 Step-3 authorities**
- Out-degree **≥ 2**
These sources integrate established interpretations rather than primary data.

#### Step 5 — Peripheral Sources
All remaining publications that do not satisfy the criteria of Steps 1–4.  
This category includes narrowly cited works and sources whose structural role cannot be reliably inferred from the available data.  
It absorbs both genuine peripheral contributions and artifacts of incomplete bibliographic coverage.  
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

