#!/usr/bin/env python3
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def write_summary(df, out_path):
    def s(col):
        x = df[col].dropna().to_numpy()
        return {
            "n": int(len(x)),
            "mean": float(np.mean(x)) if len(x) else np.nan,
            "median": float(np.median(x)) if len(x) else np.nan,
            "p10": float(np.percentile(x, 10)) if len(x) else np.nan,
            "p90": float(np.percentile(x, 90)) if len(x) else np.nan,
        }

    stats = {
        "gc_percent": s("gc_percent"),
        "read_length": s("read_length"),
        "mean_q": s("mean_q"),
    }

    # N50 (read_length için)
    lens = np.sort(df["read_length"].dropna().to_numpy())[::-1]
    if len(lens):
        csum = np.cumsum(lens)
        half = csum[-1] / 2
        n50 = float(lens[np.where(csum >= half)[0][0]])
    else:
        n50 = np.nan

    with open(out_path, "w", encoding="utf-8") as w:
        w.write("Summary statistics (per-read)\n")
        w.write("================================\n\n")
        for k, v in stats.items():
            w.write(f"{k}:\n")
            for kk, vv in v.items():
                w.write(f"  {kk}: {vv}\n")
            w.write("\n")
        w.write(f"read_length_N50: {n50}\n")

def hist_plot(x, title, xlabel, out_png, logx=False):
    x = x.dropna()
    plt.figure()
    if logx:
        x = x[x > 0]
        plt.hist(np.log10(x), bins=60)
        plt.title(title + " (log10)")
        plt.xlabel("log10(" + xlabel + ")")
    else:
        plt.hist(x, bins=60)
        plt.title(title)
        plt.xlabel(xlabel)
    plt.ylabel("Read count")
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Per-read metrics CSV")
    ap.add_argument("--outdir", default=None, help="Output directory (optional)")
    ap.add_argument("--prefix", default=None, help="Output filename prefix (optional)")

    # İsteğe bağlı override (istersen tek tek de yazabil)
    ap.add_argument("--out-gc", default=None)
    ap.add_argument("--out-len", default=None)
    ap.add_argument("--out-meanq", default=None)
    ap.add_argument("--out-summary", default=None)

    args = ap.parse_args()

    csv_path = Path(args.csv)
    outdir = Path(args.outdir) if args.outdir else csv_path.parent
    outdir.mkdir(parents=True, exist_ok=True)

    # prefix: kullanıcı vermezse CSV dosya adından türet (results.csv -> results)
    prefix = args.prefix if args.prefix else csv_path.stem

    out_gc = Path(args.out_gc) if args.out_gc else outdir / f"{prefix}.gc_hist.png"
    out_len = Path(args.out_len) if args.out_len else outdir / f"{prefix}.len_hist.png"
    out_meanq = Path(args.out_meanq) if args.out_meanq else outdir / f"{prefix}.meanq_hist.png"
    out_summary = Path(args.out_summary) if args.out_summary else outdir / f"{prefix}.summary.txt"

    df = pd.read_csv(csv_path)

    hist_plot(df["gc_percent"], "GC% distribution", "GC%", out_gc, logx=False)
    hist_plot(df["read_length"], "Read length distribution", "Read length (bp)", out_len, logx=True)
    hist_plot(df["mean_q"], "Mean read quality distribution", "Mean Phred Q", out_meanq, logx=False)

    write_summary(df, out_summary)

    print("Wrote outputs:")
    print(" ", out_gc)
    print(" ", out_len)
    print(" ", out_meanq)
    print(" ", out_summary)

if __name__ == "__main__":
    main()
