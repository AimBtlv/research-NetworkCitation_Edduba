import igraph as ig
import csv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

EDGES = ( BASE_DIR/ "edubbaData"/ "edubba3_DataSourceFile" / "7.outputEdges"/ "edges_expanded.csv")
PKL_PATH = (BASE_DIR / "edubbaData" / "edubba3_DataSourceFile" / "8.outputAnalize_BuildGraph")
GRAPH_PKL = os.path.join(PKL_PATH, "citation_graph.pkl")
SUMMARY_CSV = os.path.join(PKL_PATH, "citation_graph.csv")

edges = []

with open(EDGES, encoding="utf8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for r in reader:
        edges.append((r["citing"], r["cited"]))

g = ig.Graph.TupleList(edges, directed=True)

print("Graph created")
print("Vertices:", g.vcount())
print("Edges:", g.ecount())

# save for reuse
g.write_pickle(GRAPH_PKL)

with open(SUMMARY_CSV, "w", encoding="utf8", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["metric", "value"])
    w.writerow(["nodes", g.vcount()])
    w.writerow(["edges", g.ecount()])
    w.writerow(["density", g.density()])
    w.writerow(["reciprocity", g.reciprocity()])
    w.writerow(["weak_components", len(g.connected_components(mode="weak"))])

components = g.connected_components(mode="weak")

print("Density:", g.density())
print("Reciprocity:", g.reciprocity())
print("Weakly connected components:", len(components))
print("Largest component size:", max(components.sizes()))
