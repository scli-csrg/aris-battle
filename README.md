# Edge-Intelligent Acoustic RIS Battles

This repository contains reference source code for the paper:

> Edge-Intelligent Acoustic Reconfigurable Intelligent Surface Battles in Connected Autonomous Underwater Vehicular Networks

The code implements a lightweight simulator for acoustic reconfigurable intelligent surface (ARIS) battles in connected autonomous underwater vehicular networks. It includes underwater acoustic channel utilities, binary ARIS configuration models, distributed and sample-efficient search algorithms, and scripts that regenerate the paper-facing CSV/PGFPlots data.

## What Is Included

- Acoustic propagation utilities with Thorp absorption, distance-dependent loss, propagation phase, multipath, and ARIS-assisted paths.
- Binary ARIS surface models for defender and adversary surfaces.
- Optimization routines for random search, element flipping, greedy search, beamforming-style binary alignment, consensus updates, and Hamming-kernel Bayesian search.
- Paper experiment generators for jamming, secure communication, sensing obfuscation, timing effects, hardware sweeps, channel effects, and edge-cost comparison.
- Standard-library tests and export scripts. No Python package dependencies are required for the default workflow.

## Quick Start

Run the paper-data export:

```bash
python3 scripts/run_paper_experiments.py --out results
```

Run the parameterized model-mode sweeps:

```bash
python3 scripts/run_paper_experiments.py --mode model --out results_model --seed 2026
```

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Outputs

The export script writes:

- `summary.json`
- CSV files for each paper table or curve
- PGFPlots-compatible `.tex` fragments for the jamming, sensing, hardware, and QPSK figures

The default `paper` mode reproduces the numerical values currently reported in `main.tex`. The `model` mode uses the same software components with deterministic seeds and calibrated nominal settings so that future experiments can move from manuscript traces to regenerated simulation traces.

## Repository Layout

```text
src/aris_battle/
  channel.py       Acoustic channel and ARIS path model
  config.py        Scenario and environment dataclasses
  experiments.py   Paper-case and model-case experiments
  metrics.py       PRR, SER, detection, and energy metrics
  optimizers.py    ARIS configuration algorithms
  paper_traces.py  Manuscript figure/table values
  plotting.py      CSV and PGFPlots exporters
scripts/
  run_paper_experiments.py
tests/
  test_core.py
```

## Reproducibility Notes

The manuscript reports simulation evidence rather than tank, lake, or field measurements. For submission, authors should keep the random seeds, parameter files, and figure-generation outputs synchronized with the final reported numbers.

