## Data Abstraction

The dataset is a directed network (graph) in which nodes represent individual academic publications and directed edges represent citation relationships. This is a relational dataset of type items + links, where the analytical interest lies not in the attributes of individual items in isolation, but in the topology of their connections.

---
***Dataset scale:***  
**Full corpus:** 2,103 nodes, 2,524 edges (density = 0.0006) 
**Epistemic subgraph (Steps 1–3, top 15% betweenness filter):** 400 nodes, 841 edges (density = 0.0053).  

### Node

--- 
Each publication carries: 
| Attribute | Data Type | Description |
|---|---|---|
| `source_id` | Categorical (nominal) | Unique DOI-based identifier |
| `step_distance_v2` | Ordinal (1–5) | Epistemic role classification |
| `in_degree` | Quantitative (ratio) | Number of incoming citations |
| `betweenness` | Quantitative (ratio) | Structural bridge position |
| `eigenvector` | Quantitative (ratio) | Integration into densely cited clusters |
| `pagerank` | Quantitative (ratio) | Random-walk reachability |
| `community` | Categorical (nominal) | Edge-betweenness cluster membership |
| `reliable_source` | Binary (0/1) | Satisfies Trust Triangle criteria |

### Edges
---

| Attribute | Data Type | Description |
|---|---|---|
| `citing` | Categorical (nominal) | Source ID of the citing publication (edge origin) |
| `cited` | Categorical (nominal) | Source ID of the cited publication (edge target) |
| `matched` | Binary (Boolean) | Whether the citation was successfully matched to a known source ID via AnyStyle extraction |
| `direction` | Implicit (directed) | Edge is directed: `citing → cited`, encoding the flow of knowledge from a newer work toward an older one |
| `step-crossing type` | Derived (ordinal pair) | The epistemic layer the edge crosses, defined by the `step_distance` of the source and target nodes (e.g. Step 2 → Step 1 = empirical anchoring; Step 3 → Step 3 = intra-authority reinforcement) |
| `triangle membership` | Derived (binary) | Whether the edge is part of a closed trust triangle — computed in H5 analysis |

**Role of edges in the analysis:**
An edge `A → B` means *A cites B*, i.e. knowledge flows from B toward A.
Edges are not weighted by frequency — each citation pair is recorded once.
The direction encodes epistemic dependency: the citing work relies on the cited work as a source of evidence, interpretation, or authority.
The structural significance of an edge is determined not by its own attributes but by the position of the nodes it connects in the **step-distance hierarchy**.
### Analytical Abstraction Layer
The Step-Distance Model functions as a structural abstraction layer that transforms citation-network relationships into interpretable epistemic roles.
#### Step-Distance Hierarchy

The raw citation dataset (2,103 nodes, 2,524 edges) does not carry explicit labels about the epistemic role of each publication. To move beyond simple citation counts, an additional layer of abstraction was applied: each node was assigned a `step_distance` value (1–5) representing its **functional distance from primary empirical data**.

This transformation converts an unstructured bibliographic network into a **stratified epistemic graph**, where each layer corresponds to a distinct knowledge-production role:

| Step | Role | Epistemic Function | Assignment Method |
|---|---|---|---|
| **1** | Direct Sources | Introduce primary empirical material (excavation reports, cuneiform editions, primary corpora) into scholarly discourse | Manually collected |
| **2** | Mediators | Transform empirical material into scholarly interpretation; function as bridges between data production and theoretical development | Betweenness ≥ top 15% AND cites ≥ 1 Step 1 node |
| **3** | Discursive Authorities | Stabilized and canonized interpretations; repeated reference points and standard theoretical frameworks | In-degree ≥ top 10% AND cited by ≥ 2 Step 2 nodes AND age ≥ 10 years |
| **4** | Mediated Sources | Secondary syntheses (textbooks, handbooks, reviews) that integrate stabilized interpretations without engaging primary data | Does not cite Step 1 AND cites ≥ 2 Step 3 nodes AND out-degree ≥ 2 |
| **5** | Peripheral / Noise | All remaining nodes — narrowly cited works and artifacts of incomplete bibliographic coverage | All others |

**Why this abstraction matters:**
The step-distance model shifts the analytical frame from *popularity* (how many times a source is cited) to *epistemic proximity* (how close a source is to verifiable primary data). This distinction is the analytical core of RQ2 and hypotheses H2–H5: it allows the study to ask not just *which sources are central*, but *where in the knowledge chain does centrality emerge*.

The model infers epistemic roles **structurally**, from citation graph metrics, rather than through semantic or content-based evaluation. Thresholds (top 15%, top 10%, age ≥ 10 years) were chosen to balance interpretability and robustness in a sparse citation network, and validated through sensitivity analysis (H3).