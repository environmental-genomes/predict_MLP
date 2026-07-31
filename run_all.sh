#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
CONFIG=${1:-"$ROOT/config.env"}
[[ -f "$CONFIG" ]] || { echo "[ERROR] Missing config: $CONFIG" >&2; exit 1; }
# shellcheck disable=SC1090
source "$CONFIG"
cd "$ROOT"

mkdir -p "$OUTPUT_DIR/logs"
MODEL_DIR="$ROOT/model/MLP"
GAPSEQ_OUT="$OUTPUT_DIR/gapseq_out"
MATRIX="$OUTPUT_DIR/external_pathway_matrix.csv"
FINAL="$OUTPUT_DIR/final_predictions.csv"

for file in metadata.json scaler.joblib model.keras; do
  [[ -s "$MODEL_DIR/$file" ]] || { echo "[ERROR] Missing model/MLP/$file" >&2; exit 1; }
done
[[ -d "$FAA_DIR" ]] || { echo "[ERROR] Missing FAA directory: $FAA_DIR" >&2; exit 1; }
command -v conda >/dev/null || { echo "[ERROR] conda command not found" >&2; exit 1; }

conda run --no-capture-output -n "$PREDICT_ENV" python "$ROOT/00_verify_install.py" \
  --model-dir "$MODEL_DIR" 2>&1 | tee "$OUTPUT_DIR/logs/00_verify_install.log"

conda run --no-capture-output -n "$GAPSEQ_ENV" python "$ROOT/01_run_gapseq.py" \
  --faa-dir "$FAA_DIR" --output-dir "$GAPSEQ_OUT" --threads "$THREADS" \
  2>&1 | tee "$OUTPUT_DIR/logs/01_gapseq.log"

conda run --no-capture-output -n "$PREDICT_ENV" python "$ROOT/02_build_matrix.py" \
  --gapseq-dir "$GAPSEQ_OUT" --metadata "$MODEL_DIR/metadata.json" --output "$MATRIX" \
  2>&1 | tee "$OUTPUT_DIR/logs/02_matrix.log"

conda run --no-capture-output -n "$PREDICT_ENV" python "$ROOT/03_predict_mlp.py" \
  --model-dir "$MODEL_DIR" --matrix "$MATRIX" --output "$FINAL" \
  2>&1 | tee "$OUTPUT_DIR/logs/03_prediction.log"

echo "[DONE] Final result: $ROOT/$FINAL"
