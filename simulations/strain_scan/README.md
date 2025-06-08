# Strain-scan – Li₂NH

This directory holds the ±3 % *biaxial* strain study used to evaluate the
sensitivity of λ (electron–phonon coupling) and predicted Tc to epitaxial
strain before committing to wafer-level growth.

| Folder / file              | Purpose                                   |
|----------------------------|-------------------------------------------|
| `inputs/`                  | Auto-generated QE `scf.in` / `ph.in` decks |
| `post/`                    | Parsed CSV (`lambda_vs_strain.csv`) + PNG |
| `run_strain_scan.py`       | Helper script – writes inputs & SLURM file |

---

## Strain grid

```
ε = −3 %, −2 %, −1 %, 0 %, +1 %, +2 %, +3 %
```

The *a* and *b* lattice parameters of Li₂NH are scaled as `a = a₀(1+ε)`,
`b = b₀(1+ε)` while **keeping c = 20 Å** to preserve 2-D character.

---

## Workflow

```bash
# 1. Generate input decks (7 folders)
python run_strain_scan.py --a0 3.520 --b0 3.520 --c 20.0 --eps -3 -2 -1 0 1 2 3

# 2. Submit QE jobs (example SLURM)
for d in strain_*; do (cd $d && sbatch qe_ph.slurm); done

# 3. After completion – extract λ and plot
python run_strain_scan.py --post
```

`lambda_vs_strain.png` is committed ( ≤100 kB) so GitHub renders the plot.

---

## To-do

* [ ] Generate decks & push initial PNG
* [ ] Update `simulations/README.md` once data lands
* [ ] Reference plot in `PROJECTS.md` (SIM-1) 