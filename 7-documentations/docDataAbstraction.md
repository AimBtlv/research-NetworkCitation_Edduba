## Data Abstraction

The dataset is a directed network (graph) in which nodes represent individual academic publications and directed edges represent citation relationships. This is a relational dataset of type items + links, where the analytical interest lies not in the attributes of individual items in isolation, but in the topology of their connections.

---
**Dataset scale:**  
**Full corpus:** 2,103 nodes, 2,524 edges (density = 0.0006) 
**Epistemic subgraph (Steps 1–3, top 15% betweenness filter):** 400 nodes, 841 edges (density = 0.0053)  

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
