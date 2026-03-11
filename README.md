# Mini-Bioinformatics_Pipeline-Reporting
Reproducible long-read FASTQ QC pipeline (per-read stats + plots) using Snakemake and Conda.

## Requirements

- Conda (Miniconda / Mambaforge recommended)

# 1) Configure the input

Edit `config/config.yaml`:

```yaml
input_fastq: "data/reads.fastq"     # FASTQ or FASTQ.GZ
outdir: "results"
sample_name: "Sample1"
threads: 4
```

# 2) Create the conda environment

```bash
conda env create -f envs/qc.yml
conda activate longread-qc
```

# 3) Run the pipeline

Dry-run (recommended)
```bash
snakemake -n -p
```
Execute
```bash
snakemake --use-conda -j 4
```
# -j 4 runs up to 4 jobs in parallel (depending on rule dependencies).
# --use-conda ensures Snakemake uses the environment specified in envs/qc.yml.
