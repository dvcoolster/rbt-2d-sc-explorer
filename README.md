# RBT Parity Super-Conductor Explorer

**Goal:** Verify (or falsify) the claim that certain 2-D hydride films become superconducting above 300 K **at 1 bar** if and only if:

```
[ K = 0  AND  ħω*/π ≥ 0.081 eV ]
```

This repository provides a complete workflow for Prof. Deep Jariwala's lab (or any 2-D materials lab) to:

1. **Screen 2-D heterostructures** by the RBT parity rule in minutes
2. **Fabricate & cap** the three top candidates with existing lab tools  
3. **Measure** room-temperature superconductivity with one four-probe sweep

## Quick Start

```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate rbt_sc

# Test the parity checker on example structures
python scripts/parity_check.py data/example_CIFs/Li2NH.cif
python scripts/bond_quantum.py data/example_CIFs/Li2NH.cif

# If both pass ✅, follow fabrication protocols
# 1. docs/01_fab_protocol_Li2NH.md
# 2. docs/03_measurement_playbook.md
```

## Repository Structure

```
rbt-2d-sc-explorer/
├─ README.md                     # This file
├─ environment.yml               # Conda environment with pymatgen, ASE, QE-tools
├─ docs/                         # Documentation and protocols
│   ├─ 00_rbt_parity_primer.pdf
│   ├─ 01_fab_protocol_Li2NH.md
│   ├─ 02_fab_protocol_Graphane_Li.md
│   └─ 03_measurement_playbook.md
├─ scripts/                      # Core analysis tools
│   ├─ parity_check.py           # K = 0 test on CIF/POSCAR
│   ├─ bond_quantum.py           # ħω*/π estimator from bond lengths
│   ├─ qe_builder.py             # Auto-generate QE input for phonons
│   └─ tc_plot.ipynb             # Jupyter: Tc vs bond length dashboard
├─ fab_protocols/                # Clean-room ready protocols
├─ data/                         # Example structures and templates
│   ├─ example_CIFs/             # Li2NH, Li4NH, B9H6, etc.
│   └─ results_template.xlsx
└─ .github/                      # Issue templates for reproducibility
    └─ ISSUE_TEMPLATE/
        ├─ new_sample.yml
        └─ measurement_report.yml
```

## The RBT Parity Rule

The **Replication-Based Theory (RBT)** predicts room-temperature superconductivity in 2-D materials when:

1. **Parity condition**: K = 0 (even number of odd-degree vertices in the crystal graph)
2. **Energy condition**: ħω*/π ≥ 0.081 eV (minimum phonon coupling threshold)

## Lab Workflow

| Day | Action | Tool |
|-----|--------|------|
| 1 | Screen candidates with parity/energy check | `parity_check.py`, `bond_quantum.py` |
| 2-3 | Fabricate top candidate (e.g., Li₂NH) | `01_fab_protocol_Li2NH.md` |
| 4 | Pattern and measure 4-probe resistance | `03_measurement_playbook.md` |
| 5 | Analyze results: R(T) < 10 nΩ @ 350K = SUCCESS | GitHub issue template |

## Expected Results

**Success criteria**: Resistance drops to ≤ 10 nΩ and stays flat from 300-350K
**Publication timeline**: If successful, submit to Nature within 1 week

## Citation

If this repository contributes to your research, please cite:
```
RBT-2D-SC-Explorer: Rapid screening and fabrication toolkit for 
room-temperature 2-D superconductors based on parity analysis.
GitHub: https://github.com/[your-username]/rbt-2d-sc-explorer
```

## Contact

For questions about implementation or results, please open a GitHub issue using the provided templates. 