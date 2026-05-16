import igraph as ig
import random
import os
import pickle
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
LAYOUT_PKL = os.path.join(OUT_DIR, "epistemic_layout2.pkl")
PDF_PATH = os.path.join(OUT_DIR, "epistemic_layout_basic2.pdf")

SEED = 42

print("Loading epistemic subgraph...")
g = ig.Graph.Read_Pickle(SUBGRAPH_PKL)

print(f"Graph loaded: {g.vcount()} nodes, {g.ecount()} edges")

print("Computing layout (Fruchterman–Reingold)...")
random.seed(SEED)

layout = g.layout_fruchterman_reingold()
if g.vcount() == 0:
    raise ValueError("Graph is empty — cannot compute layout")

with open(LAYOUT_PKL, "wb") as f:
    pickle.dump(layout, f)

print("Layout saved to:", LAYOUT_PKL)

color_map = {1: "#1f77b4", 2: "#ff7f0e", 3: "#d62728", 5: "#aaaaaa"}
size_map = {1: 10, 2: 6, 3: 3, 5: 2}

g.vs["color"] = [color_map.get(v["step_distance"], "#000000") for v in g.vs]
g.vs["size"] = [size_map.get(v["step_distance"], 2) for v in g.vs]

# Plot to PDF
print("Rendering PDF...")

plot = ig.plot(
    g,
    layout=layout,
    vertex_color=g.vs["color"],
    vertex_size=g.vs["size"],
    vertex_label=None,
    edge_width=0.2,
    edge_color="lightgray",
    edge_arrow_size=0.15,
    bbox=(1200, 1200),
)

ig.plot(
    g,
    PDF_PATH,
    layout=layout,
    vertex_color=g.vs["color"],
    vertex_size=g.vs["size"],
    vertex_label=None,
    edge_width=0.2,
    edge_color="lightgray",
    edge_arrow_size=0.15,
    bbox=(1800, 1800),
    margin=60,
)

print("PDF saved to:", PDF_PATH)

print("\nDone.")
display(plot)
