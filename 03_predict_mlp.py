#!/usr/bin/env python3
"""Predict NPA/PAc/PAd using only the packaged MLP."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf


def arguments():
    p = argparse.ArgumentParser()
    p.add_argument("--model-dir", required=True, type=Path)
    p.add_argument("--matrix", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--batch-size", default=32, type=int)
    return p.parse_args()


def main():
    a = arguments()
    if a.batch_size < 1:
        raise ValueError("--batch-size must be positive")
    required_files = [a.model_dir / "metadata.json", a.model_dir / "scaler.joblib",
                      a.model_dir / "model.keras"]
    missing_files = [str(x) for x in required_files if not x.is_file()]
    if missing_files:
        raise FileNotFoundError(f"Missing MLP package files: {missing_files}")
    metadata = json.loads(required_files[0].read_text(encoding="utf-8"))
    if metadata.get("model") != "MLP":
        raise ValueError("metadata.json is not an MLP package")
    features = pd.Index([str(x) for x in metadata["feature_names"]])
    classes = [str(x) for x in metadata["classes"]]
    if set(classes) != {"NPA", "PAc", "PAd"}:
        raise ValueError(f"Unexpected classes: {classes}")
    raw = pd.read_csv(a.matrix, index_col=0)
    raw.index, raw.columns = raw.index.astype(str), raw.columns.astype(str)
    if raw.index.duplicated().any() or raw.columns.duplicated().any():
        raise ValueError("Duplicated pathway or sample IDs in matrix")
    missing, extra = features.difference(raw.index), raw.index.difference(features)
    if len(missing) or len(extra):
        raise ValueError(f"Matrix/model feature mismatch: missing={len(missing)}, extra={len(extra)}")
    frame = raw.reindex(features).T.apply(pd.to_numeric, errors="raise").astype(np.float32)
    values = set(np.unique(frame.to_numpy()).tolist())
    if not values.issubset({0.0, 1.0}):
        raise ValueError(f"Matrix must be binary; observed values include {sorted(values)[:10]}")
    scaler = joblib.load(required_files[1])
    if int(getattr(scaler, "n_features_in_", -1)) != len(features):
        raise ValueError("Scaler feature count differs from metadata")
    scaled = scaler.transform(frame.to_numpy(dtype=np.float32))
    model = tf.keras.models.load_model(required_files[2])
    probability = model.predict(scaled, batch_size=a.batch_size, verbose=0)
    if probability.shape != (len(frame), len(classes)):
        raise ValueError(f"Unexpected model output shape: {probability.shape}")
    predicted = probability.argmax(axis=1)
    result = pd.DataFrame({"sample": frame.index,
                           "predicted_class": [classes[i] for i in predicted],
                           "max_probability": probability.max(axis=1)})
    for index, name in enumerate(classes):
        result[f"probability_{name}"] = probability[:, index]
    a.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(a.output, index=False)
    print(result["predicted_class"].value_counts().reindex(classes, fill_value=0).to_string())
    print(f"Predictions written to: {a.output}")


if __name__ == "__main__":
    main()

