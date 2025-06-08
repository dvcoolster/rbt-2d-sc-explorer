# Contributing to RBT-2D-SC-Explorer

Thank you for your interest in improving this project! We welcome contributions from software developers, theorists, clean-room engineers, and experimentalists alike.

---

## Getting Started

1. **Fork** the repository and create your branch from `main`.
2. If you're modifying code, ensure you have the dev dependencies:
   ```bash
   pip install -e .[dev]
   ```
3. **Open an Issue** or pick an item in `PROJECTS.md` and assign yourself.
4. **Create a WIP pull-request** early so we avoid duplicate work.

---

## Pull-request checklist

> Copy-paste this list into every PR description.

```markdown
- [ ] Title starts with feat/fix/docs/test/chore/sim/fab/data
- [ ] Added or updated entry in PROJECTS.md
- [ ] If code: `pytest -q` passes locally
- [ ] If QE data: include README with lattice parameters, k/q meshes
- [ ] If measurement: attach raw CSV + YAML meta (sample, temp, instrument)
```

---

## Coding style

* Follow [PEP8](https://www.python.org/dev/peps/pep-0008/) and keep functions short.
* Add type hints where it clarifies intent.
* Write docstrings for public functions/classes.

---

## Commit Style

Use conventional commits:

```
feat: short imperative summary
fix:  …
docs: …
chore: …
```

Examples:

```
feat: parity-check CLI v1.0
sim: add strain_scan results
```

---

## Tests

* Unit tests live in `tests/` and run with **pytest**.
* Aim for ≥90 % coverage on any new Python file.

---

## Large Data & Binaries

Please do **not** commit data files >100 MB. Put them on OSF/Zenodo and link in `data/README.md`.

---

Thanks again for helping push RBT superconductivity forward! 🚀 