import igraph as ig
import pandas as pd
import pickle
import os
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

GRAPH_PKL = ( BASE_DIR/ "edubbaData"/ "edubba3_DataSourceFile" /"9.outputSourceAnalyseEpist_1"/"epistemic_subgraph_with_centralities2.pkl")
LAYOUT_PKL =  ( BASE_DIR/ "edubbaData"/ "edubba3_DataSourceFile" /"9.outputSourceAnalyseEpist_1"/"epistemic_layout2.pkl")
OUT_DIR = ( BASE_DIR/ "edubbaData"/ "edubba3_DataSourceFile" /"9.outputSourceAnalyseEpist_1")

CSV_PATH = os.path.join(OUT_DIR, "epistemic_communities2.csv")
GRAPH_OUT_PKL = os.path.join(OUT_DIR, "epistemic_subgraph_with_communities2.pkl")
PDF_PATH = os.path.join(OUT_DIR, "epistemic_communities2.pdf")

os.makedirs(OUT_DIR, exist_ok=True)

# Load data
print("Loading graph...")
g = ig.Graph.Read_Pickle(GRAPH_PKL)

print("Loading layout...")
with open(LAYOUT_PKL, "rb") as f:
    layout = pickle.load(f)

print(f"Graph: {g.vcount()} nodes, {g.ecount()} edges")

# Community detection
print("Running community_edge_betweenness (this may take time)...")

communities = g.community_edge_betweenness(directed=True)
clusters = communities.as_clustering()

print(f"Detected communities: {len(clusters)}")

# Attach to graph
g.vs["community"] = clusters.membership
g.write_pickle(GRAPH_OUT_PKL)
print("Graph with communities saved to:", GRAPH_OUT_PKL)

df = pd.DataFrame({
    "source_id": g.vs["name"],
    "step_distance": g.vs["step_distance"],
    "community": clusters.membership,
    "in_degree": g.vs["in_degree"],
    "betweenness": g.vs["betweenness"],
    "eigenvector": g.vs["eigenvector"],
    "pagerank": g.vs["pagerank"]
})

df.to_csv(CSV_PATH, sep=";", index=False)
print("Communities table saved to:", CSV_PATH)

sizes = Counter(clusters.membership)

print("\nTop 10 communities by size:")
print("-" * 40)

for cid, size in sizes.most_common(10):
    print(f"Community {cid:3d}: {size} nodes")

# Visualization
print("\nRendering visualization...")

palette = ig.drawing.colors.ClusterColoringPalette(len(clusters))
g.vs["color"] = [palette[c] for c in clusters.membership]

plot = ig.plot(
    g,
    layout=layout,
    vertex_color=g.vs["color"],
    vertex_size=4,
    vertex_label=None,
    edge_color="lightgray",
    edge_arrow_size=0.12,
    bbox=(900, 900),
)
ig.plot(
    g,
    PDF_PATH,
    layout=layout,
    vertex_color=g.vs["color"],
    vertex_size=4,
    vertex_label=None,
    edge_color="lightgray",
    edge_width=0.15,
    edge_arrow_size=0.08,
    bbox=(2000, 2000),
    margin=80
)

print("Community plot saved to:", PDF_PATH)

print("\nDone.")
display(plot)