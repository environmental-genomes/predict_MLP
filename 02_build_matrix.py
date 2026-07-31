#!/usr/bin/env python3
"""Convert gapseq tables to the exact feature matrix required by the MLP."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

TRUE_VALUES = {"true", "1", "yes"}


def arguments():
    p = argparse.ArgumentParser()
    p.add_argument("--gapseq-dir", required=True, type=Path)
    p.add_argument("--metadata", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    return p.parse_args()


def parse_table(path):
    header = None
    observed, present = set(), set()
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip() or line.startswith("#"):
                continue
            fields = line.rstrip("\r\n").split("\t")
            if header is None:
                header = fields
                if not {"ID", "Prediction"}.issubset(header):
                    raise ValueError(f"{path}: ID/Prediction columns not found")
                continue
            row = dict(zip(header, fields))
            pathway = row["ID"].strip()
            if pathway in observed:
                raise ValueError(f"{path}: duplicated pathway ID {pathway}")
            observed.add(pathway)
            if row["Prediction"].strip().lower() in TRUE_VALUES:
                present.add(pathway)
    if header is None:
        raise ValueError(f"Empty pathway table: {path}")
    return observed, present


def main():
    a = arguments()
    metadata = json.loads(a.metadata.read_text(encoding="utf-8"))
    features = [str(x) for x in metadata["feature_names"]]
    if not features or len(features) != len(set(features)):
        raise ValueError("metadata.json has missing or duplicated feature_names")
    declared = metadata.get("n_features")
    if declared is not None and int(declared) != len(features):
        raise ValueError("metadata n_features does not equal len(feature_names)")
    feature_set = set(features)
    tables = sorted(a.gapseq_dir.glob("*-all-Pathways.tbl"))
    if not tables:
        raise FileNotFoundError(f"No *-all-Pathways.tbl in {a.gapseq_dir}")
    samples, calls, report = [], [], []
    for table in tables:
        suffix = "-all-Pathways.tbl"
        sample = table.name[:-len(suffix)]
        observed, present = parse_table(table)
        missing, extra = feature_set - observed, observed - feature_set
        if missing or extra:
            raise ValueError(f"{table.name}: pathway IDs differ from model; "
                             f"missing={len(missing)}, extra={len(extra)}")
        samples.append(sample)
        calls.append(present)
        report.append({"sample": sample, "predicted_pathways": len(present),
                       "matched_features": len(observed), "missing": 0, "extra": 0})
    if len(samples) != len(set(samples)):
        raise ValueError("Duplicated sample names")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(["ID", *samples])
        for feature in features:
            writer.writerow([feature, *(int(feature in present) for present in calls)])
    alignment = {"metadata": str(a.metadata.resolve()), "n_features": len(features),
                 "n_samples": len(samples), "samples": report}
    Path(str(a.output) + ".alignment.json").write_text(
        json.dumps(alignment, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(features)} pathways x {len(samples)} samples: {a.output}")


if __name__ == "__main__":
    main()
