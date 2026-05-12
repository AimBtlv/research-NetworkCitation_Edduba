import igraph as ig
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

GRAPH_PKL = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "10.outputSourceAnalyse_2"
    / "epistemic_subgraph_with_centralities2.pkl"
)
LAYOUT_PKL = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "10.outputSourceAnalyse_2"
    / "epistemic_layout2.pkl"
)
CSV_PATH = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "10.outputSourceAnalyse_2"
    / "sources_withAll_steps_v2.csv"
)
OUT_PDF = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "10.outputSourceAnalyse_2"
    / "reliable_sources_graph3.pdf"
)

INDEGREE_PERCENTILE = 90

# STEP 1 NODES
step1_nodes = {v.index for v in g.vs if v["step_distance"] == 1}

# IN-DEGREE
indeg = np.array(g.indegree())
indeg_thr = np.percentile(indeg, INDEGREE_PERCENTILE)
high_indeg_nodes = {v.index for v in g.vs if indeg[v.index] >= indeg_thr}

# RELIABLE SOURCES (STRICT CLOSED TRIANGLES)
# ONE TRIANGLE PER SOURCE
reliable_sources = set()
triangle_edges = set()
top10_triangle_nodes = set()  # top-10 that actually have triangles

for a in g.vs:
    a_id = a.index

    if a_id in step1_nodes or a_id not in high_indeg_nodes:
        continue

    a_step1 = set(g.successors(a_id)) & step1_nodes
    if not a_step1:
        continue

    for b_id in high_indeg_nodes:
        if b_id == a_id:
            continue

        b_step1 = set(g.successors(b_id)) & a_step1
        if not b_step1:
            continue

        if g.are_adjacent(a_id, b_id) or g.are_adjacent(b_id, a_id):

            reliable_sources.add(a_id)
            reliable_sources.add(b_id)

            s = next(iter(b_step1))
            for x, y in [(a_id, b_id), (a_id, s), (b_id, s)]:
                eid = g.get_eid(x, y, directed=False, error=False)
                if eid != -1:
                    triangle_edges.add(eid)

            break

# TOP 10 RELIABILITY CANDIDATES (SOFT SCORE)
scores = []

for v in g.vs:
    vid = v.index
    if vid in step1_nodes:
        continue

    score = 0
    a_step1 = set(g.successors(vid)) & step1_nodes
    if a_step1:
        score += 1
    if vid in high_indeg_nodes:
        score += 1

    for u in high_indeg_nodes:
        if u == vid:
            continue
        if g.are_adjacent(vid, u) or g.are_adjacent(u, vid):
            if set(g.successors(u)) & a_step1:
                score += 1
                break

    scores.append((vid, score, indeg[vid]))

top_10_candidates = [
    vid
    for vid, s, d in sorted(scores, key=lambda x: (x[1], x[2]), reverse=True)
    if s >= 2
][:10]

# TRIANGLES FOR TOP-10 (ONLY IF THEY EXIST)
for a_id in top_10_candidates:
    if a_id in reliable_sources:
        continue

    a_step1 = set(g.successors(a_id)) & step1_nodes
    if not a_step1:
        continue

    for b_id in high_indeg_nodes:
        if b_id == a_id:
            continue

        b_step1 = set(g.successors(b_id)) & a_step1
        if not b_step1:
            continue

        if g.are_adjacent(a_id, b_id) or g.are_adjacent(b_id, a_id):

            top10_triangle_nodes.add(a_id)

            s = next(iter(b_step1))
            for x, y in [(a_id, b_id), (a_id, s), (b_id, s)]:
                eid = g.get_eid(x, y, directed=False, error=False)
                if eid != -1:
                    triangle_edges.add(eid)

            break  # ONE triangle per top-10

print("\nMOST RELIABLE SOURCES:")
for v in reliable_sources:
    print(" -", g.vs[v]["name"])

print("\nTOP 10 RELIABILITY CANDIDATES:")
for v in top_10_candidates:
    print(" -", g.vs[v]["name"])

# VISUAL PARAMETERS
vertex_colors = []
vertex_sizes = []
vertex_labels = []
vertex_label_sizes = []
vertex_label_colors = []

for v in g.vs:
    vid = v.index

    if vid in reliable_sources:
        vertex_colors.append("#d62728")  # red
        vertex_sizes.append(18)
        vertex_labels.append(v["name"])
        vertex_label_sizes.append(10)
        vertex_label_colors.append("#d62728")

    elif vid in top_10_candidates:
        vertex_colors.append("#ffcc00")  # yellow
        vertex_sizes.append(14)
        vertex_labels.append(v["name"])
        vertex_label_sizes.append(9)
        vertex_label_colors.append("#b58900")

    elif vid in step1_nodes:
        vertex_colors.append("#1f77b4")  # blue
        vertex_sizes.append(10)
        vertex_labels.append("")
        vertex_label_sizes.append(0)
        vertex_label_colors.append("black")

    else:
        vertex_colors.append("lightgray")
        vertex_sizes.append(4)
        vertex_labels.append("")
        vertex_label_sizes.append(0)
        vertex_label_colors.append("black")

# EDGES (ONLY REAL TRIANGLES)
edge_colors = []
edge_widths = []

for e in g.es:
    if e.index in triangle_edges:
        edge_colors.append("#f28e8e")
        edge_widths.append(1.6)
    else:
        edge_colors.append("#e0e0e0")
        edge_widths.append(0.25)

plot = ig.plot(
    g,
    OUT_PDF,
    layout=layout,
    vertex_color=vertex_colors,
    vertex_size=vertex_sizes,
    vertex_label=vertex_labels,
    vertex_label_size=vertex_label_sizes,
    vertex_label_color=vertex_label_colors,
    edge_color=edge_colors,
    edge_width=edge_widths,
    bbox=(1200, 1200),
    margin=90,
)

print("\nSaved visualization to:", OUT_PDF)
display(plot)
