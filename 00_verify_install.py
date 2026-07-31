#!/usr/bin/env python3
"""Fail fast when the published MLP package or prediction environment is unusable."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import joblib
import numpy
import pandas
import sklearn
import tensorflow as tf


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest().upper()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", required=True, type=Path)
    args = parser.parse_args()
    folder = args.model_dir
    expected = {}
    for line in (folder / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        checksum, filename = line.split(maxsplit=1)
        expected[filename.strip()] = checksum.upper()
    for filename, checksum in expected.items():
        path = folder / filename
        if not path.is_file() or digest(path) != checksum:
            raise RuntimeError(f"Missing or checksum mismatch: {path}")
    metadata = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
    if metadata.get("model") != "MLP" or metadata.get("classes") != ["NPA", "PAc", "PAd"]:
        raise ValueError("Unexpected model type or class order in metadata")
    features = metadata.get("feature_names", [])
    if len(features) != 3156 or len(features) != len(set(features)):
        raise ValueError("Expected 3156 unique feature names")
    scaler = joblib.load(folder / "scaler.joblib")
    if int(getattr(scaler, "n_features_in_", -1)) != len(features):
        raise ValueError("Scaler feature count differs from metadata")
    model = tf.keras.models.load_model(folder / "model.keras")
    if int(model.input_shape[-1]) != len(features) or int(model.output_shape[-1]) != 3:
        raise ValueError(f"Unexpected Keras shapes: {model.input_shape} -> {model.output_shape}")
    print("Package and environment check: OK")
    print("Python", platform.python_version())
    print("NumPy", numpy.__version__, "pandas", pandas.__version__)
    print("scikit-learn", sklearn.__version__, "joblib", joblib.__version__)
    print("TensorFlow", tf.__version__)


if __name__ == "__main__":
    main()
