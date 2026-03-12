#!/usr/bin/env python3
import argparse
import gzip
import math
import pandas as pd

def open_maybe_gz(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path, "rt")

def phred_mean(qual_str: str) -> float:
    # Phred+33 varsayımı
    qs = [ord(c) - 33 for c in qual_str.strip()]
    return sum(qs) / len(qs) if qs else float("nan")

def gc_percent(seq: str) -> float:
    seq = seq.strip().upper()
    if not seq:
        return float("nan")
    gc = sum(1 for b in seq if b in ("G", "C"))
    atgc = sum(1 for b in seq if b in ("A", "T", "G", "C"))
    return (100.0 * gc / atgc) if atgc else float("nan")

def parse_fastq(path):
    with open_maybe_gz(path) as f:
        while True:
            header = f.readline().rstrip()
            if not header:
                break
            seq = f.readline().rstrip()
            plus = f.readline().rstrip()
            qual = f.readline().rstrip()
            if not qual:
                break
            read_id = header.split()[0].lstrip("@")
            yield read_id, seq, qual

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fastq", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rows = []
    for rid, seq, qual in parse_fastq(args.fastq):
        rows.append({
            "read_id": rid,
            "read_length": len(seq),
            "gc_percent": gc_percent(seq),
            "mean_q": phred_mean(qual)
        })

    df = pd.DataFrame(rows)
    df.to_csv(args.out, index=False)

if __name__ == "__main__":
    main()
