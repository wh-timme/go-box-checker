"""Parse Go source with tree-sitter, extract f_xxx function ASTs."""

from __future__ import annotations

from pathlib import Path

import tree_sitter_go as tsgo
from tree_sitter import Language, Parser, Node


GO_LANG = Language(tsgo.language())


def make_parser() -> Parser:
    p = Parser(GO_LANG)
    return p


def parse_file(path: str | Path) -> Node:
    src = Path(path).read_bytes()
    parser = make_parser()
    tree = parser.parse(src)
    return tree.root_node


def parse_source(src: str) -> Node:
    parser = make_parser()
    tree = parser.parse(src.encode())
    return tree.root_node


def extract_functions(root: Node) -> dict[str, Node]:
    """Return {name: function_declaration_node} for all f_xxx funcs."""
    funcs: dict[str, Node] = {}
    for child in root.children:
        if child.type != "function_declaration":
            continue
        name_node = child.child_by_field_name("name")
        if name_node is None:
            continue
        name = name_node.text.decode()
        if name.startswith("f_"):
            funcs[name] = child
    return funcs
