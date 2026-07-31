#!/usr/bin/env python3
"""Run gapseq 1.4.0 pathway prediction for every external protein FASTA."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path


def arguments():
    p = argparse.ArgumentParser()
    p.add_argument("--faa-dir", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--threads", default=8, type=int)
    return p.parse_args()


def main():
    a = arguments()
    if a.threads < 1:
        raise ValueError("--threads must be positive")
    gapseq = shutil.which("gapseq")
    if not gapseq:
        raise FileNotFoundError("gapseq is not available in the active environment")
    faa_dir = a.faa_dir.resolve()
    files = sorted((*faa_dir.glob("*.faa"), *faa_dir.glob("*.faa.gz")))
    if not files:
        raise FileNotFoundError(f"No *.faa or *.faa.gz files in {faa_dir}")
    sample_names = [x.name[:-7] if x.name.endswith(".faa.gz") else x.stem for x in files]
    if len(sample_names) != len(set(sample_names)):
        raise ValueError("FAA filenames produce duplicated sample IDs")
    out = a.output_dir.resolve()
    logs = out / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    version = subprocess.run([gapseq, "-v"], text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, check=False).stdout
    (out / "gapseq_version.txt").write_text(version, encoding="utf-8")
    if "gapseq version: 1.4.0" not in version or "Sequence DB md5sum: 954ab58" not in version:
        raise RuntimeError("Expected gapseq 1.4.0 and Bacteria DB md5 prefix 954ab58; "
                           f"observed version report:\n{version}")

    for faa in files:
        sample = faa.name[:-7] if faa.name.endswith(".faa.gz") else faa.stem
        target = out / f"{sample}-all-Pathways.tbl"
        if target.is_file() and target.stat().st_size:
            print(f"[SKIP] {sample}", flush=True)
            continue
        work = out / f".work_{sample}"
        work.mkdir(exist_ok=True)
        command = [gapseq, "find", "-p", "all", "-t", "Bacteria",
                   "-M", "prot", "-K", str(a.threads), str(faa.resolve())]
        print(f"[START] {sample}", flush=True)
        with (logs / f"{sample}.log").open("w", encoding="utf-8") as log:
            completed = subprocess.run(command, cwd=work, stdout=log,
                                       stderr=subprocess.STDOUT, env=os.environ.copy())
        if completed.returncode:
            raise RuntimeError(f"gapseq failed for {sample}; see {logs / (sample + '.log')}")
        produced = sorted(work.glob("*-all-Pathways.tbl"))
        if len(produced) != 1 or not produced[0].stat().st_size:
            raise RuntimeError(f"Expected one non-empty pathway table for {sample}; keeping {work}")
        produced[0].replace(target)
        shutil.rmtree(work)
        print(f"[DONE] {target}", flush=True)


if __name__ == "__main__":
    main()
