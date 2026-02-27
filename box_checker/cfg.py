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
        self._continue_targets: list[int] = []
        self._label_break_targets: dict[str, int] = {}
        self._label_continue_targets: dict[str, int] = {}

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
            return self._build_break(node, pred_id)
        if t == "continue_statement":
            return self._build_continue(node, pred_id)
        if t == "labeled_statement":
            return self._build_labeled(node, pred_id, exit_n)
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
    # break / continue (label-aware)
    # ---------------------------------------------------------------

    @staticmethod
    def _stmt_label(node: Node) -> str | None:
        for child in node.children:
            if child.type == "label_name":
                return child.text.decode()
        return None

    def _build_break(self, node: Node, pred_id: int) -> list[int]:
        label = self._stmt_label(node)
        if label and label in self._label_break_targets:
            target = self._label_break_targets[label]
        elif self._break_targets:
            target = self._break_targets[-1]
        else:
            return []
        self._nodes[pred_id].succs.append(target)
        return []

    def _build_continue(self, node: Node, pred_id: int) -> list[int]:
        label = self._stmt_label(node)
        if label and label in self._label_continue_targets:
            target = self._label_continue_targets[label]
        elif self._continue_targets:
            target = self._continue_targets[-1]
        else:
            return []
        self._nodes[pred_id].succs.append(target)
        return []

    # ---------------------------------------------------------------
    # labeled statement
    # ---------------------------------------------------------------

    def _build_labeled(
        self, node: Node, pred_id: int, exit_n: CFGNode
    ) -> list[int]:
        label: str | None = None
        inner_stmt: Node | None = None
        for child in node.children:
            if child.type == "label_name":
                label = child.text.decode()
            elif child.type != ":":
                inner_stmt = child
        if inner_stmt is None:
            return [pred_id]
        if inner_stmt.type == "for_statement" and label:
            return self._build_for(inner_stmt, pred_id, exit_n, label=label)
        if inner_stmt.type == "expression_switch_statement" and label:
            return self._build_switch(inner_stmt, pred_id, exit_n, label=label)
        return self._build_stmt(inner_stmt, pred_id, exit_n)

    # ---------------------------------------------------------------
    # for loop
    # ---------------------------------------------------------------

    def _build_for(
        self, node: Node, pred_id: int, exit_n: CFGNode, label: str | None = None
    ) -> list[int]:
        loop_head = self._new_node("for_head")
        loop_exit = self._new_node("for_exit")
        self._nodes[pred_id].succs.append(loop_head.id)

        # Determine if this is a bare `for {}` (no condition)
        has_condition = False
        cond_calls: list[tuple[str, Node]] = []
        for child in node.children:
            if child.type == "for_clause":
                has_condition = True
                break
            if child.type in ("call_expression", "identifier", "binary_expression",
                              "unary_expression", "parenthesized_expression",
                              "selector_expression"):
                # `for f_cond() {}` or `for cond {}`
                if child.type != "block":
                    has_condition = True
                    cond_calls = self._find_calls(child)
                break
            if child.type == "block":
                # `for { ... }` – bare loop, no condition before block
                break

        # Process condition calls at loop_head
        cond_tail = loop_head.id
        for call_text, call_node in cond_calls:
            if call_text.startswith("f_"):
                n = self._new_node(f"call:{call_text}", call_target=call_text)
                self._nodes[cond_tail].succs.append(n.id)
                cond_tail = n.id

        # 0-iteration path: only if there's a condition that can be false
        if has_condition:
            self._nodes[cond_tail].succs.append(loop_exit.id)

        body = node.child_by_field_name("body")
        if body:
            if label:
                self._label_break_targets[label] = loop_exit.id
                self._label_continue_targets[label] = loop_head.id
            self._break_targets.append(loop_exit.id)
            self._continue_targets.append(loop_head.id)
            inner = self._extract_stmts(body)
            body_entry = self._new_node("for_body")
            self._nodes[cond_tail].succs.append(body_entry.id)
            tails = self._build_block(inner, body_entry, exit_n)
            self._continue_targets.pop()
            self._break_targets.pop()
            if label:
                del self._label_break_targets[label]
                del self._label_continue_targets[label]
            # back-edge
            for t in tails:
                self._nodes[t].succs.append(loop_head.id)

        return [loop_exit.id]

    # ---------------------------------------------------------------
    # switch / case
    # ---------------------------------------------------------------

    def _build_switch(
        self, node: Node, pred_id: int, exit_n: CFGNode,
        label: str | None = None,
    ) -> list[int]:
        switch_node = self._new_node("switch")
        switch_exit = self._new_node("switch_exit")
        self._nodes[pred_id].succs.append(switch_node.id)

        # In Go, break inside switch exits the switch
        self._break_targets.append(switch_exit.id)
        if label:
            self._label_break_targets[label] = switch_exit.id

        tails: list[int] = []
        has_default = False

        # Collect all cases in order for fallthrough handling
        cases: list[Node] = []
        for child in node.children:
            if child.type in (
                "expression_case", "default_case",
                "expression_case_clause", "default_case_clause",
            ):
                cases.append(child)
                if child.type in ("default_case", "default_case_clause"):
                    has_default = True

        for i, case_node in enumerate(cases):
            body_stmts: list[Node] = []
            has_fallthrough = False
            for c in case_node.children:
                if c.type == "statement_list":
                    for s in c.children:
                        if s.type == "fallthrough_statement":
                            has_fallthrough = True
                        else:
                            body_stmts.append(s)
                elif c.type not in ("case", "default", ":", ",", "expression_list"):
                    body_stmts.append(c)

            case_tails = self._build_block(body_stmts, switch_node, exit_n)

            if has_fallthrough and i + 1 < len(cases):
                # Fallthrough: connect tails to next case's body
                next_case = cases[i + 1]
                next_stmts: list[Node] = []
                next_has_ft = False
                for c in next_case.children:
                    if c.type == "statement_list":
                        for s in c.children:
                            if s.type == "fallthrough_statement":
                                next_has_ft = True
                            else:
                                next_stmts.append(s)
                    elif c.type not in ("case", "default", ":", ",", "expression_list"):
                        next_stmts.append(c)
                for t in case_tails:
                    ft_entry = self._new_node("fallthrough")
                    self._nodes[t].succs.append(ft_entry.id)
                    ft_tails = self._build_block(next_stmts, ft_entry, exit_n)
                    if next_has_ft and i + 2 < len(cases):
                        # Chain fallthrough (rare but possible)
                        tails.extend(ft_tails)
                    else:
                        tails.extend(ft_tails)
            else:
                tails.extend(case_tails)

        self._break_targets.pop()
        if label:
            del self._label_break_targets[label]

        if not has_default:
            self._nodes[switch_node.id].succs.append(switch_exit.id)

        # Connect all case tails to switch_exit
        for t in tails:
            self._nodes[t].succs.append(switch_exit.id)

        return [switch_exit.id]
