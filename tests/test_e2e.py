"""End-to-end tests for box_checker."""

from __future__ import annotations

from pathlib import Path

from box_checker.go_parser import parse_file, extract_functions
from box_checker.cfg import CFGBuilder
from box_checker.analyzer import verify

TESTDATA = Path(__file__).parent / "testdata"


def _check(filename: str, entry: str = "f_top") -> tuple[bool, str]:
    root = parse_file(TESTDATA / filename)
    funcs = extract_functions(root)
    cfgs = {}
    for name, node in funcs.items():
        builder = CFGBuilder()
        cfgs[name] = builder.build(node)
    return verify(cfgs, entry)


class TestBalanced:
    def test_01_simple_balanced(self):
        ok, _ = _check("01_simple_balanced.go")
        assert ok

    def test_03_cross_function(self):
        ok, _ = _check("03_cross_function.go")
        assert ok

    def test_05_recursive(self):
        ok, _ = _check("05_recursive.go")
        assert ok

    def test_06_loop_balanced(self):
        ok, _ = _check("06_loop_balanced.go")
        assert ok

    def test_08_panic_discard(self):
        ok, _ = _check("08_panic_discard.go")
        assert ok

    def test_09_switch_balanced(self):
        ok, _ = _check("09_switch_balanced.go")
        assert ok

    def test_11_break_in_loop(self):
        ok, _ = _check("11_break_in_loop.go")
        assert ok

    def test_12_loop_nested_balanced(self):
        ok, _ = _check("12_loop_nested_balanced.go")
        assert ok

    def test_15_loop_switch_balanced(self):
        ok, _ = _check("15_loop_switch_balanced.go")
        assert ok


class TestUnbalanced:
    def test_02_simple_unbalanced(self):
        ok, _ = _check("02_simple_unbalanced.go")
        assert not ok

    def test_04_branch_mismatch(self):
        ok, _ = _check("04_branch_mismatch.go")
        assert not ok

    def test_07_loop_unbalanced(self):
        ok, msg = _check("07_loop_unbalanced.go")
        assert not ok

    def test_10_return_mid(self):
        ok, _ = _check("10_return_mid.go")
        assert not ok

    def test_13_loop_nested_unbalanced(self):
        ok, _ = _check("13_loop_nested_unbalanced.go")
        assert not ok

    def test_14_loop_nested_unbalanced(self):
        ok, _ = _check("14_loop_nested_unbalanced.go")
        assert not ok
