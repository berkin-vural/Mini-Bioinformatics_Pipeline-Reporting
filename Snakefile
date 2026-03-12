configfile: "config/config.yaml"

SAMPLE  = config["sample_name"]
FASTQ   = config["input_fastq"]
OUTDIR  = config.get("outdir", "results")

STATS_CSV     = f"{OUTDIR}/stats/{SAMPLE}.per_read_metrics.csv"

PLOT_GC   = f"{OUTDIR}/plots/{SAMPLE}.gc_hist.png"
PLOT_LEN  = f"{OUTDIR}/plots/{SAMPLE}.len_hist.png"
PLOT_MEAN = f"{OUTDIR}/plots/{SAMPLE}.meanq_hist.png"

rule all:
    input:
        STATS_CSV,
        PLOT_GC,
        PLOT_LEN,
        PLOT_MEAN

rule per_read_stats:
    conda:
        "envs/qc.yml"
    input:
        fastq=FASTQ
    output:
        csv=STATS_CSV
    shell:
        r"""
        python scripts/per_read_stats.py \
          --fastq {input.fastq} \
          --out {output.csv}
        """

rule make_plots:
    conda:
        "envs/qc.yml"
    input:
        csv=STATS_CSV
    output:
        gc=PLOT_GC,
        length=PLOT_LEN,
        meanq=PLOT_MEAN
    shell:
        r"""
        python scripts/make_plots.py \
          --csv {input.csv} \
          --out-gc {output.gc} \
          --out-len {output.length} \
          --out-meanq {output.meanq}
        """


