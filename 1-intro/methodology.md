## Methodology 
**Network Analysis***

#### Analytical Pipeline
---
The analytical workflow follows a sequential hypothesis-driven design, structured as a pipeline of five stages: (1) graph construction, (2) centrality computation, (3) subgraph extraction, (4) community detection, and (5) hypothesis testing. Each stage produces outputs that serve as inputs for the next, forming a reproducible analytical chain.
#### Graph Construction
---
A directed citation graph was constructed using igraph (Python). The full corpus yields a graph with 2,050 nodes and 2,524 directed edges, with a global density of 0.0006 and reciprocity ≈ 0.0008 — indicating a nearly acyclic structure consistent with one-directional citation flow. The graph decomposes into two weakly connected components, confirming structural fragmentation at the macro level.
Due to extreme sparsity, a subgraph was extracted for detailed analysis by filtering nodes with betweenness centrality in the top 15% (N = 400, 841 edges, density = 0.0053). This subgraph preserves the structurally active portion of the network while removing peripheral nodes that contribute no relational signal.
#### Centrality Measures
---
**In-degree centrality** counts the number of incoming citation edges for each node. In a citation network, high in-degree indicates that a source has been adopted as a reference point by many other works- a proxy for canonisation.   
**Betweenness centrality** measures the fraction of shortest paths between all pairs of nodes that pass through a given node. High betweenness identifies structural brokers: nodes whose removal would disconnect or restructure large portions of the graph. In the epistemic context of this study, high betweenness corresponds to interpretive mediation — the transmission of empirical findings through the citation chain.   
**Eigenvector centrality** assigns each node a score proportional to the sum of the scores of its neighbours. Unlike in-degree, eigenvector centrality rewards embeddedness in densely interconnected, mutually reinforcing clusters. In a knowledge network, it approximates "discursive authority" — the influence of a work within the epistemic core.   
**PageRank** is a variant of eigenvector centrality that accounts for the direction and weight of edges, originally designed for web link analysis (Page et al., 1999). It was computed as a supplementary measure to cross-validate eigenvector findings.
#### Community Detection
---
Community structure was detected using the Louvain algorithm, which optimises modularity to identify groups of nodes with higher internal connectivity than expected under a random graph model. The detection was applied to the epistemic subgraph (N = 400) to identify epistemic clusters and examine whether community membership correlates with step-distance roles.
#### Sensitivity Analysis
---
To assess whether the bottleneck structure identified in H3 is a genuine structural property rather than an artefact of the betweenness filter used to define Step 2, a sensitivity analysis was performed. The betweenness criterion was relaxed and Step 2 membership was recomputed. This test verified that the set of nodes citing Step 1 sources remains stable regardless of the filter threshold.
