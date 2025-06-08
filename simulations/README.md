# Simulations ⨯ DFPT / EPW Workflows

This folder holds *first-principles* input decks and post-processed data that
bridge the RBT screening (`scripts/`) with quantitative Tc predictions.

```
simulations/
├─ strain_scan/        ← SIM-1 task: ±3 % lattice strain study
├─ doping_scan/        ← SIM-2 task: jellium e-doping series
└─ reference/          ← v1 DFPT decks used in README quick-start
```

* **Do not** commit raw `*.save/` or `*.xml` directories—too heavy.
* Keep each sub-folder self-contained with:
  * `README.md` (k-mesh, q-mesh, pseudopotentials)
  * `scf.in`, `ph.in`, optional `epw.in`
  * `post/`  – processed CSVs / PNGs ready for GitHub view.
* If files >100 MB → upload to Zenodo/OSF and link.

---

## Reference decks

`reference/` contains minimal SCF + PH inputs for Li₂NH **2 × 2 × 1** cell so
CI can finish in <5 min.

---

Happy crunching! 🔬⚛️ 