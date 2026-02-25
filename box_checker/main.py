"""CLI entry point for box_checker."""

from __future__ import annotations

import sys
from pathlib import Path

from .go_parser import parse_file, extract_functions
from .cfg import CFGBuilder
from .analyzer import verify


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m box_checker <file.go> [entry_func]")
        sys.exit(1)

    go_file = Path(sys.argv[1])
    entry = sys.argv[2] if len(sys.argv) > 2 else "f_top"

    if not go_file.exists():
        print(f"Error: {go_file} not found")
        sys.exit(1)

    root = parse_file(go_file)
    funcs = extract_functions(root)

    if not funcs:
        print("No f_xxx functions found.")
        sys.exit(1)

    cfgs = {}
    for name, node in funcs.items():
        builder = CFGBuilder()
        cfgs[name] = builder.build(node)

    ok, msg = verify(cfgs, entry)
    print(msg)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
