"""Worklist dataflow analysis + inter-procedural fixed-point iteration."""

from __future__ import annotations

from collections import deque

from .model import FuncCFG, DeltaSet, FuncSummary


# ---------------------------------------------------------------------------
# Intra-procedural: worklist analysis for a single function
# ---------------------------------------------------------------------------

def analyze_function(
    cfg: FuncCFG,
    summaries: dict[str, FuncSummary],
    widen_limit: int = 32,
) -> DeltaSet:
    """Compute the DeltaSet at the exit node of *cfg*."""
    # state[node_id] = DeltaSet reaching that node
    state: dict[int, DeltaSet] = {}
    state[cfg.entry] = DeltaSet.single(0)

    worklist: deque[int] = deque([cfg.entry])
    iterations = 0
    max_iterations = len(cfg.nodes) * 50 + 200

    while worklist:
        iterations += 1
        if iterations > max_iterations:
            return DeltaSet.top()

        nid = worklist.popleft()
        node = cfg.nodes[nid]
        cur = state.get(nid, DeltaSet.bottom())

        if cur.is_bottom:
            continue
        if node.is_panic:
            continue  # discard panic paths

        # Compute outgoing delta
        out = cur
        if node.delta != 0:
            out = cur.add_scalar(node.delta)
        if node.call_target:
            callee_sum = summaries.get(node.call_target)
            if callee_sum is not None:
                out = cur.compose(callee_sum.delta_set)
            else:
                # unknown function – treat as delta=0
                pass

        # Propagate to successors
        for sid in node.succs:
            old = state.get(sid, DeltaSet.bottom())
            merged = old.union(out).widen(widen_limit)
            if merged != old:
                state[sid] = merged
                worklist.append(sid)

    return state.get(cfg.exit, DeltaSet.bottom())


# ---------------------------------------------------------------------------
# Tarjan SCC
# ---------------------------------------------------------------------------

def _tarjan_scc(graph: dict[str, set[str]]) -> list[list[str]]:
    index_counter = [0]
    stack: list[str] = []
    on_stack: set[str] = set()
    index_map: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    result: list[list[str]] = []

    def strongconnect(v: str) -> None:
        index_map[v] = index_counter[0]
        lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack.add(v)

        for w in graph.get(v, set()):
            if w not in index_map:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index_map[w])

        if lowlink[v] == index_map[v]:
            component: list[str] = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                component.append(w)
                if w == v:
                    break
            result.append(component)

    for v in graph:
        if v not in index_map:
            strongconnect(v)

    return result


# ---------------------------------------------------------------------------
# Collect callees from a CFG
# ---------------------------------------------------------------------------

def _collect_callees(cfg: FuncCFG) -> set[str]:
    callees: set[str] = set()
    for node in cfg.nodes.values():
        if node.call_target:
            callees.add(node.call_target)
    return callees


# ---------------------------------------------------------------------------
# Whole-program analysis
# ---------------------------------------------------------------------------

def analyze_program(
    cfgs: dict[str, FuncCFG],
    entry: str = "f_top",
    max_rounds: int = 50,
) -> dict[str, FuncSummary]:
    """Compute summaries for all functions reachable from *entry*."""
    # Build call graph
    call_graph: dict[str, set[str]] = {}
    for name, cfg in cfgs.items():
        callees = _collect_callees(cfg)
        # Only keep callees that are known f_xxx functions
        call_graph[name] = callees & cfgs.keys()

    # Ensure all nodes appear in graph
    for name in cfgs:
        call_graph.setdefault(name, set())

    # Compute SCCs in reverse topological order
    sccs = _tarjan_scc(call_graph)

    # Initialize summaries
    summaries: dict[str, FuncSummary] = {}
    for name in cfgs:
        summaries[name] = FuncSummary(
            name=name,
            delta_set=DeltaSet.bottom(),
            calls=call_graph.get(name, set()),
        )

    # Process SCCs (Tarjan returns in reverse topo order)
    for scc in sccs:
        # Bootstrap: set SCC-internal summaries to {0} so recursive calls
        # don't block the first iteration.
        for fname in scc:
            if fname in summaries:
                summaries[fname].delta_set = DeltaSet.single(0)
        for _ in range(max_rounds):
            changed = False
            for fname in scc:
                if fname not in cfgs:
                    continue
                new_ds = analyze_function(cfgs[fname], summaries)
                if new_ds != summaries[fname].delta_set:
                    summaries[fname].delta_set = new_ds
                    changed = True
            if not changed:
                break

    return summaries


def verify(
    cfgs: dict[str, FuncCFG],
    entry: str = "f_top",
) -> tuple[bool, str]:
    """Check that *entry* has delta == {0}. Returns (ok, message)."""
    if entry not in cfgs:
        return False, f"entry function '{entry}' not found"

    summaries = analyze_program(cfgs, entry)
    ds = summaries[entry].delta_set

    if ds.is_top:
        return False, f"{entry}: delta is TOP (unbounded depth changes)"
    if ds.is_bottom:
        return False, f"{entry}: unreachable (all paths panic?)"
    if ds.values == frozenset({0}):
        return True, f"{entry}: OK (delta = {{0}})"
    return False, f"{entry}: FAIL (delta = {sorted(ds.values)})"
