import igraph as ig
import numpy as np
import pickle
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

GRAPH_PKL = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "9.outputSourceAnalyseEpist_1"
    / "epistemic_subgraph_with_centralities2.pkl"
)
LAYOUT_PKL = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "9.outputSourceAnalyseEpist_1"
    / "epistemic_layout2.pkl"
)
OUT_DIR = (
    BASE_DIR / "edubbaData" / "edubba3_DataSourceFile" / "9.outputSourceAnalyseEpist_1"
)

METRIC = "eigenvector"
# options: in_degree, betweenness, eigenvector, pagerank

PDF_PATH = os.path.join(OUT_DIR, f"epistemic_{METRIC}_heatmap.pdf")

print("Loading graph...")
g = ig.Graph.Read_Pickle(GRAPH_PKL)

print("Loading layout...")
with open(LAYOUT_PKL, "rb") as f:
    layout = pickle.load(f)

print(f"Graph: {g.vcount()} nodes, {g.ecount()} edges")

# Prepare metric
values = np.array(g.vs[METRIC])

# normalization (0–1, clip top 1%)
p99 = np.percentile(values, 99)
clipped = np.clip(values, 0, p99)
norm = (clipped - clipped.min()) / (clipped.max() - clipped.min() + 1e-12)


# Color scale
def heat_color(x):
    r = int(255 * x)
    g = int(255 * (1 - abs(x - 0.5) * 2))
    b = int(255 * (1 - x))
    return f"#{r:02x}{g:02x}{b:02x}"


vertex_colors = [heat_color(x) for x in norm]

# Vertex size (eigenvector ×2, step_1 ×1.8)
vertex_sizes = [
    18 if v["step_distance"] <= 1.0 else (4 + 4 * x) for v, x in zip(g.vs, norm)
]

# Vertex shapes (step_distance == 1 - star)
vertex_shapes = ["star" if v["step_distance"] <= 1.0 else "circle" for v in g.vs]
vertex_frame_width = [2.5 if v["step_distance"] <= 1.0 else 0.5 for v in g.vs]
vertex_frame_color = ["black" if v["step_distance"] <= 1.0 else "gray" for v in g.vs]

# Edge colors (connected to step_distance == 1 -red)
edge_colors = []

for e in g.es:
    s = g.vs[e.source]
    t = g.vs[e.target]

    if s["step_distance"] <= 1.0 or t["step_distance"] <= 1.0:
        edge_colors.append("#cc0000")
    else:
        edge_colors.append("lightgray")

# Plot
print(
    "Nodes with step_distance <= 1:", sum(1 for v in g.vs if v["step_distance"] <= 1.0)
)
print("Rendering plot...")

plot = ig.plot(
    g,
    PDF_PATH,
    layout=layout,
    vertex_color=vertex_colors,
    vertex_size=vertex_sizes,
    vertex_shape=vertex_shapes,
    vertex_frame_width=vertex_frame_width,
    vertex_frame_color=vertex_frame_color,
    vertex_label=None,
    edge_color=edge_colors,
    edge_width=0.3,
    edge_arrow_size=0.12,
    bbox=(900, 900),
    margin=80,
)

print("Saved to:", PDF_PATH)
print("Done.")

display(plot)
