#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
from pathlib import Path


def require_tool(name):
    if shutil.which(name) is None:
        raise SystemExit(f"Missing required tool: {name}")


def run(cmd, stdout_path=None):
    if stdout_path is None:
        subprocess.run(cmd, check=True)
        return
    with open(stdout_path, "w") as out_f:
        subprocess.run(cmd, check=True, stdout=out_f)


def main():
    parser = argparse.ArgumentParser(
        description="Minimap2 alignment + BAM processing pipeline"
    )
    parser.add_argument("--fastq", required=True, help="Input FASTQ file")
    parser.add_argument("--reference", required=True, help="Reference FASTA")
    parser.add_argument("--outdir", default="results", help="Output directory")
    parser.add_argument("--threads", type=int, default=4, help="Thread count")
    parser.add_argument(
        "--preset",
        default="map-ont",
        help="Minimap2 preset (e.g., map-ont, map-pb, sr)",
    )
    args = parser.parse_args()

    require_tool("minimap2")
    require_tool("samtools")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    sam_path = outdir / "aligned.sam"
    bam_path = outdir / "aligned.bam"
    sorted_bam_path = outdir / "aligned.sorted.bam"
    flagstat_path = outdir / "aligned.flagstat.txt"
    idxstats_path = outdir / "aligned.idxstats.txt"

    minimap_cmd = [
        "minimap2",
        "-t",
        str(args.threads),
        "-ax",
        args.preset,
        args.reference,
        args.fastq,
    ]
    run(minimap_cmd, stdout_path=sam_path)

    run(["samtools", "view", "-bS", str(sam_path), "-o", str(bam_path)])
    run(["samtools", "sort", "-o", str(sorted_bam_path), str(bam_path)])
    run(["samtools", "index", str(sorted_bam_path)])
    run(["samtools", "flagstat", str(sorted_bam_path)], stdout_path=flagstat_path)
    run(["samtools", "idxstats", str(sorted_bam_path)], stdout_path=idxstats_path)

    print("Pipeline complete.")
    print(f"SAM: {sam_path}")
    print(f"Sorted BAM: {sorted_bam_path}")
    print(f"Stats: {flagstat_path}, {idxstats_path}")


if __name__ == "__main__":
    main()
