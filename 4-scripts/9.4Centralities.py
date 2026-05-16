import igraph as ig
import pandas as pd
import numpy as np
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SUBGRAPH_PKL = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "9.outputSourceAnalyseEpist_1"
    / "epistemic_subgraph2.pkl"
)
OUT_DIR = (
    BASE_DIR / "edubbaData" / "edubba3_DataSourceFile" / "9.outputSourceAnalyseEpist_1"
)
CSV_PATH = os.path.join(OUT_DIR, "epistemic_centralities2.csv")
GRAPH_OUT_PKL = os.path.join(OUT_DIR, "epistemic_subgraph_with_centralities2.pkl")

os.makedirs(OUT_DIR, exist_ok=True)

print("Loading epistemic subgraph...")
g = ig.Graph.Read_Pickle(SUBGRAPH_PKL)

print(f"Graph: {g.vcount()} nodes, {g.ecount()} edges")

# Compute centralities
print("Computing centralities...")

in_degree = np.array(g.indegree())
betweenness = np.array(g.betweenness(directed=True, cutoff=5))
eigenvector = np.array(g.eigenvector_centrality(directed=True, scale=True))
pagerank = np.array(g.pagerank(directed=True))

# attach to graph
g.vs["in_degree"] = in_degree.tolist()
g.vs["betweenness"] = betweenness.tolist()
g.vs["eigenvector"] = eigenvector.tolist()
g.vs["pagerank"] = pagerank.tolist()

# Save CSV table
df = pd.DataFrame(
    {
        "source_id": g.vs["name"],
        "step_distance": g.vs["step_distance"],
        "in_degree": in_degree,
        "betweenness": betweenness,
        "eigenvector": eigenvector,
        "pagerank": pagerank,
    }
)

df.to_csv(CSV_PATH, sep=";", index=False)

print("Centralities saved to:", CSV_PATH)

g.write_pickle(GRAPH_OUT_PKL)
print("Graph with centralities saved to:", GRAPH_OUT_PKL)


# Print TOP-10 for each metric
def print_top(metric_name, values):
    print(f"\nTOP-10 by {metric_name}")
    print("-" * 40)
    idx = np.argsort(values)[::-1][:10]
    for i in idx:
        print(f"{g.vs[i]['name']:40s}  {values[i]:.6f}")


print_top("in-degree (canonization)", in_degree)
print_top("betweenness (mediation)", betweenness)
print_top("eigenvector (epistemic core)", eigenvector)
print_top("pagerank (prestige)", pagerank)

print("\nDone.")
