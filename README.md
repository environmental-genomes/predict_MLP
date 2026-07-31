# MLP-Based Classification of External Genomes into NPA, PAc, and PAd

This package provides a pretrained multilayer perceptron (MLP) model for classifying bacterial genomes into the NPA, PAc, or PAd category. The model was trained on the known functional-gene feature matrix used in **Fig. 5a** and accepts predicted proteins in FASTA format (`.faa` or `.faa.gz`) as its starting input.

The workflow was designed as a lightweight, CPU-compatible option so that it can be used without a GPU. It uses 3,156 gapseq pathway features and achieved an accuracy of approximately 0.8 in our evaluation. For the more accurate (>0.9) protein-structure-based external prediction model, see [CryoClass](https://github.com/ZhuGuoLiang-gi/CryoClass).

The complete workflow is:

```text
protein FASTA files
        ↓
gapseq pathway prediction
        ↓
3,156-feature binary pathway matrix
        ↓
pretrained MLP model
        ↓
NPA / PAc / PAd predictions
```

## 1. System requirements

- A Linux x86-64 system
- Conda or Mamba
- Internet access and sufficient disk space to install gapseq and its bacterial sequence database
- CPU execution is supported; a GPU is not required

gapseq pathway prediction is normally the most time-consuming part of the workflow.

## 2. Create the environments

Open a terminal in the repository directory. For example:

```bash
cd predict_MLP
```

Create the two isolated Conda environments:

```bash
conda env create -f environment_gapseq.yml
conda env create -f environment_predict.yml
```


Verify the installation and model package:

```bash
conda run -n gapseq140_pathway gapseq -v
conda run -n gapseq140_pathway gapseq test

conda run -n npa_mlp_predict python -c \
  "import tensorflow, sklearn, pandas, joblib; print(tensorflow.__version__)"

conda run -n npa_mlp_predict python 00_verify_install.py \
  --model-dir model/MLP
```

The final command should report:

```text
Package and environment check: OK
```

The model features were generated with:

- gapseq version: `1.4.0`
- Bacteria Sequence Database date: `2024-11-06`
- Bacteria Sequence Database MD5: `954ab5834c907e22d6d6a98d45df6640`

Use the same gapseq and database versions whenever possible. The workflow checks these values before processing the input genomes to reduce incompatibility between the external pathway matrix and the trained model.

## 3. Prepare the input data

Place one protein FASTA file per genome in `input_faa/`:

```text
input_faa/
├── genome_A.faa
├── genome_B.faa
└── genome_C.faa
```

Important input requirements:

- Only protein FASTA files are accepted.
- Do not place nucleotide FASTA files such as `.fna` files in this directory.
- Each filename must be unique.
- The filename without `.faa` or `.faa.gz` is used as the sample identifier in the final output.

For example, `genome_A.faa` will appear as `genome_A` in the prediction table.

## 4. Run the complete workflow

The default configuration is stored in `config.env`:

```bash
FAA_DIR=input_faa
GAPSEQ_ENV=gapseq140_pathway
PREDICT_ENV=npa_mlp_predict
THREADS=8
OUTPUT_DIR=results
```

Adjust `THREADS` according to the CPU resources available on your machine or computing cluster. Then run:

```bash
bash run_all.sh config.env
```

You do not need to activate either environment manually. The script uses `conda run` to execute each stage in the appropriate environment.

The workflow performs the following steps:

1. Verifies the model files, their checksums, and the prediction environment.
2. Runs gapseq pathway prediction for every input FAA file.
3. Builds a binary pathway matrix using the exact feature names and order stored in `metadata.json`.
4. Loads the packaged scaler and MLP model.
5. Writes the predicted class and the probability of each class.

Existing, non-empty gapseq pathway tables are skipped, so an interrupted gapseq run can be resumed.

## 5. Output files

The final prediction table is:

```text
results/final_predictions.csv
```

It contains the following columns:

| Column              | Description                                                    |
| ------------------- | -------------------------------------------------------------- |
| `sample`          | Sample identifier derived from the FAA filename                |
| `predicted_class` | Class with the highest predicted probability: NPA, PAc, or PAd |
| `max_probability` | Highest of the three predicted probabilities                   |
| `probability_NPA` | Predicted probability for NPA                                  |
| `probability_PAc` | Predicted probability for PAc                                  |
| `probability_PAd` | Predicted probability for PAd                                  |

Additional outputs include:

```text
results/
├── final_predictions.csv
├── external_pathway_matrix.csv
├── external_pathway_matrix.csv.alignment.json
├── gapseq_out/
│   ├── SAMPLE-all-Pathways.tbl
│   └── logs/
└── logs/
    ├── 00_verify_install.log
    ├── 01_gapseq.log
    ├── 02_matrix.log
    └── 03_prediction.log
```

The alignment report records whether the pathway identifiers generated for each genome match all 3,156 features required by the model.

