#!/usr/bin/env python3
"""Extract published TorchVision 0.17 weight-table observations from a saved HTML snapshot.

The input is an official documentation snapshot stored under ignored out/sources/.
This script does not infer latency or compare metrics across benchmark tasks.
"""

import hashlib
import json
import math
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "out/sources/torchvision_models_0_17.html"
DEST = ROOT / "interactive/src/data/torchvision_observations.json"
BASE_URL = "https://docs.pytorch.org/vision/0.17/models.html"

TABLES = {
    1: ("image_classification", "ImageNet-1K validation", "top1_accuracy", "percent", 1, 3, 4),
    3: ("semantic_segmentation", "COCO with VOC labels", "mean_iou", "percent", 1, 3, 4),
    4: ("object_detection", "COCO val2017", "box_map", "percent", 1, 2, 3),
    7: ("video_classification", "Kinetics-400", "top1_accuracy", "percent", 1, 3, 4),
}

HIGHLIGHT = {
    "AlexNet", "VGG16", "GoogLeNet", "Inception_V3", "ResNet18", "ResNet50",
    "ResNet152", "DenseNet121", "EfficientNet_B0", "EfficientNet_B7", "MobileNet_V2",
    "MobileNet_V3_Large", "RegNet_Y_16GF", "ConvNeXt_Base", "ViT_B_16", "ViT_L_16",
    "Swin_T", "Swin_B", "FasterRCNN_ResNet50_FPN", "SSD300_VGG16",
    "DeepLabV3_ResNet50", "MViT_V2_S", "R3D_18",
}


def numeric(text):
    return float(text.replace("M", "").replace(",", ""))


def main():
    raw = SOURCE.read_bytes()
    soup = BeautifulSoup(raw, "html.parser")
    tables = soup.select("table")
    records = []
    for table_index, (domain, benchmark, metric, unit, metric_i, params_i, flops_i) in TABLES.items():
        for row_i, row in enumerate(tables[table_index].select("tbody tr"), 1):
            cells = row.select("td")
            if not cells:
                continue
            weight = cells[0].get_text(" ", strip=True)
            link = cells[0].select_one("a[href]")
            model = weight.split("_Weights.")[0]
            try:
                value = numeric(cells[metric_i].get_text(" ", strip=True))
                params = numeric(cells[params_i].get_text(" ", strip=True))
                gflops = numeric(cells[flops_i].get_text(" ", strip=True))
            except (ValueError, IndexError) as exc:
                raise ValueError(f"Bad official row {table_index}:{row_i}: {weight}") from exc
            if not all(math.isfinite(x) for x in (value, params, gflops)):
                continue  # Feature-only weights have no published classification score.
            records.append({
                "id": f"EI-TV017-{table_index:02d}-{row_i:03d}",
                "domain": domain,
                "benchmark": benchmark,
                "metric": metric,
                "unit": unit,
                "weight": weight,
                "model": model,
                "value": value,
                "params_m": params,
                "gflops": gflops,
                "highlight": model in HIGHLIGHT,
                "source_id": "EI-SRC-TV017",
                "source_url": urljoin(BASE_URL, link["href"]) if link else BASE_URL,
                "source_locator": f"TorchVision 0.17 model table {table_index}, row {row_i}, weight {weight}",
            })
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(json.dumps({
        "source": {"id": "EI-SRC-TV017", "url": BASE_URL, "version": "0.17",
                   "snapshot_sha256": hashlib.sha256(raw).hexdigest(),
                   "inspected_on": "2026-09-28", "status": "official version-pinned library documentation",
                   "jurisdiction": "benchmark results; no regulatory jurisdiction implied",
                   "uncertainty": "individual benchmark configuration and preprocessing; no deployment transfer",
                   "scope": "Float-weight summary tables; published benchmark values and weight-specific GFLOPs; not measured latency"},
        "observations": records,
    }, indent=2, allow_nan=False) + "\n")
    print(f"Wrote {len(records)} records to {DEST}")


if __name__ == "__main__":
    main()
