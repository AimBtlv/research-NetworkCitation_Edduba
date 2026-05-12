import igraph as ig
import pandas as pd
import csv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

GRAPH_PKL = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "9.outputSourceAnalyseEpist_1"
    / "citation_graph.pkl"
)
SOURCES_CSV = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "9.outputSourceAnalyseEpist_1"
    / "sources_withAll_steps_v2.csv"
)


OUT_DIR = (
    BASE_DIR / "edubbaData" / "edubba3_DataSourceFile" / "9.outputSourceAnalyseEpist_1"
)
SUBGRAPH_PKL = os.path.join(OUT_DIR, "epistemic_subgraph2.pkl")
SUMMARY_CSV = os.path.join(OUT_DIR, "epistemic_subgraph_summary2.csv")


ALLOWED_STEPS = {1, 2, 3}

print("Loading full graph...")
g = ig.Graph.Read_Pickle(GRAPH_PKL)
print(f"Full graph: {g.vcount()} nodes, {g.ecount()} edges")

print("Loading sources metadata...")
sources = pd.read_csv(SOURCES_ALL, delimiter=";")

# Build step_distance mapping
step_map = {}

for _, row in sources.iterrows():
    sid = str(row["source_id"]).strip()
    step = row.get("step_distance_v2")

    try:
        step = int(step)
    except:
        step = 5  # peripheral by default

    step_map[sid] = step

# Attach step_distance to graph
missing = 0

for v in g.vs:
    sid = v["name"]
    step = step_map.get(sid, 5)  # default = peripheral

    if sid not in step_map:
        missing += 1

    v["step_distance"] = step

print(f"Vertices missing in CSV (assigned to step 5): {missing}")

# Build epistemic subgraph
selected_vertices = [v.index for v in g.vs if v["step_distance"] in ALLOWED_STEPS]

H = g.subgraph(selected_vertices)

print("\nEpistemic subgraph created")
print(f"Included steps: {sorted(ALLOWED_STEPS)}")
print(f"Vertices: {H.vcount()}")
print(f"Edges: {H.ecount()}")

os.makedirs(OUT_DIR, exist_ok=True)
H.write_pickle(SUBGRAPH_PKL)
print("Saved to:", SUBGRAPH_PKL)

# Metrics
components = H.connected_components(mode="weak")

density = H.density()
reciprocity = H.reciprocity()
largest_component = max(components.sizes()) if len(components) > 0 else 0


with open(SUMMARY_CSV, "w", encoding="utf8", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["metric", "value"])
    w.writerow(["nodes", H.vcount()])
    w.writerow(["edges", H.ecount()])
    w.writerow(["density", round(density, 6)])
    w.writerow(["reciprocity", round(reciprocity, 6)])
    w.writerow(["weak_components", len(components)])
    w.writerow(["largest_component", largest_component])

print("\nSubgraph metrics:")
print("Density:", round(density, 6))
print("Reciprocity:", round(reciprocity, 6))
print("Weak components:", len(components))
print("Largest component size:", largest_component)

print("\nDone.")
