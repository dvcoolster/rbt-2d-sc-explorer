from pathlib import Path
from subprocess import CalledProcessError, run, PIPE
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_phonon_stability.py"
MOCK = ROOT / "tests" / "data" / "mock.dyn"


def test_imaginary_modes():
    """check_phonon_stability should exit 1 on imaginary modes."""
    result = run([sys.executable, str(SCRIPT), str(MOCK)], stdout=PIPE, stderr=PIPE)
    # Expect exit code 1 and warning icon
    assert result.returncode == 1
    assert b"imaginary" in result.stdout.lower()  # sanity check 