# RBT-2D-SC-Explorer – Engineering Kan-ban

> **Purpose**: One-page snapshot for every contributor—software, theory,
> fabrication, characterization—to know exactly what to do **next** so the
> repository becomes a turnkey package Prof. Deep Jariwala's lab can clone,
> run, fabricate, measure, and publish.

---

## 0 Current repo snapshot

```text
.
├─ README.md                ← ok, but missing quick video GIF
├─ environment.yml          ← good
├─ docs/                    ← parity primer + fab SOPs
├─ scripts/                 ← parity_check.py, bond_quantum.py, …
├─ simulations/             ← v1 DFPT decks
├─ fab_protocols/           ← PDF duplicates of docs
├─ data/                    ← example_CIFs/ only
└─ .github/                 ← issue templates (new_sample, measurement)
```

---

## 1 Kan-ban board

Paste new rows in PRs; **do not** reorder without discussion.

| 🏷️ Label                            | Owner          | Deliverable (PR title)                      | Definition of "done"                                                                                      |
| ------------------------------------ | -------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **CORE-1** <br>*CLI polish*          | software       | **`feat: parity-check CLI v1.0`**           | `parity_check.py` becomes `rbt-parity` entry-point, `pip install -e .` works, README quick-start updated. |
| **CORE-2** <br>*Unit tests*          | software       | **`test: pytest parity & bond`**            | GitHub Action running `pytest`, ≥90 % coverage on `scripts/`.                                             |
| **DOC-1** <br>*Fab flowchart*        | doc            | **`docs: add Li2NH flowchart.svg`**         | One-page SVG inserted into `docs/01_fab_protocol_Li2NH.md`.                                               |
| **SIM-1** <br>*Strain scan*          | sim-student    | **`sim: add strain_scan results`**          | `simulations/strain_scan/` folder + CSV + `lambda_vs_strain.png`; `issue #12` auto-generated.             |
| **SIM-2** <br>*Doping scan*          | sim-student    | **`sim: doping_scan data`**                 | Same for +0.1 e … +0.8 e jellium; update notebook.                                                        |
| **SIM-3** <br>*Phonon sanity script* | sim-student    | **`feat: check_phonon_stability.py`**       | Reads QE `.dyn*`, prints ✅/⚠️, unit-tested.                                                               |
| **DATA-1** <br>*MESA results sheet*  | experi-postdoc | **`data: add Li2NH_Hallbar1_RvsT.csv`**     | Raw 4-probe CSV + metadata YAML in `data/measurements/`; GitHub issue auto-linked.                        |
| **APP-1** <br>*Plot dashboard*       | software       | **`feat: tc_dashboard.ipynb`**              | Jupyter nb that ingests any measurement CSV and overlays DFPT Tc. Binder badge works.                     |
| **SEC-1** <br>*LICENSE & CITATION*   | maintainer     | **`chore: add MIT license & CITATION.cff`** | Files added; repo ready for Zenodo DOI.                                                                   |
| **CI-1** <br>*QE smoke test*         | sim-devops     | **`ci: GH-action quantum-espresso`**        | Minimal QE container; runs `pw.x -in tests/min.scf.in` in <5 min.                                         |
| **FAB-1** <br>*Mask GDS*             | fab-engineer   | **`fab: Li2NH_hallbar50um.gds`**            | GDSII in `fab_protocols/masks/`; pull dimensions into SOP.                                                |
| **EVERYONE**                         | all            | **`README: add usage GIF & contact`**       | 30-sec asciinema or GIF demo; badge to Slack / Matrix invite.                                             |

> **Legend**  
> CORE = python package polish SIM = QE & EPW work DATA = real-world measurements  
> FAB = clean-room artefacts DOC = written docs CI = automation SEC = legal/credit

---

## 2 Immediate priorities (week-1 sprint)

1. **CORE-1 & CORE-2** – turnkey CLI + tests → shows project is real software.
2. **SIM-1** – strain scan; gives Jariwala a classical Tc-vs-lattice plot **before** sputtering.
3. **DOC-1** – printable flow-chart PDF the clean-room tech can pin above the glovebox.

---

## 3 Pull-request checklist (append to CONTRIBUTING.md)

```markdown
- [ ] Title starts with feat/fix/docs/test/chore/sim/fab/data
- [ ] Added or updated entry in PROJECTS.md
- [ ] If code: `pytest -q` passes locally
- [ ] If QE data: include README with lattice parameters, k/q meshes
- [ ] If measurement: attach raw CSV + YAML meta (sample, temp, instrument)
```

---

## 4 What **not** to add yet 🛑

* No Graphane-Li SOP until Li₂NH result is known.
* No RBT math PDFs—keep repo *agnostic* for conventional reviewers.
* No heavy data (>100 MB) in Git; point to OSF/Zenodo when real measurement files appear.

---

### 📣 Copy-paste footer for Slack / e-mail

> "I've pushed **PROJECTS.md** with a kan-ban of twelve bite-size tasks. Finish CORE-1, CORE-2, SIM-1 this week and we're demo-ready. Grab an issue, assign yourself, and open a WIP PR before coding so we stay non-overlapping. Thanks everyone!" 