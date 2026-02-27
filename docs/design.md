# Box-Checker 设计文档

## 1. 概述

`box-checker` 是一个静态分析工具，用于验证 Go 手写递归下降 parser 中的
**box-depth 配对平衡性**。这类 parser 通过 `DepthBox` 对象跟踪嵌套深度：

- `db.New()` — 打开新的深度层级（delta = +1）
- `db.Wrap()` — 关闭当前深度层级（delta = −1）

正确实现的 parser 要求：从入口函数 `f_top` 出发，所有可能的执行路径在函数返回时
净深度变化量必须恰好为 0。工具最终判定出口处的 DeltaSet 是否为 `{0}`。

---

## 2. 整体架构

```
Go 源文件
    │
    ▼
go_parser.py        tree-sitter 解析 → AST 根节点
    │               extract_functions() → {函数名: 函数节点}
    ▼
  cfg.py            CFGBuilder.build() → FuncCFG（逐函数）
    │               （AST 语句 → CFG 节点 + 边）
    ▼
analyzer.py         analyze_program()
    │                 ├─ Tarjan SCC 分解调用图
    │                 └─ 逐 SCC worklist 数据流 + 不动点迭代
    ▼
 model.py           DeltaSet（抽象域）
    │
    ▼
 verify()           检查出口 DeltaSet == {0}
```

### 模块职责

| 模块 | 职责 |
|------|------|
| `model.py` | 核心数据结构：`CFGNode`、`FuncCFG`、`DeltaSet`、`FuncSummary` |
| `go_parser.py` | 封装 tree-sitter-go；提取所有 `f_xxx` 函数的 AST 节点 |
| `cfg.py` | 从函数 AST 构建过程内 CFG |
| `analyzer.py` | 过程间不动点分析；`verify()` 作为入口 |
| `main.py` | CLI 入口（`python -m box_checker`） |

---

## 3. 抽象域：DeltaSet

分析过程追踪每条执行路径上所有**可能的**净深度变化量。每个 CFG 节点的抽象值为
`DeltaSet`：一个整数的有限集合，表示该点可达的深度变化量。

```
DeltaSet = BOTTOM               （不可达 — 所有节点的初始状态）
         | {d₁, d₂, …, dₙ}     （有限具体 delta 集合）
         | TOP                  （无界 — 由 widening 触发）
```

### 核心操作

| 操作 | 语义 |
|------|------|
| `union(a, b)` | 集合并集 — 在汇合点合并状态 |
| `add_scalar(n)` | 每个元素偏移 n — 建模 `db.New`(+1) / `db.Wrap`(−1) |
| `compose(a, b)` | 笛卡尔和 `{x+y \| x∈a, y∈b}` — 建模函数调用 |
| `widen(limit)` | 若 `\|set\| > limit` 则返回 TOP — 防止发散 |

`BOTTOM` 是 `union` 的单位元，也是 `compose` 的零元/吸收元（被调函数 summary 为
BOTTOM 时整条路径被剪枝）。

---

## 4. CFG 构建（`cfg.py`）

每个 Go 函数 `f_xxx` 被转换为一个 `FuncCFG`：

- **entry 节点** — 零 delta 起始节点
- **exit 节点** — 所有终止路径的汇聚点
- 每个关键 AST 结构对应一个 **CFGNode**

### 语句映射

| Go 语法结构 | CFG 结构 |
|---|---|
| `db.New()` | 单节点，`delta = +1` |
| `db.Wrap()` | 单节点，`delta = −1` |
| `f_xxx()` 调用 | 单节点，`call_target = "f_xxx"` |
| `panic(...)` | 死端节点（`is_panic = True`）；路径被丢弃 |
| `return` | 连接到 exit；返回空 tails |
| `if / else` | 条件节点 → 两分支；在汇合点合并 |
| `for {}` | `for_head → for_body → (回边到 for_head)` + `for_exit` |
| `for cond {}` | `for_head → [for_exit \| for_body]`；条件中的调用内联在 head 之后 |
| `switch` | `switch_node` → 每个 case 一个分支；`fallthrough` 链接到下一个 case 的 body |
| `break` | 将当前节点连接到最内层 `for_exit`；返回空 tails |
| `continue` | 将当前节点连接到最内层 `for_head`；返回空 tails |
| `break LABEL` | 连接到标签 `LABEL` 所在循环的 `for_exit` |
| `continue LABEL` | 连接到标签 `LABEL` 所在循环的 `for_head` |
| `LABEL: for {}` | 与 `for {}` 相同，但在构建 body 前注册标签映射 |

### break / continue 目标栈

`CFGBuilder` 维护两组并行的数据结构：

**栈**（用于无标签的 break/continue）：
- `_break_targets: list[int]` — 循环退出节点 ID 栈，进入 `for` 时压入
- `_continue_targets: list[int]` — 循环头节点 ID 栈，进入 `for` 时压入

无标签的 `break` / `continue` 使用栈顶 `[-1]`（最内层循环）。

**字典**（用于带标签的 break/continue）：
- `_label_break_targets: dict[str, int]`
- `_label_continue_targets: dict[str, int]`

在进入带标签的 `for` 循环时注册，退出时删除。这正确建模了 Go 语义：
`continue LABEL` 跳转到**外层标签循环**的头部，跳过内层循环体和外层循环体的
剩余部分。

### switch 语义

- 每个 case 的 body 从共享的 `switch_node` 开始构建。
- `fallthrough` 通过中间 `fallthrough` 节点将当前 case 的 tails 链接到
  **下一个** case 的 body。
- switch 内的 `break` 使用 `_break_targets[-1]`（外层循环的 exit）。在 Go 中
  若仅需退出 switch，需使用带标签的 `break LABEL`，工具通过标签字典正确处理。
- 若 switch 无 `default` 分支，则 `switch_node` 自身加入 tails（"无 case 匹配"
  的穿透路径）。

### 裸 `for {}` vs 有条件循环

`for {}` 是 Go 的无限循环，无条件判断，唯一出口为 `break` 或 `return`。
`for_head → for_exit` 边**仅在**检测到循环条件时添加（`for_clause` 或条件表达式），
裸 `for {}` 不添加此边，迫使分析器通过显式 `break` 或 `return` 才能到达 `for_exit`。

---

## 5. 过程内分析（`analyzer.py`）

标准的 **worklist 数据流分析**：

```
state: dict[node_id → DeltaSet]
state[entry] = {0}
worklist = deque([entry])

while worklist:
    nid = worklist.popleft()
    out = propagate(state[nid], nodes[nid])
    for succ in nodes[nid].succs:
        merged = state[succ].union(out).widen(limit)
        if merged != state[succ]:
            state[succ] = merged
            worklist.append(succ)

return state[exit]
```

各节点类型的传播规则：

| 节点类型 | `out = ?` |
|----------|-----------|
| 普通节点（无 delta、无调用） | `cur` |
| `delta != 0` | `cur.add_scalar(delta)` |
| `call_target` 已知 | `cur.compose(summaries[callee].delta_set)` |
| `call_target` 未知 | `cur`（视为 delta = 0） |
| `is_panic` | 跳过（路径丢弃） |

安全上限（`max_iterations = len(nodes) × 50 + 200`）防止病态图导致无限循环。

---

## 6. 过程间分析

### 调用图与 SCC

从所有 CFG 的 `call_target` 字段构建函数调用图，使用 **Tarjan 算法**分解为
**强连通分量**（SCC）。Tarjan 以逆拓扑序返回 SCC，确保被调用者先于调用者完成分析。

### 逐 SCC 不动点迭代

对每个 SCC（可能包含互递归函数），工具运行多轮迭代直到 summary 不再变化：

```
for scc in sccs:                # 逆拓扑序
    for _ in range(max_rounds):
        changed = False
        for fname in scc:
            new_ds = analyze_function(cfgs[fname], summaries)
            if new_ds != summaries[fname].delta_set:
                summaries[fname].delta_set = new_ds
                changed = True
        if not changed:
            break
```

### 递归函数的 bootstrap 策略

所有 summary 初始化为 `BOTTOM`。第一轮迭代中，对同一 SCC 内函数的调用使用
`compose(cur, BOTTOM) = BOTTOM`，**剪枝**整条递归路径。只有 base case 路径
（不递归的分支）存活并产生初始 delta。后续轮次使用已收敛的 summary 展开递归路径，
自然达到不动点。

这避免了将 summary 初始化为 `{0}` 所引入的虚假路径（`{0}` 会错误地建模为
"递归调用不改变 depth"）。

---

## 7. 验证

```python
def verify(cfgs, entry="f_top") -> (bool, str):
    summaries = analyze_program(cfgs, entry)
    ds = summaries[entry].delta_set
    if ds == {0}:    return True,  "OK"
    if ds.is_top:    return False, "TOP (无界)"
    if ds.is_bottom: return False, "不可达"
    return False, f"FAIL (delta = {sorted(ds.values)})"
```

仅当出口 DeltaSet 恰好为 `{0}` 时返回 `True`。

---

## 8. 测试覆盖

### 8.1 手工测试（`tests/test_e2e.py`）

`tests/testdata/` 中的手工测试用例覆盖：

| # | 场景 | 期望结果 |
|---|------|---------|
| 01 | 简单平衡 `New/Wrap` | PASS |
| 02 | 简单不平衡 | FAIL |
| 03 | 跨函数调用（平衡） | PASS |
| 04 | 分支 delta 不匹配 | FAIL |
| 05 | 递归函数 | PASS |
| 06 | 循环体平衡 | PASS |
| 07 | 循环体不平衡 | FAIL |
| 08 | `panic` 丢弃路径 | PASS |
| 09 | `switch` + `fallthrough` | PASS |
| 10 | 提前 `return` 导致不平衡 | FAIL |
| 11 | 循环内 `break` 不带 `Wrap` | PASS |
| 12 | 嵌套循环 + `break/continue LABEL`（平衡） | PASS |
| 13 | 嵌套循环，内层 `continue` 跳过 `Wrap`（不平衡） | FAIL |
| 14 | 嵌套循环，`continue LABEL` 跳过外层 `Wrap`（不平衡） | FAIL |
| 15 | 循环 + switch + `fallthrough` + `break LABEL`（平衡） | PASS |

### 8.2 压力测试（`tests/test_stress.py`）

使用 `tests/gen_stress.py` 自动生成大规模测试，接近真实 parser 的规模和复杂度。

**运行方式**：

```bash
python tests/gen_stress.py                    # 生成 stress_*.go + test_stress.py
python -m pytest tests/test_stress.py -v      # 运行压力测试
```

**生成器架构**：

```
gen_stress.py
  ├── GoEmitter          # Go 代码字符串构建器（缩进管理、emit 语句）
  └── StressGenerator    # 编排所有分类的生成
        ├── _gen_simple()         # 分类01: 线性序列
        ├── _gen_if_else()        # 分类02: if/else 分支
        ├── _gen_bare_for()       # 分类03: 裸 for {}
        ├── _gen_cond_for()       # 分类04: 有条件 for
        ├── _gen_for_call()       # 分类05: for f_cond() {}
        ├── _gen_switch()         # 分类06: switch/case
        ├── _gen_fallthrough()    # 分类07: fallthrough
        ├── _gen_panic()          # 分类08: panic 剪枝
        ├── _gen_break_continue() # 分类09: break/continue
        ├── _gen_labeled()        # 分类10: 标签 break/continue
        ├── _gen_return()         # 分类11: 提前 return
        ├── _gen_nested()         # 分类12: 嵌套循环
        ├── _gen_cross_func()     # 分类13: 跨函数调用链
        ├── _gen_recursive()      # 分类14: 递归/互递归
        └── _gen_mixed()          # 分类15: 混合复杂场景
```

**产物**：

| 文件 | 说明 |
|------|------|
| `tests/testdata/stress_01_simple.go` ~ `stress_15_mixed.go` | 15 个按分类拆分的 Go 源文件 |
| `tests/test_stress.py` | pytest 测试文件，内嵌 EXPECTED 字典 |

**规模**（默认参数 `scale=1.8, body_scale=2.5, seed=42`）：

| 指标 | 数值 |
|------|------|
| Go 文件数 | 15 |
| 总行数 | ~20000 |
| 测试入口数 | ~750（平衡 ~380 / 不平衡 ~370） |
| 执行时间 | < 1s |

**可调参数**：

- `seed` — 随机种子，固定为 42 保证可复现
- `scale` — 函数数量缩放因子
- `body_scale` — 函数体复杂度缩放因子（影响 `db.New/Wrap` 序列长度）

**测试优化**：每个 Go 文件只调用一次 `analyze_program`（处理文件内所有函数），
然后逐个检查各函数的 summary，避免 N 次全量分析。
