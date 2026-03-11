# Mini-Bioinformatics_Pipeline-Reporting
Reproducible long-read FASTQ QC pipeline (per-read stats + plots) using Snakemake and Conda.

## Requirements

- Conda (Miniconda / Mambaforge recommended)

# 1) Configure the input

Place your input file in the `data/` directory in either **FASTQ** (`.fastq`) or **gzipped FASTQ** (`.fastq.gz`) format, then update the filename/path in `config/config.yaml` under `input_fastq`.

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

#-j 4 runs up to 4 jobs in parallel (depending on rule dependencies).

#--use-conda ensures Snakemake uses the environment specified in envs/qc.yml.

# Outputs

Outputs are created under results/:

results/stats/<sample>.per_read_metrics.csv

results/stats/<sample>.per_read_metrics_summary.txt

results/plots/<sample>.gc_hist.png

results/plots/<sample>.len_hist.png

results/plots/<sample>.meanq_hist.png
