"""
Render whitepaper diagrams to PNG files.
Run from the repo root: python3 whitepaper/render_diagrams.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe
import os

OUT = os.path.join(os.path.dirname(__file__))
DPI = 200

# ── Color palette ────────────────────────────────────────────────────────────
C = {
    "req_dark":   "#4a9eed",
    "req_mid":    "#a5d8ff",
    "req_light":  "#dbe4ff",
    "code":       "#d0bfff",
    "code_dark":  "#8b5cf6",
    "test":       "#ffd8a8",
    "analysis":   "#fff3bf",
    "spec":       "#c3fae8",
    "spec_dark":  "#06b6d4",
    "result":     "#b2f2bb",
    "result_dark":"#22c55e",
    "human":      "#a5d8ff",
    "human_dark": "#2563eb",
    "llm":        "#d0bfff",
    "llm_dark":   "#8b5cf6",
    "warn":       "#ffc9c9",
    "warn_dark":  "#ef4444",
    "zone_req":   "#dbe4ff",
    "zone_code":  "#e5dbff",
    "zone_evi":   "#d3f9d8",
    "zone_common":"#b2f2bb",
    "txt_dark":   "#1e1e1e",
    "txt_mid":    "#444444",
    "txt_muted":  "#666666",
}


def box(ax, cx, cy, w, h, text, fc, ec, lw=1.5, fs=9, bold=False,
        text_color="#1e1e1e", alpha=1.0, style="round,pad=0.015"):
    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=style, facecolor=fc, edgecolor=ec,
        linewidth=lw, alpha=alpha, zorder=2,
    )
    ax.add_patch(patch)
    weight = "bold" if bold else "normal"
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            fontweight=weight, color=text_color,
            multialignment="center", zorder=3)


def zone(ax, x0, y0, w, h, fc, ec, label, label_color):
    patch = FancyBboxPatch(
        (x0, y0), w, h,
        boxstyle="round,pad=0.01", facecolor=fc, edgecolor=ec,
        linewidth=1, alpha=0.35, zorder=0,
    )
    ax.add_patch(patch)
    ax.text(x0 + 0.012, y0 + h - 0.012, label, va="top",
            fontsize=8.5, fontweight="bold", color=label_color, zorder=1)


def arr(ax, x1, y1, x2, y2, color="#333", lw=1.5, dashed=False,
        label="", label_fs=8):
    ls = (0, (4, 3)) if dashed else "solid"
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                        linestyle=ls, mutation_scale=12),
        zorder=4,
    )
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + 0.01, my, label, fontsize=label_fs, color=color,
                va="center", style="italic", zorder=5)


# ─────────────────────────────────────────────────────────────────────────────
# DIAGRAM 1: Artifact Graph
# ─────────────────────────────────────────────────────────────────────────────
def diagram1():
    fig, ax = plt.subplots(figsize=(15, 10.5))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(0.5, 0.975, "The Verification Compiler: Artifact Graph",
            ha="center", va="top", fontsize=14, fontweight="bold", color=C["txt_dark"])

    # Zones
    zone(ax, 0.01, 0.56, 0.98, 0.365, C["zone_req"], C["req_dark"],
         "REQUIREMENTS", C["human_dark"])
    zone(ax, 0.01, 0.435, 0.98, 0.115, C["zone_code"], C["code_dark"],
         "CODE UNITS  (C)", "#6d28d9")
    zone(ax, 0.01, 0.01, 0.98, 0.415, C["zone_evi"], C["result_dark"],
         "VERIFICATION EVIDENCE", "#15803d")

    # SR-1
    box(ax, 0.50, 0.875, 0.22, 0.055, "System Requirement SR-1",
        C["req_dark"], C["human_dark"], lw=2, fs=10, bold=True, text_color="white")

    arr(ax, 0.50, 0.847, 0.265, 0.787, C["human_dark"], lw=2)
    arr(ax, 0.50, 0.847, 0.775, 0.787, C["human_dark"], lw=2)

    # HLRs
    box(ax, 0.265, 0.765, 0.20, 0.05, "HL Requirement 1",
        C["req_mid"], C["req_dark"], fs=9.5)
    box(ax, 0.775, 0.765, 0.20, 0.05, "HL Requirement 2",
        C["req_mid"], C["req_dark"], fs=9.5)

    arr(ax, 0.265, 0.74, 0.15, 0.678, C["req_dark"], lw=1.5)
    arr(ax, 0.265, 0.74, 0.385, 0.678, C["req_dark"], lw=1.5)
    arr(ax, 0.775, 0.74, 0.775, 0.678, C["req_dark"], lw=1.5)

    # LLRs
    box(ax, 0.15, 0.655, 0.165, 0.048, "LL Req 1a",
        C["req_light"], C["req_dark"], fs=9.5)
    box(ax, 0.385, 0.655, 0.165, 0.048, "LL Req 1b",
        C["req_light"], C["req_dark"], fs=9.5)
    box(ax, 0.775, 0.655, 0.185, 0.048, "LL Req 2a",
        C["req_light"], C["req_dark"], fs=9.5)

    # LLR → Code
    arr(ax, 0.15, 0.631, 0.16, 0.508, C["llm_dark"], lw=1.5)
    arr(ax, 0.385, 0.631, 0.16, 0.508, C["llm_dark"], lw=1.5)
    arr(ax, 0.385, 0.631, 0.47, 0.508, C["llm_dark"], lw=1.5)
    arr(ax, 0.775, 0.631, 0.83, 0.508, C["llm_dark"], lw=1.5)

    # Code units
    box(ax, 0.16, 0.483, 0.185, 0.055, "init_motor()",
        C["code"], C["code_dark"], lw=2, fs=9.5, bold=True)
    box(ax, 0.47, 0.483, 0.185, 0.055, "read_sensor()",
        C["code"], C["code_dark"], lw=2, fs=9.5, bold=True)
    box(ax, 0.83, 0.483, 0.185, 0.055, "check_limit()",
        C["code"], C["code_dark"], lw=2, fs=9.5, bold=True)

    # Code → Evidence
    arr(ax, 0.16, 0.455, 0.085, 0.368, C["code_dark"], lw=1.5)
    arr(ax, 0.16, 0.455, 0.275, 0.368, C["code_dark"], lw=1.5)
    arr(ax, 0.47, 0.455, 0.47, 0.368, C["spec_dark"], lw=1.5,
        dashed=True, label="ref")
    arr(ax, 0.47, 0.455, 0.645, 0.368, C["code_dark"], lw=1.5)
    arr(ax, 0.83, 0.455, 0.875, 0.368, C["code_dark"], lw=1.5)

    # Evidence boxes
    box(ax, 0.085, 0.342, 0.14, 0.048, "Unit Test",
        C["test"], "#f59e0b", fs=9)
    box(ax, 0.275, 0.342, 0.155, 0.048, "Static Analysis",
        C["analysis"], "#d97706", fs=9)
    box(ax, 0.47, 0.342, 0.14, 0.048, "Datasheet",
        C["spec"], C["spec_dark"], fs=9)
    box(ax, 0.645, 0.342, 0.14, 0.048, "Integ. Test",
        C["test"], "#f59e0b", fs=9)
    box(ax, 0.875, 0.342, 0.155, 0.048, "Static Analysis",
        C["analysis"], "#d97706", fs=9)

    # Evidence → Results
    arr(ax, 0.085, 0.318, 0.085, 0.245, C["result_dark"], lw=1.5)
    arr(ax, 0.645, 0.318, 0.655, 0.245, C["result_dark"], lw=1.5)

    # Results
    box(ax, 0.085, 0.22, 0.14, 0.048, "Test Result",
        C["result"], C["result_dark"], fs=9)
    box(ax, 0.655, 0.22, 0.195, 0.048, "Physical Test Result",
        C["result"], C["result_dark"], fs=9)
    ax.text(0.655, 0.188, "tied to code version hash",
            ha="center", va="top", fontsize=7.5, color="#15803d", style="italic")

    plt.tight_layout(pad=0.5)
    plt.savefig(os.path.join(OUT, "diagram1_artifact_graph.png"),
                dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close()
    print("  diagram1_artifact_graph.png")


# ─────────────────────────────────────────────────────────────────────────────
# DIAGRAM 2: Verification Query Assembly
# ─────────────────────────────────────────────────────────────────────────────
def diagram2():
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(0.5, 0.975, "Graph Traversal: Assembling a Verification Query",
            ha="center", va="top", fontsize=14, fontweight="bold", color=C["txt_dark"])

    ax.text(0.04, 0.93, "ARTIFACT GRAPH (excerpt)", fontsize=10,
            fontweight="bold", color=C["human_dark"])
    ax.text(0.55, 0.93, "ASSEMBLED VERIFICATION QUERY",
            fontsize=10, fontweight="bold", color="#15803d")

    # Left: graph excerpt — requirements chain
    box(ax, 0.175, 0.860, 0.22, 0.052, "SR-1",
        C["req_dark"], C["human_dark"], lw=2, fs=10, bold=True, text_color="white")
    arr(ax, 0.175, 0.834, 0.175, 0.792, C["human_dark"], lw=1.5)
    box(ax, 0.175, 0.768, 0.22, 0.048, "HL Requirement 1",
        C["req_mid"], C["req_dark"], fs=9.5)
    arr(ax, 0.175, 0.744, 0.175, 0.702, C["req_dark"], lw=1.5)
    box(ax, 0.175, 0.678, 0.22, 0.048, "LL Req 1b",
        C["req_light"], C["req_dark"], fs=9.5)
    arr(ax, 0.175, 0.654, 0.175, 0.598, C["llm_dark"], lw=1.5)

    # Code unit (highlighted)
    box(ax, 0.175, 0.568, 0.245, 0.058, "read_sensor()",
        C["code_dark"], "#4c1d95", lw=3, fs=11, bold=True, text_color="white")

    # Evidence below
    arr(ax, 0.175, 0.539, 0.085, 0.472, C["spec_dark"], lw=1.5, dashed=True, label="ref")
    arr(ax, 0.175, 0.539, 0.27, 0.472, C["code_dark"], lw=1.5)
    box(ax, 0.085, 0.448, 0.16, 0.048, "Datasheet",
        C["spec"], C["spec_dark"], fs=9)
    box(ax, 0.27, 0.448, 0.16, 0.048, "Integ. Test",
        C["test"], "#f59e0b", fs=9)
    arr(ax, 0.27, 0.424, 0.27, 0.362, C["result_dark"], lw=1.5)
    box(ax, 0.27, 0.338, 0.195, 0.048, "Phys. Test Result",
        C["result"], C["result_dark"], fs=9)
    ax.text(0.27, 0.306, "same code version", ha="center",
            fontsize=7.5, color="#15803d", style="italic")

    # Collection arrow
    ax.annotate("", xy=(0.535, 0.568), xytext=(0.415, 0.568),
                arrowprops=dict(arrowstyle="-|>", color="#1e1e1e",
                                lw=3, mutation_scale=20), zorder=4)
    ax.text(0.475, 0.592, "traversal", ha="center", fontsize=9,
            fontweight="bold", color="#1e1e1e")
    ax.text(0.475, 0.575, "collects", ha="center", fontsize=9,
            fontweight="bold", color="#1e1e1e")

    # Right: query packet box
    qbox = FancyBboxPatch((0.545, 0.08), 0.42, 0.83,
                           boxstyle="round,pad=0.015",
                           facecolor="#fffde7", edgecolor="#f59e0b",
                           linewidth=2.5, linestyle=(0, (5, 3)), zorder=1)
    ax.add_patch(qbox)
    ax.text(0.755, 0.895, "VERIFICATION QUERY",
            ha="center", fontsize=11, fontweight="bold", color="#1e1e1e", zorder=3)
    ax.text(0.755, 0.873, "[ fits in model context window ]",
            ha="center", fontsize=8.5, color="#d97706", style="italic", zorder=3)

    sections = [
        (0.755, 0.810, 0.38, 0.09,  "Requirements Context\nSR-1  →  HL Req 1  →  LL Req 1b",
         C["req_mid"], C["req_dark"]),
        (0.755, 0.700, 0.38, 0.075, "Code Under Review\nread_sensor()",
         C["code"], C["code_dark"]),
        (0.755, 0.593, 0.38, 0.09,  "Tests & Results\nInteg. Test  |  Physical Test Result",
         C["test"], "#f59e0b"),
        (0.755, 0.497, 0.38, 0.075, "Referenced Specs\nDatasheet",
         C["spec"], C["spec_dark"]),
        (0.755, 0.385, 0.38, 0.09,  "Evaluation Instruction\nDo requirements match implementation\nand evidence?",
         "#fff9c4", "#d97706"),
    ]
    for cx, cy, w, h, txt, fc, ec in sections:
        box(ax, cx, cy, w, h, txt, fc, ec, fs=9, lw=1.5)

    ax.text(0.755, 0.12, "≈ 6–8K tokens", ha="center",
            fontsize=9, color="#d97706", fontweight="bold", zorder=3)

    # Arrow down to reviewer
    arr(ax, 0.755, 0.104, 0.755, 0.065, "#1e1e1e", lw=2)
    box(ax, 0.755, 0.040, 0.38, 0.045, "LLM or Human Reviewer  →  Structured Result",
        C["result"], C["result_dark"], fs=9.5, lw=2)

    plt.tight_layout(pad=0.5)
    plt.savefig(os.path.join(OUT, "diagram2_query_assembly.png"),
                dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close()
    print("  diagram2_query_assembly.png")


# ─────────────────────────────────────────────────────────────────────────────
# DIAGRAM 3: Dual-Mode Operation
# ─────────────────────────────────────────────────────────────────────────────
def diagram3():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(0.5, 0.975,
            "Dual-Mode Operation: Same Decomposition, Interchangeable Reviewers",
            ha="center", va="top", fontsize=13, fontweight="bold", color=C["txt_dark"])

    # Top: verification queries
    box(ax, 0.5, 0.885, 0.30, 0.055, "Verification Queries\n(from graph traversal)",
        "#fff9c4", "#f59e0b", fs=10, lw=2)

    # Branch arrows
    arr(ax, 0.5, 0.857, 0.22, 0.795, "#1e1e1e", lw=2)
    arr(ax, 0.5, 0.857, 0.78, 0.795, "#1e1e1e", lw=2)

    # Mode labels
    ax.text(0.22, 0.825, "LLM MODE", ha="center", fontsize=11,
            fontweight="bold", color=C["llm_dark"])
    ax.text(0.78, 0.825, "HUMAN MODE", ha="center", fontsize=11,
            fontweight="bold", color=C["human_dark"])

    # LLM box
    box(ax, 0.22, 0.755, 0.305, 0.065, "LLM Reviewer\n(automated, CI/CD)",
        C["llm"], C["llm_dark"], fs=10, lw=2)

    # Human box
    box(ax, 0.78, 0.755, 0.305, 0.065, "Human Reviewer\n(final certification)",
        C["human"], C["human_dark"], fs=10, lw=2)

    # Interchangeable arrow (double-headed)
    ax.annotate("", xy=(0.62, 0.755), xytext=(0.38, 0.755),
                arrowprops=dict(arrowstyle="<->", color=C["llm_dark"],
                                lw=1.5, linestyle=(0, (4, 3)),
                                mutation_scale=14), zorder=4)
    ax.text(0.5, 0.773, "interchangeable per node",
            ha="center", fontsize=8.5, color=C["llm_dark"], style="italic")

    # Down to results
    arr(ax, 0.22, 0.722, 0.22, 0.658, C["llm_dark"], lw=1.5)
    arr(ax, 0.78, 0.722, 0.78, 0.658, C["human_dark"], lw=1.5)

    # Result boxes
    box(ax, 0.22, 0.625, 0.30, 0.065,
        "Structured Result\npass/fail + confidence + rationale",
        "#ede9fe", C["llm_dark"], fs=9.5, lw=1.5)
    box(ax, 0.78, 0.625, 0.30, 0.065,
        "Structured Result\npass/fail + confidence + rationale",
        "#eff6ff", C["human_dark"], fs=9.5, lw=1.5)

    # Identical schema note
    box(ax, 0.5, 0.625, 0.155, 0.055, "identical\nevidence schema",
        "white", "#999999", fs=8.5, lw=1, style="round,pad=0.01")

    # Notes under results
    ax.text(0.22, 0.582, "confidence weighted by\ntask-specific accuracy profile",
            ha="center", fontsize=8.5, color=C["llm_dark"], style="italic",
            multialignment="center")
    ax.text(0.78, 0.582, "same decomposition used for\nhuman-reviewed certification",
            ha="center", fontsize=8.5, color=C["human_dark"], style="italic",
            multialignment="center")

    # Converge to evidence graph
    arr(ax, 0.22, 0.592, 0.46, 0.485, C["result_dark"], lw=2)
    arr(ax, 0.78, 0.592, 0.54, 0.485, C["result_dark"], lw=2)

    # Evidence graph
    box(ax, 0.5, 0.458, 0.30, 0.055, "Evidence Graph",
        C["result"], C["result_dark"], fs=11, bold=True, lw=2)

    # Provable decomp note
    box(ax, 0.855, 0.458, 0.235, 0.10,
        "graph structure\nindependently proves\nscope completeness",
        "#fff9c4", "#d97706", fs=8.5, lw=1)

    # Arrow to confidence score
    arr(ax, 0.5, 0.430, 0.5, 0.368, "#1e1e1e", lw=2)

    # Confidence score
    box(ax, 0.5, 0.328, 0.50, 0.075,
        "Confidence Score\n"
        "= per-query results × accuracy profiles × coverage × staleness",
        "#fff3e0", "#f59e0b", fs=9.5, lw=2)

    # Bottom clarifications
    ax.text(0.5, 0.232,
            "Any node reviewed by LLM can be re-reviewed by a human using the same query — "
            "the decomposition does not change.",
            ha="center", fontsize=9, color=C["txt_mid"], style="italic")

    plt.tight_layout(pad=0.5)
    plt.savefig(os.path.join(OUT, "diagram3_dual_mode.png"),
                dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close()
    print("  diagram3_dual_mode.png")


# ─────────────────────────────────────────────────────────────────────────────
# DIAGRAM 4: Cross-Standard Evidence Structure
# ─────────────────────────────────────────────────────────────────────────────
def diagram4():
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(0.5, 0.975,
            "Safety Standards: Evidence Structure Is Defined — Reviewer Identity Is Not",
            ha="center", va="top", fontsize=13, fontweight="bold", color=C["txt_dark"])

    # Row labels (left margin)
    row_labels = [
        (0.830, "Domain"),
        (0.720, "Safety / Security\nLevels"),
        (0.535, "Evidence\nRequired"),
        (0.378, "Reviewer\nSpecified?"),
    ]
    for y, lbl in row_labels:
        ax.text(0.01, y, lbl, ha="left", va="center", fontsize=9,
                color=C["txt_muted"], multialignment="center")

    # Column positions
    cols = [
        (0.28, "DO-178C", "Aerospace Software", C["req_dark"], C["human_dark"],
         "DAL A through E\n(A = most critical)",
         C["req_mid"], C["req_dark"],
         "Bidirectional traceability\nCode and design reviews\nTest plans and results\nTool qualification records",
         C["req_light"], C["req_dark"]),
        (0.55, "ISO 26262", "Automotive Safety", "#22c55e", "#15803d",
         "ASIL A through D\n(severity × exposure × controllability)",
         "#b2f2bb", "#22c55e",
         "Hazard analysis (FHA / FMEA)\nSafety case traceability\nTest plans and results\nASIL decomposition records",
         "#d3f9d8", "#22c55e"),
        (0.82, "IEC 62443", "Industrial / OT Systems", "#f59e0b", "#d97706",
         "Security Level 1 through 4\n(threat sophistication)",
         "#ffd8a8", "#f59e0b",
         "Threat analysis (TARA)\nControl-to-FR mapping records\nTest plans and results\nArchitecture review records",
         "#fff3bf", "#f59e0b"),
    ]

    col_w = 0.245

    for cx, name, domain, hfc, hec, levels, lfc, lec, evidence, efc, eec in cols:
        # Header
        box(ax, cx, 0.880, col_w, 0.075,
            f"{name}\n{domain}", hfc, hec,
            fs=10, bold=True, text_color="white", lw=2)

        # Levels
        box(ax, cx, 0.765, col_w, 0.08, levels,
            lfc, lec, fs=9, lw=1.5)

        # Evidence
        box(ax, cx, 0.575, col_w, 0.29, evidence,
            efc, eec, fs=9, lw=1.5)

        # Reviewer: NOT SPECIFIED
        box(ax, cx, 0.395, col_w, 0.065,
            "Reviewer:  NOT SPECIFIED",
            C["warn"], C["warn_dark"], fs=9.5, bold=True,
            text_color=C["warn_dark"], lw=2)

    # Common pattern footer
    footer = FancyBboxPatch(
        (0.09, 0.06), 0.82, 0.27,
        boxstyle="round,pad=0.015",
        facecolor=C["zone_common"], edgecolor=C["result_dark"],
        linewidth=2, zorder=1,
    )
    ax.add_patch(footer)
    ax.text(0.5, 0.305, "Common Pattern", ha="center", fontsize=11,
            fontweight="bold", color="#15803d", zorder=2)
    ax.text(
        0.5, 0.265,
        "All three standards define:  tiered severity/security levels  •  "
        "verification objectives per level  •  required evidence artifact types",
        ha="center", fontsize=9.5, color=C["txt_dark"], zorder=2,
    )
    ax.text(
        0.5, 0.225,
        "None of the three standards specify who or what performs the review — "
        "only that evidence meets the objective.",
        ha="center", fontsize=9.5, color=C["txt_dark"], zorder=2,
    )
    ax.text(
        0.5, 0.175,
        "A verification compiler that produces conformant evidence satisfies "
        "the standard's requirements by design,",
        ha="center", fontsize=9.5, color=C["txt_dark"], fontweight="bold", zorder=2,
    )
    ax.text(
        0.5, 0.140,
        "regardless of whether the reviewer is an LLM or a human engineer.",
        ha="center", fontsize=9.5, color=C["txt_dark"], fontweight="bold", zorder=2,
    )

    plt.tight_layout(pad=0.5)
    plt.savefig(os.path.join(OUT, "diagram4_cross_standard.png"),
                dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close()
    print("  diagram4_cross_standard.png")


# ─────────────────────────────────────────────────────────────────────────────
# DIAGRAM 5: Units of Intelligence — Properties and Endpoint Replaceability
# ─────────────────────────────────────────────────────────────────────────────
def diagram5():
    fig, ax = plt.subplots(figsize=(16, 11))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(0.5, 0.977, "Units of Intelligence: A New Category — Not DO-330 Tools",
            ha="center", va="top", fontsize=14, fontweight="bold", color=C["txt_dark"])

    # ── Section label: top half ──────────────────────────────────────────────
    ax.text(0.5, 0.938, "Comparison of Unit Types",
            ha="center", va="top", fontsize=10, color=C["txt_muted"], style="italic")

    # Column centers — two reviewer types only
    col_human  = 0.30
    col_llm    = 0.72
    col_w      = 0.36

    # Headers
    box(ax, col_human, 0.890, col_w, 0.060,
        "Human Engineer", C["human"], C["human_dark"],
        fs=12, bold=True, lw=2)
    box(ax, col_llm,   0.890, col_w, 0.060,
        "LLM Model Unit", C["llm"], C["llm_dark"],
        fs=12, bold=True, lw=2)

    # Property rows
    props = [
        ("Capacity",
         "Working memory — bounded by\ncognitive load, ~10s of artifacts",
         "Context window — bounded by\ndesign (6–128K tokens per query)"),
        ("Accuracy",
         "High, experience-dependent\nTask-specific; declines with fatigue",
         "Task-specific, measurable\n16–33% variance across domains"),
        ("Adaptability",
         "Cross-session learning\nCareer-long domain expertise",
         "Strong in-context adaptation\nNo cross-session memory"),
        ("Qualification\nPathway",
         "Education + certification +\nproject-specific authorization",
         "Task-specific accuracy profiling\n+ usage boundary definition"),
        ("Certification\nRole",
         "Primary — human verdict IS\nthe certification evidence",
         "Developmental only — LLM verdict\nis engineering feedback, not evidence"),
    ]

    row_ys = [0.800, 0.710, 0.620, 0.530, 0.440]
    row_h  = 0.068
    row_fc = ["#f8f9fa", "#f0f4ff", "#f8f9fa", "#f0f4ff", "#f8f9fa"]

    for i, (prop, h_text, l_text) in enumerate(props):
        y   = row_ys[i]
        rfc = row_fc[i]
        ax.text(0.01, y, prop, ha="left", va="center", fontsize=8.5,
                color=C["txt_muted"], fontweight="bold", multialignment="left")
        box(ax, col_human, y, col_w, row_h, h_text, rfc, C["human_dark"], fs=9, lw=1)
        box(ax, col_llm,   y, col_w, row_h, l_text, rfc, C["llm_dark"],   fs=9, lw=1)

    # "LLMs are NOT DO-330 tools" callout
    box(ax, 0.5, 0.365, 0.70, 0.050,
        "LLMs were not designed to meet DO-330 constraints — they are a new category"
        " of unit of intelligence,\nnot deterministic tools with fixed specifications."
        "  The compound architecture handles this, not DO-330 qualification of the LLM.",
        C["warn"], C["warn_dark"], fs=8.5, lw=2, text_color=C["warn_dark"])

    # ── Section label: bottom half ───────────────────────────────────────────
    ax.text(0.5, 0.312, "Compound Architecture: Reviewer Endpoint Replaceability",
            ha="center", va="top", fontsize=10, fontweight="bold", color=C["txt_dark"])

    # Artifact graph node (center-left)
    box(ax, 0.38, 0.232, 0.31, 0.065,
        "DAG Node\n(code unit + req chain + tool evidence)",
        "#fff9c4", "#f59e0b", fs=9.5, lw=2)
    ax.text(0.38, 0.187, "directed acyclic graph — no looping references",
            ha="center", fontsize=7.5, color="#d97706", style="italic")

    # Note: specialized tools shown in diagram 2
    ax.text(0.38, 0.268,
            "Evidence from specialized tools (cppcheck, aiT, gcov…)\nenters as DAG nodes — see Diagram 2 for assembly detail.",
            ha="center", fontsize=7.5, color=C["spec_dark"], style="italic",
            multialignment="center")

    # Query package arrow right
    arr(ax, 0.538, 0.232, 0.590, 0.232, "#1e1e1e", lw=2)
    box(ax, 0.72, 0.232, 0.26, 0.065,
        "Verification\nQuery Package",
        "#fffde7", "#d97706", fs=9.5, lw=2)

    # Branch arrows DOWN to two endpoints
    arr(ax, 0.655, 0.200, 0.36, 0.108, C["human_dark"], lw=1.5)
    arr(ax, 0.785, 0.200, 0.785, 0.108, C["llm_dark"],   lw=1.5)

    # Endpoint boxes
    box(ax, 0.36, 0.075, 0.30, 0.055,
        "Human Engineer  (certification pass)",
        C["human"], C["human_dark"], fs=9.5, lw=2.5, bold=True)
    box(ax, 0.785, 0.075, 0.30, 0.055,
        "LLM Model Unit  (nightly CI)",
        C["llm"],   C["llm_dark"],   fs=9.5, lw=2, bold=True)

    # Annotations
    ax.text(0.36, 0.033,
            "Independence: human reviewer independent\nof developer — satisfies DO-178C",
            ha="center", fontsize=7.5, color=C["human_dark"],
            fontweight="bold", multialignment="center")
    ax.text(0.785, 0.033,
            "Model diversity: rotate vendors —\nmultiple training sets must concur",
            ha="center", fontsize=7.5, color=C["llm_dark"],
            style="italic", multialignment="center")

    plt.tight_layout(pad=0.5)
    plt.savefig(os.path.join(OUT, "diagram5_units_of_intelligence.png"),
                dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close()
    print("  diagram5_units_of_intelligence.png")


# ─────────────────────────────────────────────────────────────────────────────
# DIAGRAM 6: Deployment Contexts — Three-Tier Spectrum
# ─────────────────────────────────────────────────────────────────────────────
def diagram6():
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(0.5, 0.972, "Same architecture and DAG — reviewer, VRM threshold, and CD gate are project-configured parameters.",
            ha="center", va="top", fontsize=11.5, color=C["txt_mid"], style="italic")

    # Three tier columns — wider with more vertical space
    tier_colors = [
        ("#dbe4ff", "#4a9eed"),   # Tier 1: light blue
        ("#d3f9d8", "#22c55e"),   # Tier 2: light green
        ("#ffe8cc", "#f59e0b"),   # Tier 3: warm amber
    ]
    tier_x = [0.025, 0.358, 0.691]
    tier_w = 0.307
    col_h  = 0.78
    col_y  = 0.09

    tier_titles  = ["TIER 1", "TIER 2", "TIER 3"]
    tier_names   = ["Development Teams", "Safety-Focused Teams", "Formal Certification"]
    tier_use     = [
        "Firmware, infrastructure,\ncontrols — no certification\nobligation",
        "Safety-relevant without\nformal cert program\n(ADAS, med devices)",
        "DO-178C · ISO 26262\nIEC 62443\n(avionics, automotive)",
    ]
    tier_reviewer = [
        "LLM only",
        "LLM + human escalation\n(flagged nodes → engineer queue)",
        "LLM pre-screen +\nqualified human final pass",
    ]
    tier_vrm = [
        "CI gate\nFails build if VRM < threshold\nor orphan nodes introduced",
        "CI gate + queue trigger\nLow-VRM nodes → human review\nwith evidence package",
        "Development signal only\n(not a certification gate)\nCert gate = human sign-off",
    ]
    tier_evidence = [
        "CI output\n(structured results,\ngraph coverage report)",
        "Internal audit trail\n(systematic, traceable\nfor incident review)",
        "Formal certification record\n(human-signed, TQL-5\ntool output available)",
    ]
    tier_cd = [
        "VRM ≥ threshold",
        "VRM + queue cleared",
        "Human sign-off",
    ]

    for i, (fc, ec) in enumerate(tier_colors):
        x0 = tier_x[i]
        cx = x0 + tier_w / 2

        # Background column
        bg = mpatches.FancyBboxPatch(
            (x0, col_y), tier_w, col_h,
            boxstyle="round,pad=0.01", facecolor=fc, edgecolor=ec,
            linewidth=2.5, zorder=1
        )
        ax.add_patch(bg)

        # Header band
        hdr = mpatches.FancyBboxPatch(
            (x0, col_y + col_h - 0.19), tier_w, 0.19,
            boxstyle="round,pad=0.01", facecolor=ec, edgecolor=ec,
            linewidth=0, alpha=0.18, zorder=2
        )
        ax.add_patch(hdr)

        # Tier label + name
        ax.text(cx, col_y + col_h - 0.025, tier_titles[i],
                ha="center", va="top", fontsize=15, fontweight="bold", color=ec, zorder=3)
        ax.text(cx, col_y + col_h - 0.075, tier_names[i],
                ha="center", va="top", fontsize=11, fontweight="bold", color=C["txt_dark"], zorder=3)
        ax.text(cx, col_y + col_h - 0.125, tier_use[i],
                ha="center", va="top", fontsize=9.5, color=C["txt_mid"],
                style="italic", multialignment="center", zorder=3)

        # Row: Reviewer
        y = col_y + col_h - 0.215
        ax.plot([x0 + 0.012, x0 + tier_w - 0.012], [y + 0.005, y + 0.005],
                color=ec, lw=0.8, alpha=0.6, zorder=2)
        ax.text(cx, y - 0.005, "REVIEWER", ha="center", va="top",
                fontsize=9, fontweight="bold", color=ec, zorder=3)
        ax.text(cx, y - 0.038, tier_reviewer[i], ha="center", va="top",
                fontsize=10, color=C["txt_dark"], multialignment="center", zorder=3)

        # Row: VRM Role
        y = col_y + col_h - 0.385
        ax.plot([x0 + 0.012, x0 + tier_w - 0.012], [y + 0.005, y + 0.005],
                color=ec, lw=0.8, alpha=0.6, zorder=2)
        ax.text(cx, y - 0.005, "VRM ROLE", ha="center", va="top",
                fontsize=9, fontweight="bold", color=ec, zorder=3)
        ax.text(cx, y - 0.038, tier_vrm[i], ha="center", va="top",
                fontsize=10, color=C["txt_dark"], multialignment="center", zorder=3)

        # Row: Evidence
        y = col_y + col_h - 0.58
        ax.plot([x0 + 0.012, x0 + tier_w - 0.012], [y + 0.005, y + 0.005],
                color=ec, lw=0.8, alpha=0.6, zorder=2)
        ax.text(cx, y - 0.005, "EVIDENCE", ha="center", va="top",
                fontsize=9, fontweight="bold", color=ec, zorder=3)
        ax.text(cx, y - 0.038, tier_evidence[i], ha="center", va="top",
                fontsize=10, color=C["txt_dark"], multialignment="center", zorder=3)

        # CD gate box
        cd_bg = mpatches.FancyBboxPatch(
            (x0 + 0.012, col_y + 0.012), tier_w - 0.024, 0.075,
            boxstyle="round,pad=0.008", facecolor=ec, edgecolor=ec,
            linewidth=1, alpha=0.88, zorder=2
        )
        ax.add_patch(cd_bg)
        ax.text(cx, col_y + 0.012 + 0.0375,
                "CD gate: " + tier_cd[i], ha="center", va="center",
                fontsize=11, color="white", fontweight="bold", zorder=3)

    # Arrows between tiers (increasing rigor →)
    for xi in [tier_x[1] - 0.005, tier_x[2] - 0.005]:
        ax.annotate("", xy=(xi + 0.002, col_y + col_h * 0.52),
                    xytext=(xi - 0.016, col_y + col_h * 0.52),
                    arrowprops=dict(arrowstyle="-|>", color="#999", lw=2.0,
                                   mutation_scale=16), zorder=5)

    # Bottom banner
    banner = mpatches.FancyBboxPatch(
        (0.025, 0.013), 0.95, 0.055,
        boxstyle="round,pad=0.01", facecolor="#1a3a6b", edgecolor="#1a3a6b",
        linewidth=1, alpha=0.92, zorder=2
    )
    ax.add_patch(banner)
    ax.text(0.5, 0.040,
            "Same underlying architecture — same DAG, same Verification Query Packages, same evidence schema",
            ha="center", va="center", fontsize=11, color="white",
            fontweight="bold", zorder=3)

    ax.text(0.5, 0.076, "← increasing formality and rigor →",
            ha="center", va="center", fontsize=10, color=C["txt_muted"], style="italic")

    plt.tight_layout(pad=0.5)
    plt.savefig(os.path.join(OUT, "diagram6_deployment_tiers.png"),
                dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close()
    print("  diagram6_deployment_tiers.png")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Rendering diagrams...")
    diagram1()
    diagram2()
    diagram3()
    diagram4()
    diagram5()
    diagram6()
    print("Done. Files written to whitepaper/")
