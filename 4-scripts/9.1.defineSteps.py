import igraph as ig
import pandas as pd
import numpy as np
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
    / "sources_all_with_steps.csv"
)
PKL_PATH = (
    BASE_DIR / "edubbaData" / "edubba3_DataSourceFile" / "9.outputSourceAnalyseEpist_1"
)
OUT_CSV = os.path.join(PKL_PATH, "sources_withAll_steps_v2.csv")

BETWEENNESS_TOP_PERCENT = 85  # top 15%
INDEGREE_AUTHORITY_PERCENT = 90  # top 10%

INDEGREE_MID_LOW_PERCENT = 20
INDEGREE_MID_HIGH_PERCENT = 80

MIN_STEP1_FOR_MEDIATOR = 1
MIN_STEP2_FOR_AUTHORITY = 2
MIN_STEP3_FOR_MEDIATED = 1

MIN_OUT_MEDIATED = 2

CURRENT_YEAR = 2025
MIN_AUTHORITY_AGE = 10

print("Loading graph...")
g = ig.Graph.Read_Pickle(GRAPH_PKL)

print("Loading sources...")
df = pd.read_csv(SOURCES_CSV, delimiter=";")

# map source_id → vertex index
name_to_idx = {v["name"]: v.index for v in g.vs}

# Step containers
step = {}

# STEP 1 — from CSV (ground truth)
for _, row in df.iterrows():
    sid = str(row["source_id"]).strip()
    if row.get("step_distance") == 1 and sid in name_to_idx:
        step[sid] = 1

step1_nodes = {name_to_idx[s] for s in step}

print(f"Step1 loaded: {len(step1_nodes)} nodes")

# Centralities
print("Computing centralities...")

bet = np.array(g.betweenness(directed=True))
indeg = np.array(g.indegree())
outdeg = np.array(g.outdegree())

bet_thr = np.percentile(bet, BETWEENNESS_TOP_PERCENT)
indeg_auth_thr = np.percentile(indeg, INDEGREE_AUTHORITY_PERCENT)

indeg_mid_low = np.percentile(indeg, INDEGREE_MID_LOW_PERCENT)
indeg_mid_high = np.percentile(indeg, INDEGREE_MID_HIGH_PERCENT)

# STEP 2 — Mediators
step2_nodes = set()

for v in g.vs:
    idx = v.index
    sid = v["name"]

    if idx in step1_nodes:
        continue

    if bet[idx] < bet_thr:
        continue

    cited_step1 = sum(1 for t in g.successors(idx) if t in step1_nodes)

    if cited_step1 >= 1:
        step2_nodes.add(idx)
        step[v["name"]] = 2

print(f"Step2 (mediators): {len(step2_nodes)}")

# removeStep_2's filters(betweenness):Check if any more edge between step_1 and step_3
step2_loose = set()

for v in g.vs:
    if v.index in step1_nodes:
        continue

    # does v cite step1 at least once?
    if any(t in step1_nodes for t in g.successors(v.index)):
        step2_loose.add(v.index)

print(f"Step2 (mediators, no_betweenness filter): {len(step2_loose)}")

# STEP 3 — Authorities
step3_nodes = set()

year_map = dict(zip(df["source_id"].astype(str), df.get("year", [])))

for v in g.vs:
    idx = v.index
    sid = v["name"]

    if idx in step1_nodes or idx in step2_nodes:
        continue

    if indeg[idx] < indeg_auth_thr:
        continue

    cited_by_step2 = sum(1 for s in g.predecessors(idx) if s in step2_nodes)

    if cited_by_step2 < MIN_STEP2_FOR_AUTHORITY:
        continue

    year = year_map.get(sid)

    try:
        age = CURRENT_YEAR - int(year)
    except:
        continue

    if age >= MIN_AUTHORITY_AGE:
        step3_nodes.add(idx)
        step[sid] = 3

print(f"Step3 (authorities): {len(step3_nodes)}")

# STEP 4 — Mediated sources
step4_nodes = set()

for v in g.vs:
    idx = v.index
    sid = v["name"]

    if idx in step1_nodes or idx in step2_nodes or idx in step3_nodes:
        continue

    cites_step1 = any(t in step1_nodes for t in g.successors(idx))
    cites_step3 = sum(1 for t in g.successors(idx) if t in step3_nodes)

    if cites_step1:
        continue

    if cites_step3 >= MIN_STEP3_FOR_MEDIATED and outdeg[idx] >= MIN_OUT_MEDIATED:
        step4_nodes.add(idx)
        step[sid] = 4

print(f"Step4 (mediated): {len(step4_nodes)}")

# STEP 5 — Peripheral / noise
for v in g.vs:
    sid = v["name"]
    if sid not in step:
        step[sid] = 5

df["step_distance_v2"] = df["source_id"].astype(str).map(step)

df.to_csv(OUT_CSV, sep=";", index=False)

print("Saved:", OUT_CSV)

print("\nFinal distribution:")
print(df["step_distance_v2"].value_counts().sort_index())
