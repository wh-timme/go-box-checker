#!/usr/bin/env python3
"""Stress-test generator for box_checker.

Produces multiple Go source files under tests/testdata/stress_*.go
and a single test_stress.py with an EXPECTED manifest.
"""

from __future__ import annotations

import random
from pathlib import Path

TESTDATA = Path(__file__).parent / "testdata"
SEED = 42


# ---------------------------------------------------------------------------
# GoEmitter – helpers for building Go source strings
# ---------------------------------------------------------------------------

class GoEmitter:
    """Incremental Go source builder with indentation management."""

    def __init__(self) -> None:
        self._lines: list[str] = []
        self._indent = 0

    # -- indentation helpers ------------------------------------------------

    def indent(self) -> None:
        self._indent += 1

    def dedent(self) -> None:
        self._indent = max(0, self._indent - 1)

    def _pfx(self) -> str:
        return "\t" * self._indent

    # -- raw emit -----------------------------------------------------------

    def line(self, text: str = "") -> None:
        if text:
            self._lines.append(f"{self._pfx()}{text}")
        else:
            self._lines.append("")

    def blank(self) -> None:
        self._lines.append("")

    # -- Go statements ------------------------------------------------------

    def new(self) -> None:
        self.line("db.New()")

    def wrap(self) -> None:
        self.line("db.Wrap()")

    def call(self, name: str) -> None:
        self.line(f"{name}(db)")

    def panic(self) -> None:
        self.line('panic("discard")')

    def ret(self) -> None:
        self.line("return")

    def brk(self, label: str = "") -> None:
        self.line(f"break {label}" if label else "break")

    def cont(self, label: str = "") -> None:
        self.line(f"continue {label}" if label else "continue")

    # -- blocks -------------------------------------------------------------

    def func_open(self, name: str) -> None:
        self.line(f"func {name}(db *DepthBox) {{")
        self.indent()

    def func_open_bool(self, name: str) -> None:
        self.line(f"func {name}(db *DepthBox) bool {{")
        self.indent()

    def func_close(self) -> None:
        self.dedent()
        self.line("}")

    def if_open(self, cond: str = "cond") -> None:
        self.line(f"if {cond} {{")
        self.indent()

    def else_open(self) -> None:
        self.dedent()
        self.line("} else {")
        self.indent()

    def else_if_open(self, cond: str = "cond") -> None:
        self.dedent()
        self.line(f"}} else if {cond} {{")
        self.indent()

    def block_close(self) -> None:
        self.dedent()
        self.line("}")

    def for_bare_open(self) -> None:
        self.line("for {")
        self.indent()

    def for_cond_open(self, cond: str = "i := 0; i < n; i++") -> None:
        self.line(f"for {cond} {{")
        self.indent()

    def for_call_open(self, fname: str) -> None:
        self.line(f"for {fname}() {{")
        self.indent()

    def labeled_for_bare_open(self, label: str) -> None:
        self.line(f"{label}:")
        self.line("for {")
        self.indent()

    def switch_open(self, expr: str = "mode") -> None:
        self.line(f"switch {expr} {{")

    def case_open(self, val: str) -> None:
        self.line(f"case {val}:")
        self.indent()

    def default_open(self) -> None:
        self.line("default:")
        self.indent()

    def case_close(self) -> None:
        self.dedent()

    def fallthrough(self) -> None:
        self.line("fallthrough")

    # -- output -------------------------------------------------------------

    def build(self) -> str:
        return "\n".join(self._lines) + "\n"

    def reset(self) -> None:
        self._lines.clear()
        self._indent = 0


# ---------------------------------------------------------------------------
# StressGenerator – orchestrates all categories
# ---------------------------------------------------------------------------

class StressGenerator:
    def __init__(self, seed: int = SEED, scale: float = 1.0,
                 body_scale: float = 1.0) -> None:
        self.rng = random.Random(seed)
        self.em = GoEmitter()
        self.scale = scale
        self.body_scale = body_scale
        # {filename: go_source}
        self.go_files: dict[str, str] = {}
        # {func_name: expected_balanced}
        self.expected: dict[tuple[str, str], bool] = {}

    def _n(self, base: int) -> int:
        """Scale a repeat count."""
        return max(1, int(base * self.scale))

    def _b(self, lo: int, hi: int) -> int:
        """Random int in [lo, hi*body_scale]."""
        return self.rng.randint(lo, max(lo, int(hi * self.body_scale)))

    def _register(self, key: tuple[str, str], balanced: bool) -> None:
        self.expected[key] = balanced

    # -- public API ---------------------------------------------------------

    def generate_all(self) -> None:
        self._gen_simple()       # cat 01
        self._gen_if_else()      # cat 02
        self._gen_bare_for()     # cat 03
        self._gen_cond_for()     # cat 04
        self._gen_for_call()     # cat 05
        self._gen_switch()       # cat 06
        self._gen_fallthrough()  # cat 07
        self._gen_panic()        # cat 08
        self._gen_break_continue()  # cat 09
        self._gen_labeled()      # cat 10
        self._gen_return()       # cat 11
        self._gen_nested()       # cat 12
        self._gen_cross_func()   # cat 13
        self._gen_recursive()    # cat 14
        self._gen_mixed()        # cat 15

    def write_go_files(self) -> None:
        for fname, src in self.go_files.items():
            path = TESTDATA / fname
            path.write_text(src, encoding="utf-8")

    def write_test_file(self) -> None:
        lines = [
            '"""Stress tests for box_checker – auto-generated by gen_stress.py."""',
            "",
            "from __future__ import annotations",
            "",
            "from pathlib import Path",
            "",
            "import pytest",
            "",
            "from box_checker.go_parser import parse_file, extract_functions",
            "from box_checker.cfg import CFGBuilder",
            "from box_checker.analyzer import analyze_program",
            "",
            "TESTDATA = Path(__file__).parent / \"testdata\"",
            "",
            "",
            "def _build_cfgs(filename: str) -> dict:",
            "    root = parse_file(TESTDATA / filename)",
            "    funcs = extract_functions(root)",
            "    cfgs = {}",
            "    for name, node in funcs.items():",
            "        cfgs[name] = CFGBuilder().build(node)",
            "    return cfgs",
            "",
            "",
            "# Pre-build CFGs per file and analyze once",
            "_file_summaries: dict[str, dict] = {}",
            "",
            "",
            "def _get_summaries(filename: str) -> dict:",
            "    if filename not in _file_summaries:",
            "        cfgs = _build_cfgs(filename)",
            "        _file_summaries[filename] = analyze_program(cfgs)",
            "    return _file_summaries[filename]",
            "",
            "",
            "def _is_balanced(filename: str, entry: str) -> bool:",
            "    summaries = _get_summaries(filename)",
            "    ds = summaries[entry].delta_set",
            "    return not ds.is_top and not ds.is_bottom and ds.values == frozenset({0})",
            "",
            "",
            "# EXPECTED: {(filename, entry_func): balanced}",
            "EXPECTED: dict[tuple[str, str], bool] = {",
        ]
        for (fname, entry), bal in sorted(self.expected.items()):
            lines.append(f"    (\"{fname}\", \"{entry}\"): {bal},")
        lines += [
            "}",
            "",
            "",
            "@pytest.mark.parametrize(",
            "    \"key,expected\",",
            "    list(EXPECTED.items()),",
            "    ids=[f\"{f}::{e}\" for (f, e) in EXPECTED],",
            ")",
            "def test_stress(key, expected):",
            "    filename, entry = key",
            "    assert _is_balanced(filename, entry) == expected",
            "",
        ]
        out = Path(__file__).parent / "test_stress.py"
        out.write_text("\n".join(lines), encoding="utf-8")

    # -----------------------------------------------------------------------
    # Category generators – each produces a Go file + registers expected
    # -----------------------------------------------------------------------

    def _start_file(self, comment: str = "") -> None:
        self.em.reset()
        self.em.line("package parser")
        if comment:
            self.em.blank()
            self.em.line(f"// {comment}")
        self.em.blank()

    def _finish_file(self, filename: str) -> None:
        self.go_files[filename] = self.em.build()

    # -- helpers for common patterns ----------------------------------------

    def _emit_new_wrap_seq(self, news: int, wraps: int) -> None:
        """Emit a linear sequence of news then wraps."""
        for _ in range(news):
            self.em.new()
        for _ in range(wraps):
            self.em.wrap()

    def _random_var(self) -> str:
        return self.rng.choice(["cond", "ok", "done", "ready", "flag",
                                "found", "valid", "active", "mode_ok"])

    # ===== Cat 01: Simple linear sequences =================================

    def _gen_simple(self) -> None:
        fname = "stress_01_simple.go"
        self._start_file("Stress cat-01: linear sequences")
        idx = 0

        # Balanced: varying lengths of New+Wrap pairs
        for length in range(1, 41):
            name = f"f_s01_bal_{idx:03d}"
            self.em.func_open(name)
            for _ in range(length):
                self.em.new()
            for _ in range(length):
                self.em.wrap()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Unbalanced: more New than Wrap or vice versa
        for _ in range(40):
            name = f"f_s01_unb_{idx:03d}"
            news = self._b(1, 15)
            wraps = self._b(0, 15)
            while news == wraps:
                wraps = self._b(0, 8)
            self.em.func_open(name)
            for _ in range(news):
                self.em.new()
            for _ in range(wraps):
                self.em.wrap()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 02: if/else branches ========================================

    def _gen_if_else(self) -> None:
        fname = "stress_02_if_else.go"
        self._start_file("Stress cat-02: if/else branches")
        idx = 0

        # Balanced: both branches have same delta
        for _ in range(1, 6):
            for _ in range(5):
                name = f"f_s02_bal_{idx:03d}"
                self.em.func_open(name)
                # prefix New
                pre = self._b(0, 3)
                for _ in range(pre):
                    self.em.new()
                # if/else with matching delta in each branch
                self.em.if_open(self._random_var())
                d = self._b(0, 3)
                self._emit_new_wrap_seq(d, d)
                self.em.else_open()
                d2 = self._b(0, 3)
                self._emit_new_wrap_seq(d2, d2)
                self.em.block_close()
                # suffix Wrap to match prefix
                for _ in range(pre):
                    self.em.wrap()
                self.em.func_close()
                self.em.blank()
                self._register((fname, name), True)
                idx += 1

        # Unbalanced: branches have different delta
        for _ in range(25):
            name = f"f_s02_unb_{idx:03d}"
            self.em.func_open(name)
            pre = self._b(0, 3)
            for _ in range(pre):
                self.em.new()
            self.em.if_open(self._random_var())
            # one branch wraps, other doesn't (or different amounts)
            b1_n = self._b(0, 3)
            b1_w = self._b(0, 3)
            self._emit_new_wrap_seq(b1_n, b1_w)
            self.em.else_open()
            b2_n = self._b(0, 3)
            b2_w = self._b(0, 3)
            # Ensure branches differ in net delta
            while (b1_n - b1_w) == (b2_n - b2_w):
                b2_w = self._b(0, 3)
            self._emit_new_wrap_seq(b2_n, b2_w)
            self.em.block_close()
            for _ in range(pre):
                self.em.wrap()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 03: bare for {} =============================================

    def _gen_bare_for(self) -> None:
        fname = "stress_03_bare_for.go"
        self._start_file("Stress cat-03: bare for loops")
        idx = 0

        # Balanced: loop body delta=0, break exits
        for _ in range(self._n(16)):
            name = f"f_s03_bal_{idx:03d}"
            self.em.func_open(name)
            pre = self._b(0, 2)
            for _ in range(pre):
                self.em.new()
            self.em.for_bare_open()
            # balanced body
            d = self._b(1, 4)
            for _ in range(d):
                self.em.new()
            self.em.if_open(self._random_var())
            for _ in range(d):
                self.em.wrap()
            self.em.else_open()
            for _ in range(d):
                self.em.wrap()
            self.em.brk()
            self.em.block_close()
            self.em.block_close()  # for
            for _ in range(pre):
                self.em.wrap()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Unbalanced: loop body has net != 0 on break path
        for _ in range(self._n(14)):
            name = f"f_s03_unb_{idx:03d}"
            self.em.func_open(name)
            self.em.for_bare_open()
            news = self._b(1, 3)
            wraps = self._b(0, 3)
            while news == wraps:
                wraps = self._b(0, 3)
            for _ in range(news):
                self.em.new()
            for _ in range(wraps):
                self.em.wrap()
            self.em.brk()
            self.em.block_close()  # for
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 04: conditional for =========================================

    def _gen_cond_for(self) -> None:
        fname = "stress_04_cond_for.go"
        self._start_file("Stress cat-04: conditional for loops")
        idx = 0

        # Balanced: loop body delta=0
        for _ in range(self._n(16)):
            name = f"f_s04_bal_{idx:03d}"
            self.em.func_open(name)
            pre = self._b(0, 2)
            for _ in range(pre):
                self.em.new()
            self.em.for_cond_open()
            d = self._b(1, 4)
            for _ in range(d):
                self.em.new()
            for _ in range(d):
                self.em.wrap()
            self.em.block_close()  # for
            for _ in range(pre):
                self.em.wrap()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Unbalanced: loop body has net != 0
        for _ in range(self._n(14)):
            name = f"f_s04_unb_{idx:03d}"
            self.em.func_open(name)
            self.em.for_cond_open()
            news = self._b(1, 3)
            wraps = self._b(0, 3)
            while news == wraps:
                wraps = self._b(0, 3)
            for _ in range(news):
                self.em.new()
            for _ in range(wraps):
                self.em.wrap()
            self.em.block_close()  # for
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 05: for + condition function call ===========================

    def _gen_for_call(self) -> None:
        fname = "stress_05_for_call.go"
        self._start_file("Stress cat-05: for with condition function call")
        idx = 0

        # Balanced: condition func delta=0, loop body delta=0
        for _ in range(self._n(10)):
            cond_name = f"f_s05_cond_{idx:03d}"
            name = f"f_s05_bal_{idx:03d}"
            # condition function: balanced
            self.em.func_open_bool(cond_name)
            d = self._b(0, 2)
            for _ in range(d):
                self.em.new()
            for _ in range(d):
                self.em.wrap()
            self.em.line("return false")
            self.em.func_close()
            self.em.blank()
            # main function
            self.em.func_open(name)
            self.em.for_call_open(cond_name)
            bd = self._b(0, 2)
            for _ in range(bd):
                self.em.new()
            for _ in range(bd):
                self.em.wrap()
            self.em.block_close()  # for
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Unbalanced: condition func has delta != 0
        for _ in range(self._n(10)):
            cond_name = f"f_s05_cond_{idx:03d}"
            name = f"f_s05_unb_{idx:03d}"
            # condition function: unbalanced
            self.em.func_open_bool(cond_name)
            news = self._b(1, 2)
            wraps = self._b(0, 2)
            while news == wraps:
                wraps = self._b(0, 2)
            for _ in range(news):
                self.em.new()
            for _ in range(wraps):
                self.em.wrap()
            self.em.line("return false")
            self.em.func_close()
            self.em.blank()
            # main function
            self.em.func_open(name)
            self.em.for_call_open(cond_name)
            self.em.block_close()  # for
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 06: switch/case =============================================

    def _gen_switch(self) -> None:
        fname = "stress_06_switch.go"
        self._start_file("Stress cat-06: switch/case")
        idx = 0

        # Balanced: all cases same net delta
        for ncases in range(2, 6):
            for _ in range(self._n(5)):
                name = f"f_s06_bal_{idx:03d}"
                self.em.func_open(name)
                pre = self._b(0, 2)
                for _ in range(pre):
                    self.em.new()
                self.em.switch_open()
                for c in range(ncases):
                    if c < ncases - 1:
                        self.em.case_open(str(c + 1))
                    else:
                        self.em.default_open()
                    # each case: same net delta = 0
                    d = self._b(0, 3)
                    self._emit_new_wrap_seq(d, d)
                    self.em.case_close()
                self.em.block_close()  # switch
                for _ in range(pre):
                    self.em.wrap()
                self.em.func_close()
                self.em.blank()
                self._register((fname, name), True)
                idx += 1

        # Unbalanced: at least one case has different net delta
        # switch without default → has fallthrough path with delta=0
        for _ in range(self._n(20)):
            name = f"f_s06_unb_{idx:03d}"
            self.em.func_open(name)
            pre = self._b(1, 3)
            for _ in range(pre):
                self.em.new()
            ncases = self.rng.randint(2, 4)
            self.em.switch_open()
            deltas = []
            for c in range(ncases):
                if c < ncases - 1:
                    self.em.case_open(str(c + 1))
                else:
                    self.em.default_open()
                n = self._b(0, 3)
                w = self._b(0, 3)
                self._emit_new_wrap_seq(n, w)
                deltas.append(n - w)
                self.em.case_close()
            self.em.block_close()  # switch
            for _ in range(pre):
                self.em.wrap()
            self.em.func_close()
            self.em.blank()
            # net delta for the function = pre + case_delta - pre
            # balanced iff all case deltas == 0
            all_zero = all(d == 0 for d in deltas)
            self._register((fname, name), all_zero)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 07: fallthrough =============================================

    def _gen_fallthrough(self) -> None:
        fname = "stress_07_fallthrough.go"
        self._start_file("Stress cat-07: fallthrough chains")
        idx = 0

        # Balanced: fallthrough chain with total delta=0 in each reachable path
        for _ in range(self._n(10)):
            name = f"f_s07_bal_{idx:03d}"
            self.em.func_open(name)
            pre = self._b(0, 2)
            for _ in range(pre):
                self.em.new()
            self.em.switch_open()
            # case 1: just fallthrough (delta=0 contribution)
            self.em.case_open("1")
            self.em.fallthrough()
            self.em.case_close()
            # case 2: the actual work
            self.em.case_open("2")
            d = self._b(0, 2)
            self._emit_new_wrap_seq(d, d)
            self.em.case_close()
            # default: panic (discard)
            self.em.default_open()
            self.em.panic()
            self.em.case_close()
            self.em.block_close()  # switch
            for _ in range(pre):
                self.em.wrap()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Unbalanced: fallthrough introduces mismatch
        for _ in range(self._n(10)):
            name = f"f_s07_unb_{idx:03d}"
            self.em.func_open(name)
            pre = self._b(1, 3)
            for _ in range(pre):
                self.em.new()
            self.em.switch_open()
            # case 1: New then fallthrough
            self.em.case_open("1")
            n1 = self._b(1, 2)
            for _ in range(n1):
                self.em.new()
            self.em.fallthrough()
            self.em.case_close()
            # case 2: Wrap (but not enough to offset case1's New + case2's own path)
            self.em.case_open("2")
            w2 = self._b(0, 1)
            for _ in range(w2):
                self.em.wrap()
            self.em.case_close()
            # default: different delta
            self.em.default_open()
            self.em.panic()
            self.em.case_close()
            self.em.block_close()  # switch
            for _ in range(pre):
                self.em.wrap()
            self.em.func_close()
            self.em.blank()
            # case1→case2 path: pre + n1 + w2(-) - pre → net = n1 - w2
            # case2 direct path: pre + w2(-) - pre → net = -w2 (if w2>0) or 0
            # These paths have different deltas unless n1==0
            self._register((fname, name), False)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 08: panic prune =============================================

    def _gen_panic(self) -> None:
        fname = "stress_08_panic.go"
        self._start_file("Stress cat-08: panic path pruning")
        idx = 0

        # Balanced: non-panic path is balanced, panic path is discarded
        for _ in range(self._n(10)):
            name = f"f_s08_bal_{idx:03d}"
            self.em.func_open(name)
            pre = self._b(1, 3)
            for _ in range(pre):
                self.em.new()
            self.em.if_open(self._random_var())
            for _ in range(pre):
                self.em.wrap()
            self.em.else_open()
            self.em.panic()
            self.em.block_close()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Unbalanced: non-panic path itself is unbalanced
        for _ in range(self._n(10)):
            name = f"f_s08_unb_{idx:03d}"
            self.em.func_open(name)
            pre = self._b(1, 3)
            for _ in range(pre):
                self.em.new()
            self.em.if_open(self._random_var())
            wraps = self.rng.randint(0, pre - 1)
            for _ in range(wraps):
                self.em.wrap()
            self.em.else_open()
            self.em.panic()
            self.em.block_close()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 09: break/continue ==========================================

    def _gen_break_continue(self) -> None:
        fname = "stress_09_break_continue.go"
        self._start_file("Stress cat-09: break and continue in loops")
        idx = 0

        # Balanced: break at delta=0, continue at delta=0
        for _ in range(self._n(16)):
            name = f"f_s09_bal_{idx:03d}"
            self.em.func_open(name)
            pre = self._b(0, 2)
            for _ in range(pre):
                self.em.new()
            self.em.for_bare_open()
            d = self._b(1, 3)
            for _ in range(d):
                self.em.new()
            self.em.if_open(self._random_var())
            for _ in range(d):
                self.em.wrap()
            self.em.cont()
            self.em.else_open()
            for _ in range(d):
                self.em.wrap()
            self.em.brk()
            self.em.block_close()
            self.em.block_close()  # for
            for _ in range(pre):
                self.em.wrap()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Unbalanced: continue skips Wrap
        for _ in range(self._n(14)):
            name = f"f_s09_unb_{idx:03d}"
            self.em.func_open(name)
            self.em.for_bare_open()
            d = self._b(1, 3)
            for _ in range(d):
                self.em.new()
            self.em.if_open(self._random_var())
            # continue without wrapping all
            skip = self.rng.randint(0, d - 1)
            for _ in range(skip):
                self.em.wrap()
            self.em.cont()
            self.em.else_open()
            for _ in range(d):
                self.em.wrap()
            self.em.brk()
            self.em.block_close()
            self.em.block_close()  # for
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 10: labeled break/continue ==================================

    def _gen_labeled(self) -> None:
        fname = "stress_10_labeled.go"
        self._start_file("Stress cat-10: labeled break and continue")
        idx = 0

        # Balanced: labeled break exits outer loop at delta=0
        for _ in range(self._n(13)):
            name = f"f_s10_bal_{idx:03d}"
            self.em.func_open(name)
            pre = self._b(0, 2)
            for _ in range(pre):
                self.em.new()
            self.em.labeled_for_bare_open("OUTER")
            d = self._b(1, 3)
            for _ in range(d):
                self.em.new()
            self.em.for_bare_open()
            inner_d = self._b(1, 2)
            for _ in range(inner_d):
                self.em.new()
            self.em.if_open(self._random_var())
            for _ in range(inner_d):
                self.em.wrap()
            for _ in range(d):
                self.em.wrap()
            self.em.brk("OUTER")
            self.em.else_open()
            for _ in range(inner_d):
                self.em.wrap()
            self.em.brk()
            self.em.block_close()
            self.em.block_close()  # inner for
            for _ in range(d):
                self.em.wrap()
            self.em.brk()
            self.em.block_close()  # outer for
            for _ in range(pre):
                self.em.wrap()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Unbalanced: labeled continue skips Wrap
        for _ in range(self._n(12)):
            name = f"f_s10_unb_{idx:03d}"
            self.em.func_open(name)
            self.em.labeled_for_bare_open("OUTER")
            d = self._b(1, 3)
            for _ in range(d):
                self.em.new()
            self.em.for_bare_open()
            inner_d = self._b(1, 2)
            for _ in range(inner_d):
                self.em.new()
            self.em.if_open(self._random_var())
            # continue OUTER without wrapping enough
            skip = self.rng.randint(0, inner_d + d - 1)
            for _ in range(skip):
                self.em.wrap()
            self.em.cont("OUTER")
            self.em.else_open()
            for _ in range(inner_d):
                self.em.wrap()
            self.em.brk()
            self.em.block_close()
            self.em.block_close()  # inner for
            for _ in range(d):
                self.em.wrap()
            self.em.brk()
            self.em.block_close()  # outer for
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 11: early return ============================================

    def _gen_return(self) -> None:
        fname = "stress_11_return.go"
        self._start_file("Stress cat-11: early return")
        idx = 0

        # Balanced: return only at delta=0
        for _ in range(self._n(10)):
            name = f"f_s11_bal_{idx:03d}"
            self.em.func_open(name)
            d = self._b(1, 4)
            for _ in range(d):
                self.em.new()
            self.em.if_open(self._random_var())
            for _ in range(d):
                self.em.wrap()
            self.em.ret()
            self.em.block_close()
            for _ in range(d):
                self.em.wrap()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Unbalanced: return at delta != 0
        for _ in range(self._n(10)):
            name = f"f_s11_unb_{idx:03d}"
            self.em.func_open(name)
            d = self._b(1, 4)
            for _ in range(d):
                self.em.new()
            self.em.if_open(self._random_var())
            self.em.ret()  # return with delta = d != 0
            self.em.block_close()
            for _ in range(d):
                self.em.wrap()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 12: nested loops ============================================

    def _gen_nested(self) -> None:
        fname = "stress_12_nested.go"
        self._start_file("Stress cat-12: nested loops")
        idx = 0

        # Balanced: nested loops all with delta=0 bodies
        for _ in range(self._n(13)):
            name = f"f_s12_bal_{idx:03d}"
            self.em.func_open(name)
            pre = self._b(0, 1)
            for _ in range(pre):
                self.em.new()
            self.em.labeled_for_bare_open("OUTER")
            outer_d = self._b(1, 2)
            for _ in range(outer_d):
                self.em.new()
            # inner loop
            self.em.for_bare_open()
            inner_d = self._b(1, 2)
            for _ in range(inner_d):
                self.em.new()
            self.em.if_open(self._random_var())
            for _ in range(inner_d):
                self.em.wrap()
            self.em.cont()
            self.em.else_open()
            for _ in range(inner_d):
                self.em.wrap()
            self.em.brk()
            self.em.block_close()
            self.em.block_close()  # inner for
            # wrap outer
            self.em.if_open(self._random_var())
            for _ in range(outer_d):
                self.em.wrap()
            self.em.cont()
            self.em.else_open()
            for _ in range(outer_d):
                self.em.wrap()
            self.em.brk()
            self.em.block_close()
            self.em.block_close()  # outer for
            for _ in range(pre):
                self.em.wrap()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Unbalanced: inner continue skips outer Wrap
        for _ in range(self._n(12)):
            name = f"f_s12_unb_{idx:03d}"
            self.em.func_open(name)
            self.em.labeled_for_bare_open("OUTER")
            outer_d = self._b(1, 2)
            for _ in range(outer_d):
                self.em.new()
            self.em.for_bare_open()
            inner_d = self._b(1, 2)
            for _ in range(inner_d):
                self.em.new()
            self.em.if_open(self._random_var())
            for _ in range(inner_d):
                self.em.wrap()
            # continue OUTER skips outer Wrap
            self.em.cont("OUTER")
            self.em.else_open()
            for _ in range(inner_d):
                self.em.wrap()
            self.em.brk()
            self.em.block_close()
            self.em.block_close()  # inner for
            for _ in range(outer_d):
                self.em.wrap()
            self.em.brk()
            self.em.block_close()  # outer for
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 13: cross-function call chains ==============================

    def _gen_cross_func(self) -> None:
        fname = "stress_13_cross_func.go"
        self._start_file("Stress cat-13: cross-function call chains")
        idx = 0

        # Balanced: linear chain where total delta = 0
        for chain_len in range(2, 6):
            for _ in range(self._n(3)):
                helpers = []
                for h in range(chain_len):
                    hname = f"f_s13_h_{idx:03d}_{h}"
                    helpers.append(hname)
                    self.em.func_open(hname)
                    if h < (chain_len + 1) // 2:
                        self.em.new()
                    else:
                        self.em.wrap()
                    self.em.func_close()
                    self.em.blank()

                name = f"f_s13_bal_{idx:03d}"
                self.em.func_open(name)
                for hname in helpers:
                    self.em.call(hname)
                # Compensate if chain_len is odd
                if chain_len % 2 == 1:
                    self.em.wrap()
                self.em.func_close()
                self.em.blank()
                self._register((fname, name), True)
                idx += 1

        # Fan-out balanced
        for fan in range(2, 5):
            name = f"f_s13_bal_{idx:03d}"
            helpers = []
            for h in range(fan):
                hname = f"f_s13_h_{idx:03d}_{h}"
                helpers.append(hname)
                self.em.func_open(hname)
                d = self._b(0, 2)
                self._emit_new_wrap_seq(d, d)
                self.em.func_close()
                self.em.blank()
            self.em.func_open(name)
            for hname in helpers:
                self.em.call(hname)
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Unbalanced: chain has net delta != 0
        for _ in range(self._n(15)):
            helpers = []
            total_delta = 0
            hcount = self.rng.randint(2, 4)
            for h in range(hcount):
                hname = f"f_s13_h_{idx:03d}_{h}"
                helpers.append(hname)
                n = self._b(0, 2)
                w = self._b(0, 2)
                total_delta += (n - w)
                self.em.func_open(hname)
                self._emit_new_wrap_seq(n, w)
                self.em.func_close()
                self.em.blank()

            name = f"f_s13_unb_{idx:03d}"
            self.em.func_open(name)
            for hname in helpers:
                self.em.call(hname)
            # Ensure net != 0: add extra New if currently balanced
            if total_delta == 0:
                self.em.new()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 14: recursive / mutual recursive ============================

    def _gen_recursive(self) -> None:
        fname = "stress_14_recursive.go"
        self._start_file("Stress cat-14: recursive and mutual recursive")
        idx = 0

        # Balanced: direct recursion with base case delta=0
        for _ in range(self._n(10)):
            name = f"f_s14_bal_{idx:03d}"
            self.em.func_open(name)
            self.em.switch_open()
            # base case
            self.em.case_open("1")
            d = self._b(0, 2)
            self._emit_new_wrap_seq(d, d)
            self.em.case_close()
            # recursive case: New + recurse + Wrap
            self.em.default_open()
            self.em.new()
            self.em.call(name)
            self.em.wrap()
            self.em.case_close()
            self.em.block_close()  # switch
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Unbalanced: recursion with net != 0
        for _ in range(self._n(10)):
            name = f"f_s14_unb_{idx:03d}"
            self.em.func_open(name)
            self.em.switch_open()
            # base case: net != 0
            self.em.case_open("1")
            n = self._b(0, 2)
            w = self._b(0, 2)
            while n == w:
                w = self._b(0, 2)
            self._emit_new_wrap_seq(n, w)
            self.em.case_close()
            # recursive case
            self.em.default_open()
            self.em.new()
            self.em.call(name)
            self.em.wrap()
            self.em.case_close()
            self.em.block_close()  # switch
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        # Mutual recursion balanced: A calls B with New+B+Wrap, B calls A with New+A+Wrap
        for _ in range(self._n(5)):
            name_a = f"f_s14_mbal_a_{idx:03d}"
            name_b = f"f_s14_mbal_b_{idx:03d}"
            # A: switch { case 1: base; default: New + B + Wrap }
            self.em.func_open(name_a)
            self.em.switch_open()
            self.em.case_open("1")
            self.em.line("; // base")
            self.em.case_close()
            self.em.default_open()
            self.em.new()
            self.em.call(name_b)
            self.em.wrap()
            self.em.case_close()
            self.em.block_close()
            self.em.func_close()
            self.em.blank()
            # B: switch { case 1: base; default: New + A + Wrap }
            self.em.func_open(name_b)
            self.em.switch_open()
            self.em.case_open("1")
            self.em.line("; // base")
            self.em.case_close()
            self.em.default_open()
            self.em.new()
            self.em.call(name_a)
            self.em.wrap()
            self.em.case_close()
            self.em.block_close()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name_a), True)
            idx += 1

        # Mutual recursion unbalanced
        for _ in range(self._n(5)):
            name_a = f"f_s14_munb_a_{idx:03d}"
            name_b = f"f_s14_munb_b_{idx:03d}"
            # A: New + call B
            self.em.func_open(name_a)
            self.em.switch_open()
            self.em.case_open("1")
            self.em.new()  # base case unbalanced
            self.em.case_close()
            self.em.default_open()
            self.em.new()
            self.em.call(name_b)
            self.em.case_close()
            self.em.block_close()
            self.em.func_close()
            self.em.blank()
            # B: call A (no wrap)
            self.em.func_open(name_b)
            self.em.switch_open()
            self.em.case_open("1")
            self.em.line("; // base")
            self.em.case_close()
            self.em.default_open()
            self.em.call(name_a)
            self.em.case_close()
            self.em.block_close()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name_a), False)
            idx += 1

        self._finish_file(fname)

    # ===== Cat 15: mixed complex ===========================================

    def _gen_mixed(self) -> None:
        fname = "stress_15_mixed.go"
        self._start_file("Stress cat-15: mixed complex scenarios")
        idx = 0

        # Balanced: if + for + switch combined
        for _ in range(self._n(10)):
            name = f"f_s15_bal_{idx:03d}"
            self.em.func_open(name)
            # prefix New
            pre = self._b(1, 3)
            for _ in range(pre):
                self.em.new()
            # if branch with loop inside
            self.em.if_open(self._random_var())
            self.em.for_cond_open()
            ld = self._b(1, 2)
            self._emit_new_wrap_seq(ld, ld)
            self.em.block_close()  # for
            for _ in range(pre):
                self.em.wrap()
            self.em.else_open()
            # switch inside else
            self.em.switch_open()
            self.em.case_open("1")
            d1 = self._b(0, 2)
            self._emit_new_wrap_seq(d1, d1)
            self.em.case_close()
            self.em.default_open()
            d2 = self._b(0, 2)
            self._emit_new_wrap_seq(d2, d2)
            self.em.case_close()
            self.em.block_close()  # switch
            for _ in range(pre):
                self.em.wrap()
            self.em.block_close()  # if
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Unbalanced: mixed constructs with imbalance
        for _ in range(self._n(10)):
            name = f"f_s15_unb_{idx:03d}"
            self.em.func_open(name)
            pre = self._b(1, 3)
            for _ in range(pre):
                self.em.new()
            self.em.if_open(self._random_var())
            # loop with continue skipping wrap
            self.em.for_bare_open()
            self.em.new()
            self.em.if_open(self._random_var())
            self.em.cont()  # skip Wrap
            self.em.block_close()
            self.em.wrap()
            self.em.brk()
            self.em.block_close()  # for
            for _ in range(pre):
                self.em.wrap()
            self.em.else_open()
            # switch with mismatched cases
            self.em.switch_open()
            self.em.case_open("1")
            for _ in range(pre):
                self.em.wrap()
            self.em.case_close()
            self.em.default_open()
            wraps = self.rng.randint(0, max(0, pre - 1))
            for _ in range(wraps):
                self.em.wrap()
            self.em.case_close()
            self.em.block_close()  # switch
            self.em.block_close()  # if
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        # Mixed with cross-function calls (balanced)
        for _ in range(self._n(5)):
            helper = f"f_s15_h_{idx:03d}"
            self.em.func_open(helper)
            d = self._b(0, 2)
            self._emit_new_wrap_seq(d, d)
            self.em.func_close()
            self.em.blank()

            name = f"f_s15_bal_{idx:03d}"
            self.em.func_open(name)
            self.em.new()
            self.em.call(helper)
            self.em.if_open(self._random_var())
            self.em.wrap()
            self.em.else_open()
            self.em.wrap()
            self.em.block_close()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), True)
            idx += 1

        # Mixed with cross-function calls (unbalanced)
        for _ in range(self._n(5)):
            helper = f"f_s15_h_{idx:03d}"
            self.em.func_open(helper)
            self.em.new()
            self.em.func_close()
            self.em.blank()

            name = f"f_s15_unb_{idx:03d}"
            self.em.func_open(name)
            self.em.new()
            self.em.call(helper)
            self.em.if_open(self._random_var())
            self.em.wrap()
            self.em.else_open()
            self.em.wrap()
            self.em.block_close()
            self.em.func_close()
            self.em.blank()
            self._register((fname, name), False)
            idx += 1

        self._finish_file(fname)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    gen = StressGenerator(seed=SEED, scale=1.8, body_scale=2.5)
    gen.generate_all()
    gen.write_go_files()
    gen.write_test_file()

    # Summary
    total_funcs = len(gen.expected)
    balanced = sum(1 for v in gen.expected.values() if v)
    unbalanced = total_funcs - balanced
    print(f"Generated {len(gen.go_files)} Go files with {total_funcs} test entries")
    print(f"  Balanced: {balanced}, Unbalanced: {unbalanced}")
    for fname in sorted(gen.go_files):
        lines = gen.go_files[fname].count("\n")
        funcs_in = sum(1 for (f, _) in gen.expected if f == fname)
        print(f"  {fname}: {lines} lines, {funcs_in} entries")


if __name__ == "__main__":
    main()
