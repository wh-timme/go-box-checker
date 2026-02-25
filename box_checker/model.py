"""Data structures: CFGNode, FuncCFG, DeltaSet, FuncSummary."""

from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# DeltaSet – abstract domain for possible depth-change values
# ---------------------------------------------------------------------------

class DeltaSet:
    """A set of possible depth-delta integers, with TOP = unbounded."""

    __slots__ = ("_values", "_is_top")

    def __init__(self, values: frozenset[int] | None = None, *, top: bool = False):
        if top:
            self._values: frozenset[int] = frozenset()
            self._is_top = True
        else:
            self._values = values if values is not None else frozenset()
            self._is_top = False

    # -- factories --

    @staticmethod
    def bottom() -> DeltaSet:
        return DeltaSet(frozenset())

    @staticmethod
    def single(v: int) -> DeltaSet:
        return DeltaSet(frozenset({v}))

    @staticmethod
    def top() -> DeltaSet:
        return DeltaSet(top=True)

    # -- predicates --

    @property
    def is_top(self) -> bool:
        return self._is_top

    @property
    def is_bottom(self) -> bool:
        return not self._is_top and len(self._values) == 0

    @property
    def values(self) -> frozenset[int]:
        return self._values

    # -- operations --

    def union(self, other: DeltaSet) -> DeltaSet:
        if self._is_top or other._is_top:
            return DeltaSet.top()
        return DeltaSet(self._values | other._values)

    def compose(self, other: DeltaSet) -> DeltaSet:
        """Cartesian sum: {a+b | a in self, b in other}."""
        if self.is_bottom or other.is_bottom:
            return DeltaSet.bottom()
        if self._is_top or other._is_top:
            return DeltaSet.top()
        return DeltaSet(frozenset(a + b for a in self._values for b in other._values))

    def add_scalar(self, n: int) -> DeltaSet:
        if self.is_bottom:
            return DeltaSet.bottom()
        if self._is_top:
            return DeltaSet.top()
        return DeltaSet(frozenset(v + n for v in self._values))

    def widen(self, limit: int = 32) -> DeltaSet:
        """If the set grows too large, widen to TOP."""
        if self._is_top:
            return self
        if len(self._values) > limit:
            return DeltaSet.top()
        return self

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DeltaSet):
            return NotImplemented
        if self._is_top and other._is_top:
            return True
        return self._is_top == other._is_top and self._values == other._values

    def __hash__(self) -> int:
        return hash((self._is_top, self._values))

    def __repr__(self) -> str:
        if self._is_top:
            return "DeltaSet(TOP)"
        if self.is_bottom:
            return "DeltaSet(BOTTOM)"
        return f"DeltaSet({sorted(self._values)})"


# ---------------------------------------------------------------------------
# CFG nodes
# ---------------------------------------------------------------------------

@dataclass
class CFGNode:
    id: int
    label: str = ""          # human-readable
    delta: int = 0           # +1 for New, -1 for Wrap
    call_target: str = ""    # f_xxx call
    is_panic: bool = False
    is_return: bool = False
    succs: list[int] = field(default_factory=list)


@dataclass
class FuncCFG:
    name: str
    entry: int = 0
    exit: int = 0
    nodes: dict[int, CFGNode] = field(default_factory=dict)


@dataclass
class FuncSummary:
    name: str
    delta_set: DeltaSet = field(default_factory=DeltaSet.bottom)
    calls: set[str] = field(default_factory=set)  # direct callees
