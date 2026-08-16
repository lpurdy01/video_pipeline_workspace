"""
Artifact graph schema for the whitepaper verification prototype.

Node types:
  WhitepaperSection  SEC-   parsed from Introductory_composition.md
  Requirement        REQ-   parsed from verification_compiler_requirements.md
  Claim              CLAIM- parsed from project_wiki/claims/*.md + matrix rows
  Source             SRC-   parsed from project_wiki/sources/*.md

Edge types:
  supported-by       CLAIM -> SRC    (source cited in support)
  appears-in         CLAIM -> SEC    (claim phrase found / mapped in section)
  covers             SEC   -> REQ    (section addresses requirement)
  sub-section-of     SEC   -> SEC    (H3 is child of H2)
  sub-req-of         REQ   -> REQ    (requirement rolls up to parent section)
  related-claim      CLAIM -> CLAIM  (claims sharing a source — for consistency check)
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


NodeType = Literal["section", "requirement", "claim", "source"]
EdgeType = Literal[
    "supported-by", "appears-in", "covers",
    "sub-section-of", "sub-req-of", "related-claim",
]


@dataclass
class Node:
    id: str
    type: NodeType
    title: str
    text: str
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "text": self.text,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Node":
        return cls(
            id=d["id"],
            type=d["type"],
            title=d["title"],
            text=d["text"],
            metadata=d.get("metadata", {}),
        )


@dataclass
class Edge:
    from_id: str
    to_id: str
    type: EdgeType
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "from_id": self.from_id,
            "to_id": self.to_id,
            "type": self.type,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Edge":
        return cls(
            from_id=d["from_id"],
            to_id=d["to_id"],
            type=d["type"],
            metadata=d.get("metadata", {}),
        )


@dataclass
class Graph:
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)

    def add_node(self, node: Node) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        if edge.from_id not in self.nodes:
            raise ValueError(f"from_id not in graph: {edge.from_id}")
        if edge.to_id not in self.nodes:
            raise ValueError(f"to_id not in graph: {edge.to_id}")
        self.edges.append(edge)

    def edges_from(self, node_id: str, edge_type: EdgeType | None = None) -> list[Edge]:
        return [
            e for e in self.edges
            if e.from_id == node_id and (edge_type is None or e.type == edge_type)
        ]

    def edges_to(self, node_id: str, edge_type: EdgeType | None = None) -> list[Edge]:
        return [
            e for e in self.edges
            if e.to_id == node_id and (edge_type is None or e.type == edge_type)
        ]

    def nodes_of_type(self, node_type: NodeType) -> list[Node]:
        return [n for n in self.nodes.values() if n.type == node_type]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
        }
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "Graph":
        data = json.loads(path.read_text(encoding="utf-8"))
        g = cls()
        for nd in data["nodes"]:
            g.nodes[nd["id"]] = Node.from_dict(nd)
        for ed in data["edges"]:
            g.edges.append(Edge.from_dict(ed))
        return g

    def summary(self) -> str:
        type_counts: dict[str, int] = {}
        for n in self.nodes.values():
            type_counts[n.type] = type_counts.get(n.type, 0) + 1
        edge_counts: dict[str, int] = {}
        for e in self.edges:
            edge_counts[e.type] = edge_counts.get(e.type, 0) + 1
        lines = ["Graph summary:"]
        lines += [f"  nodes/{t}: {c}" for t, c in sorted(type_counts.items())]
        lines += [f"  edges/{t}: {c}" for t, c in sorted(edge_counts.items())]
        return "\n".join(lines)
