# Minimap2-auto-pipeline

Simple Python pipeline for Minimap2 alignment and BAM post-processing.

## Requirements

- `minimap2`
- `samtools`
- Python 3.8+

## Usage

```bash
python scripts/run_pipeline.py \
  --fastq data/sample.fastq \
  --reference refs/genome.fa \
  --outdir results \
  --threads 4 \
  --preset map-ont \
  --plot
```

## Outputs

- `results/aligned.sam`
- `results/aligned.bam`
- `results/aligned.sorted.bam`
- `results/aligned.sorted.bam.bai`
- `results/aligned.flagstat.txt`
- `results/aligned.idxstats.txt`
- `results/aligned.depth.tsv`
- `results/aligned.coverage.png` (when `--plot` is used)
