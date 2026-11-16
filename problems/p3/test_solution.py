"""Example cases from the problem statement. Run: uv run pytest problems/p3"""

from solution import solve

EXAMPLES = [
    # ("input", "expected output"),
]


def test_examples():
    for inp, out in EXAMPLES:
        assert solve(inp).strip() == out.strip()
