"""Build CFG from Go function AST (tree-sitter nodes)."""

from __future__ import annotations

from tree_sitter import Node

from .model import CFGNode, FuncCFG


class CFGBuilder:
    """Builds a CFG for a single Go function."""

    def __init__(self) -> None:
        self._next_id = 0
        self._nodes: dict[int, CFGNode] = {}
        self._break_targets: list[int] = []

    def _new_node(self, label: str = "", **kw) -> CFGNode:
        nid = self._next_id
        self._next_id += 1
        n = CFGNode(id=nid, label=label, **kw)
        self._nodes[nid] = n
        return n

    def build(self, func_node: Node) -> FuncCFG:
        name_node = func_node.child_by_field_name("name")
        name = name_node.text.decode() if name_node else "?"
        body = func_node.child_by_field_name("body")

        entry = self._new_node(f"{name}_entry")
        exit_n = self._new_node(f"{name}_exit")

        if body is None:
            entry.succs.append(exit_n.id)
        else:
            stmts = self._extract_stmts(body)
            tails = self._build_block(stmts, entry, exit_n)
            for t in tails:
                if t != exit_n.id:
                    self._nodes[t].succs.append(exit_n.id)

        return FuncCFG(
            name=name, entry=entry.id, exit=exit_n.id, nodes=self._nodes
        )

    @staticmethod
    def _extract_stmts(block: Node) -> list[Node]:
        """Extract statements from a block, unwrapping statement_list."""
        result: list[Node] = []
        for c in block.children:
            if c.type in ("{", "}"):
                continue
            if c.type == "statement_list":
                result.extend(c.children)
            else:
                result.append(c)
        return result

    # ---------------------------------------------------------------
    # Block / statement list
    # ---------------------------------------------------------------

    def _build_block(
        self, stmts: list[Node], pred: CFGNode, exit_n: CFGNode
    ) -> list[int]:
        """Process a list of statements. Returns list of tail node ids."""
        tails = [pred.id]
        for stmt in stmts:
            if not tails:
                break
            new_tails: list[int] = []
            for t in tails:
                new_tails.extend(self._build_stmt(stmt, t, exit_n))
            tails = new_tails
        return tails

    def _build_stmt(
        self, node: Node, pred_id: int, exit_n: CFGNode
    ) -> list[int]:
        """Dispatch a single statement. Returns tail node ids."""
        t = node.type
        if t == "if_statement":
            return self._build_if(node, pred_id, exit_n)
        if t == "for_statement":
            return self._build_for(node, pred_id, exit_n)
        if t in ("expression_switch_statement",):
            return self._build_switch(node, pred_id, exit_n)
        if t == "return_statement":
            return self._build_return(node, pred_id, exit_n)
        if t == "break_statement":
            return self._build_break(pred_id)
        if t == "block":
            inner = self._extract_stmts(node)
            pred_node = self._nodes[pred_id]
            return self._build_block(inner, pred_node, exit_n)
        if t in ("expression_statement", "short_var_declaration",
                  "assignment_statement", "var_declaration"):
            return self._build_expr_stmt(node, pred_id)
        # Ignore other statement types (comments, etc.)
        return [pred_id]

    # ---------------------------------------------------------------
    # Expression statements – detect db.New / db.Wrap / f_xxx / panic
    # ---------------------------------------------------------------

    def _build_expr_stmt(self, node: Node, pred_id: int) -> list[int]:
        calls = self._find_calls(node)
        cur = pred_id
        for call_text, call_node in calls:
            if call_text == "panic":
                n = self._new_node("panic", is_panic=True)
                self._nodes[cur].succs.append(n.id)
                return []  # dead end
            elif call_text == "db.New":
                n = self._new_node("db.New", delta=1)
                self._nodes[cur].succs.append(n.id)
                cur = n.id
            elif call_text == "db.Wrap":
                n = self._new_node("db.Wrap", delta=-1)
                self._nodes[cur].succs.append(n.id)
                cur = n.id
            elif call_text.startswith("f_"):
                n = self._new_node(f"call:{call_text}", call_target=call_text)
                self._nodes[cur].succs.append(n.id)
                cur = n.id
        return [cur]

    def _find_calls(self, node: Node) -> list[tuple[str, Node]]:
        """Recursively find call_expression nodes, return (callee_text, node)."""
        results: list[tuple[str, Node]] = []
        if node.type == "call_expression":
            fn = node.child_by_field_name("function")
            if fn:
                results.append((fn.text.decode(), node))
        for child in node.children:
            results.extend(self._find_calls(child))
        return results

    # ---------------------------------------------------------------
    # if / else
    # ---------------------------------------------------------------

    def _build_if(
        self, node: Node, pred_id: int, exit_n: CFGNode
    ) -> list[int]:
        cond_node = self._new_node("if_cond")
        self._nodes[pred_id].succs.append(cond_node.id)

        tails: list[int] = []

        # then branch
        consequence = node.child_by_field_name("consequence")
        if consequence:
            inner = self._extract_stmts(consequence)
            tails.extend(self._build_block(inner, cond_node, exit_n))

        # else branch
        alternative = node.child_by_field_name("alternative")
        if alternative:
            # "else { ... }" or "else if { ... }"
            if alternative.type == "block":
                inner = self._extract_stmts(alternative)
                tails.extend(self._build_block(inner, cond_node, exit_n))
            else:
                # else if ...
                tails.extend(self._build_stmt(alternative, cond_node.id, exit_n))
        else:
            # no else: cond falls through
            tails.append(cond_node.id)

        return tails

    # ---------------------------------------------------------------
    # return
    # ---------------------------------------------------------------

    def _build_return(
        self, node: Node, pred_id: int, exit_n: CFGNode
    ) -> list[int]:
        ret = self._new_node("return", is_return=True)
        self._nodes[pred_id].succs.append(ret.id)
        ret.succs.append(exit_n.id)
        return []  # no fall-through

    # ---------------------------------------------------------------
    # break
    # ---------------------------------------------------------------

    def _build_break(self, pred_id: int) -> list[int]:
        if self._break_targets:
            self._nodes[pred_id].succs.append(self._break_targets[-1])
        return []  # no fall-through

    # ---------------------------------------------------------------
    # for loop
    # ---------------------------------------------------------------

    def _build_for(
        self, node: Node, pred_id: int, exit_n: CFGNode
    ) -> list[int]:
        loop_head = self._new_node("for_head")
        loop_exit = self._new_node("for_exit")
        self._nodes[pred_id].succs.append(loop_head.id)

        # 0-iteration path
        loop_head.succs.append(loop_exit.id)

        body = node.child_by_field_name("body")
        if body:
            self._break_targets.append(loop_exit.id)
            inner = self._extract_stmts(body)
            tails = self._build_block(inner, loop_head, exit_n)
            self._break_targets.pop()
            # back-edge
            for t in tails:
                self._nodes[t].succs.append(loop_head.id)

        return [loop_exit.id]

    # ---------------------------------------------------------------
    # switch / case
    # ---------------------------------------------------------------

    def _build_switch(
        self, node: Node, pred_id: int, exit_n: CFGNode
    ) -> list[int]:
        switch_node = self._new_node("switch")
        self._nodes[pred_id].succs.append(switch_node.id)

        tails: list[int] = []
        has_default = False

        for child in node.children:
            if child.type not in (
                "expression_case", "default_case",
                "expression_case_clause", "default_case_clause",
            ):
                continue
            if child.type in ("default_case", "default_case_clause"):
                has_default = True
            # case body: extract statements from statement_list children
            body_stmts: list[Node] = []
            for c in child.children:
                if c.type == "statement_list":
                    body_stmts.extend(c.children)
                elif c.type not in ("case", "default", ":", ",", "expression_list"):
                    body_stmts.append(c)
            tails.extend(self._build_block(body_stmts, switch_node, exit_n))

        if not has_default:
            tails.append(switch_node.id)

        return tails
