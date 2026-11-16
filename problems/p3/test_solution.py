"""Example cases from the problem statement. Run: uv run pytest problems/p3"""

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("sol_p3", Path(__file__).with_name("solution.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
solve = _mod.solve

EXAMPLES = [
    # ("input", "expected output"),
]


def test_examples():
    for inp, out in EXAMPLES:
        assert solve(inp).strip() == out.strip()
