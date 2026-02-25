# Go Parser Box-Depth Static Checker

A static analysis tool that verifies box depth balancing in Go hand-written recursive descent parsers.

## Problem

Go parsers using a custom recursive descent framework track depth via `db.New()` (depth+1) and `db.Wrap()` (depth-1). This tool statically checks that all execution paths from the entry function `f_top` end with box depth == 0.

## How It Works

- **Abstract interpretation** with `DeltaSet` (set of possible depth-delta integers)
- **Worklist-based CFG analysis** per function (handles if/for/switch/break/return/panic)
- **Tarjan SCC + fixed-point iteration** for inter-procedural recursive calls
- **Widening** to prevent divergence on unbounded loops
- Paths ending in `panic()` are discarded

## Usage

```bash
# Install
pip install tree-sitter tree-sitter-go

# Check a Go file (default entry: f_top)
python -m box_checker path/to/parser.go

# Specify entry function
python -m box_checker path/to/parser.go f_my_entry
```

## Testing

```bash
pip install pytest
pytest tests/ -v
```

## Project Structure

```
box_checker/
    model.py       # DeltaSet, CFGNode, FuncCFG, FuncSummary
    go_parser.py   # tree-sitter Go parsing, f_xxx extraction
    cfg.py         # AST -> CFG builder
    analyzer.py    # Dataflow analysis + fixed-point iteration
    main.py        # CLI entry point
tests/
    test_e2e.py    # 11 end-to-end test cases
    testdata/      # Go test fixtures (01-11)
```
