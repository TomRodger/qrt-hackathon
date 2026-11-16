"""Example cases from the problem statement. Run: uv run pytest problems/bonus"""

from solution import solve

EXAMPLES = [
    # ("input", "expected output"),
]


def test_examples():
    for inp, out in EXAMPLES:
        assert solve(inp).strip() == out.strip()
