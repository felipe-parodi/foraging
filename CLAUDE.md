# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research data analysis project for human foraging behavior studies, focused on ADHD research. The project processes behavioral task data from two studies:
- **fADHD**: Adult ADHD foraging task (464 final participants from 510 initial)
- **AMPLIO**: Foraging behavior study (208 final participants from 241 initial)

## Architecture

The project follows a notebook-driven data processing pipeline:

```
Raw Data (data/raw/) → Preprocessing Notebooks (scripts/) → Processed Data (data/processed/, amplio/) → Analysis (methods.ipynb) → Figures (results/figures/)
```

**No build system, tests, or linting** - this is a Jupyter notebook-based research project.

## Running Notebooks

Execute notebooks in this order:
1. `scripts/foraging_preprocessing.ipynb` - fADHD data cleaning (steps 1-3)
2. `scripts/amplio_processing.ipynb` - AMPLIO data cleaning (steps 3-10)
3. `scripts/FRGEADHD_fixserialorder.ipynb` - Fix serial order issues
4. `scripts/methods.ipynb` - Statistical analysis and figure generation
5. `scripts/check_work.ipynb` - Validation/QA

Dependencies: `pandas`, `numpy`, `matplotlib`

## Data Processing Steps

### fADHD Pipeline
1. Load 494 trials, match with 488 survey participants
2. Filter to 464 valid IDs
3. Remove invalid patches (final bush removed if last decision != 0)

### AMPLIO Pipeline
- Convert decisions to 0/1 (explore/exploit), time to seconds
- Remove individuals with no exploit decisions (23 removed)
- Remove final bushes of all blocks
- Filter to participants with ≥25 decisions

## Key Data Columns

| Column | Description |
|--------|-------------|
| ID | Participant identifier (Prolific ID format) |
| Block | Experimental block (1-4 for fADHD, 1-2 for AMPLIO) |
| Bush | Patch/location number within block |
| Round | Trial number within patch |
| Decision | 0=explore (leave patch), 1=exploit (stay) |
| TotalTime_sec | Cumulative time in seconds |
| RT | Reaction time in milliseconds |
| BerryCount | Reward measure |

## Exclusion Criteria

Participants excluded if:
- Survey data doesn't match task data
- No switch (explore) decisions OR no stay (exploit) decisions
- Fewer than 25 total trials
- Hyper/hypo-exploitation patterns (manual review)

## File Naming Convention

Processed data files follow step-based naming:
- `frge_adultadhd_step1_494.csv` → `frge_adultadhd_step2.csv` → `frge_adultadhd_step3.csv`
- `AMPLIO_Mar622_3.csv` → `AMPLIO_Mar622_4.csv` → ... → `AMPLIO_Mar622_10.csv`

## Important Notes

- Raw survey data (`total_data_vludwig.xlsx`) is password protected
- Notebooks contain hardcoded absolute paths that may need updating
- The `src/` and `tests/` directories are empty placeholders
- Final datasets: `fADHD_final_groupDF_464.csv`, `464withcreativity.csv`
