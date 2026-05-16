import igraph as ig
import numpy as np
import pandas as pd
import pickle
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

GRAPH_PKL = ( BASE_DIR/ "edubbaData"/ "edubba3_DataSourceFile" /"10.outputSourceAnalyse_2"/"epistemic_subgraph_with_centralities2.pkl")
LAYOUT_PKL = ( BASE_DIR/ "edubbaData"/ "edubba3_DataSourceFile" /"10.outputSourceAnalyse_2"/"epistemic_layout2.pkl")
CSV_PATH = ( BASE_DIR/ "edubbaData"/ "edubba3_DataSourceFile" /"10.outputSourceAnalyse_2"/"sources_withAll_steps_v2.csv")
OUT_PDF = ( BASE_DIR/ "edubbaData"/ "edubba3_DataSourceFile" /"10.outputSourceAnalyse_2"/"reliable_sources_graph4.pdf")

INDEGREE_PERCENTILE = 90   # threshold for "high in-degree"


print("Loading graph...")
g = ig.Graph.Read_Pickle(GRAPH_PKL)

print("Loading layout...")
with open(LAYOUT_PKL, "rb") as f:
    layout = pickle.load(f)

print("Loading CSV...")
df = pd.read_csv(CSV_PATH, sep=";")

# STEP 1 NODES
step1_nodes = {
    v.index for v in g.vs
    if v.attributes().get("step_distance", None) == 1
}

print(f"Step 1 nodes: {len(step1_nodes)}")

# HIGH IN-DEGREE NODES
indeg = np.array(g.indegree())
indeg_thr = np.percentile(indeg, INDEGREE_PERCENTILE)

high_indeg_nodes = {
    v.index for v in g.vs
    if indeg[v.index] >= indeg_thr
}

print(f"High in-degree threshold: {indeg_thr}")
print(f"High in-degree nodes: {len(high_indeg_nodes)}")

# RELIABLE SOURCES
reliable_sources = set()

for a in g.vs:
    a_id = a.index
    if a_id in step1_nodes:
        continue
    if a_id not in high_indeg_nodes:
        continue

    # Step 1 neighbors of A
    a_step1 = set(g.successors(a_id)) & step1_nodes
    if not a_step1:
        continue

    # Candidate B nodes
    for b_id in high_indeg_nodes:
        if b_id == a_id:
            continue

        # B must cite the SAME Step 1
        b_step1 = set(g.successors(b_id)) & a_step1
        if not b_step1:
            continue

        # A ↔ B connection
        if g.are_connected(a_id, b_id) or g.are_connected(b_id, a_id):
            reliable_sources.add(a_id)
            reliable_sources.add(b_id)
            break

print(f"Reliable sources found: {len(reliable_sources)}")

# CONSOLE OUTPUT
print("\nReliable source IDs:")
for v in list(reliable_sources)[:20]:
    print(" -", g.vs[v]["name"])

# ADD COLUMN TO CSV
df["reliable_source"] = 0

# map vertex name -> vertex index
name_to_index = {
    g.vs[v]["name"]: v
    for v in range(g.vcount())
}

df["reliable_source"] = df["source_id"].apply(
    lambda x: 1 if name_to_index.get(x, -1) in reliable_sources else 0
)

df.to_csv(CSV_PATH, index=False, sep=";")
print("CSV updated with reliable_source column")

# TRIANGLE EDGES (for visualization)
triangle_edges = set()

for v in reliable_sources:
    # neighbors of reliable source
    neigh = set(g.neighbors(v, mode="ALL"))

    # high in-degree neighbors
    trusted_neighbors = neigh & high_indeg_nodes

    # step 1 neighbors
    step1_neighbors = neigh & step1_nodes

    # triangle exists if both are non-empty
    if not trusted_neighbors or not step1_neighbors:
        continue

    # mark edges forming the triangle
    for u in trusted_neighbors:
        eid = g.get_eid(v, u, directed=False, error=False)
        if eid != -1:
            triangle_edges.add(eid)

    for s in step1_neighbors:
        eid = g.get_eid(v, s, directed=False, error=False)
        if eid != -1:
            triangle_edges.add(eid)

# VISUALIZATION
vertex_colors = []
vertex_sizes = []

for v in g.vs:
    if v.index in reliable_sources:
        vertex_colors.append("#d62728")   # red
        vertex_sizes.append(16)
    elif v.index in step1_nodes:
        vertex_colors.append("#1f77b4")   # blue
        vertex_sizes.append(10)
    else:
        vertex_colors.append("lightgray")
        vertex_sizes.append(4)


edge_colors = []
edge_widths = []

for e in g.es:
    if e.index in triangle_edges:
        edge_colors.append("#f28e8e")   # soft red
        edge_widths.append(1.2)
    else:
        edge_colors.append("#d0d0d0")   # light gray
        edge_widths.append(0.3)

print("Rendering PDF...")

plot = ig.plot(
    g,
    OUT_PDF,
    layout=layout,
    vertex_color=vertex_colors,
    vertex_size=vertex_sizes,
    vertex_label=None,
    edge_color=edge_colors,
    edge_width=edge_widths,
    bbox=(1000, 1000),
    margin=80
)

print("Saved visualization to:", OUT_PDF)
print("DONE.")
display(plot)