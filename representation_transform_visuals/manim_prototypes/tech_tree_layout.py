from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MERMAID = ROOT / "drafts" / "tech_tree_lineage.mmd"
DEFAULT_OUT = ROOT / "manim_prototypes" / "out" / "tech_tree_coords.json"


NODE_ID = r"[A-Za-z0-9_]+"
NODE_WITH_LABEL = rf"(?P<id>{NODE_ID})(?:\[(?P<quote>[\"']?)(?P<label>[^\]]*?)(?P=quote)\])?"
NODE_RE = re.compile(rf"^\s*{NODE_WITH_LABEL}\s*$")
EDGE_RE = re.compile(
    rf"^\s*(?P<src>{NODE_ID})(?:\[(?P<src_quote>[\"']?)(?P<src_label>[^\]]*?)(?P=src_quote)\])?"
    rf"\s*(?:-->|--\|[^|]*\|>|-\.\->|-\.\s*[^-]*\s*\.-?>)\s*"
    rf"(?P<dst>{NODE_ID})(?:\[(?P<dst_quote>[\"']?)(?P<dst_label>[^\]]*?)(?P=dst_quote)\])?"
)


def parse_mermaid(path: Path) -> tuple[dict[str, str], list[tuple[str, str]]]:
    labels: dict[str, str] = {}
    edges: list[tuple[str, str]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("%") or line.startswith("flowchart") or line.startswith("graph"):
            continue
        node_match = NODE_RE.match(line)
        if node_match:
            labels[node_match.group("id")] = node_match.group("label")
        edge_match = EDGE_RE.match(line)
        if edge_match:
            src = edge_match.group("src")
            dst = edge_match.group("dst")
            edges.append((src, dst))
            labels.setdefault(src, edge_match.group("src_label") or src.replace("_", " "))
            labels.setdefault(dst, edge_match.group("dst_label") or dst.replace("_", " "))
    return labels, edges


def assert_dag(nodes: set[str], edges: list[tuple[str, str]]) -> list[str]:
    outgoing: dict[str, list[str]] = defaultdict(list)
    indegree = {node: 0 for node in nodes}
    for src, dst in edges:
        outgoing[src].append(dst)
        indegree[dst] += 1

    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for dst in sorted(outgoing[node]):
            indegree[dst] -= 1
            if indegree[dst] == 0:
                queue.append(dst)
    if len(order) != len(nodes):
        cyclic = sorted(node for node, degree in indegree.items() if degree > 0)
        raise ValueError(f"Mermaid graph contains a cycle involving: {', '.join(cyclic)}")
    return order


def assign_layers(order: list[str], edges: list[tuple[str, str]]) -> dict[str, int]:
    parents: dict[str, list[str]] = defaultdict(list)
    for src, dst in edges:
        parents[dst].append(src)
    layer: dict[str, int] = {}
    for node in order:
        if not parents[node]:
            layer[node] = 0
        else:
            layer[node] = max(layer[parent] + 1 for parent in parents[node])
    return layer


def layout(labels: dict[str, str], edges: list[tuple[str, str]]) -> dict:
    nodes = set(labels)
    order = assert_dag(nodes, edges)
    layers = assign_layers(order, edges)
    by_layer: dict[int, list[str]] = defaultdict(list)
    for node in order:
        by_layer[layers[node]].append(node)

    max_layer = max(by_layer) if by_layer else 0
    x_min, x_max = -6.0, 6.0
    x_step = (x_max - x_min) / max(1, max_layer)
    coords: dict[str, dict] = {}
    for layer_idx in range(max_layer + 1):
        layer_nodes = by_layer[layer_idx]
        count = max(1, len(layer_nodes))
        for row, node in enumerate(layer_nodes):
            y = 2.75 if count == 1 else 2.75 - row * (5.5 / max(1, count - 1))
            coords[node] = {
                "label": labels[node],
                "x": round(x_min + layer_idx * x_step, 3),
                "y": round(y, 3),
                "layer": layer_idx,
            }
    return {
        "source": DEFAULT_MERMAID.as_posix(),
        "nodes": coords,
        "edges": [{"source": src, "target": dst} for src, dst in edges],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse Mermaid tech-tree DAG and emit deterministic coordinates.")
    parser.add_argument("--mermaid", type=Path, default=DEFAULT_MERMAID)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    labels, edges = parse_mermaid(args.mermaid)
    result = layout(labels, edges)
    result["source"] = args.mermaid.as_posix()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
