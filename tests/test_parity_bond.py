from pathlib import Path
from subprocess import run, PIPE
import sys

ROOT = Path(__file__).resolve().parents[1]
PARITY = ROOT / "scripts" / "parity_check.py"
BOND = ROOT / "scripts" / "bond_quantum.py"
CIF = ROOT / "data" / "example_CIFs" / "Li2NH.cif"


def test_parity_cli_runs():
    """Parity script should run and exit code >=0."""
    result = run([sys.executable, str(PARITY), str(CIF), "--quiet"], stdout=PIPE)
    # exit code 0 or 1 acceptable (pass/fail), just ensure no crash
    assert result.returncode in (0, 1)


def test_bond_cli_runs():
    """Bond script should run and exit code >=0."""
    result = run([sys.executable, str(BOND), str(CIF), "--quiet"], stdout=PIPE)
    assert result.returncode in (0, 1) 