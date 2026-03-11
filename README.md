# Mini-Bioinformatics_Pipeline-Reporting
Reproducible long-read FASTQ QC pipeline (per-read stats + plots) using Snakemake and Conda.

## Requirements

- Conda (Miniconda / Mambaforge recommended)

## 1) Configure the input

Edit `config/config.yaml`:

```yaml
input_fastq: "data/reads.fastq"     # FASTQ or FASTQ.GZ
outdir: "results"
sample_name: "Sample1"
threads: 4
```

