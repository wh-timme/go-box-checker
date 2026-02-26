# Box-Depth 静态检查器：修复思路与流程

## 背景

Box-Depth 静态检查器用于验证 Go 手写递归下降 parser 中 `db.New()`（depth+1）和 `db.Wrap()`（depth-1）的配对关系。核心方法是抽象解释 + 不动点迭代：为每个 `f_xxx` 函数构建 CFG，用 worklist 算法计算所有路径的 depth 变化量集合（DeltaSet），最终验证入口函数 `f_top` 的 delta == {0}。

初版实现通过了 11 个基础测试用例。随后用户将测试数据升级为更贴近真实 parser 的复杂场景，引入了 `continue`、`fallthrough`、for 循环条件调用、裸 `for {}` 等语法结构，导致 6 个测试失败。

## 失败用例诊断

通过 dump CFG 节点和 DeltaSet 结果，逐个定位根因：

| 用例 | 期望 | 实际 | 根因 |
|------|------|------|------|
| 05_recursive | PASS {0} | FAIL {0,1} | SCC bootstrap 用 {0} 引入虚假路径 |
| 06_loop_balanced | PASS {0} | FAIL {-2,0} | 缺少 continue 支持；for 条件调用未识别 |
| 07_loop_unbalanced | FAIL | PASS {0} | `for f_cond() {}` 条件中的 f_cond 调用未被分析 |
| 08_panic_discard | PASS {0} | FAIL {0,1} | fallthrough 未支持，case 2 被当作空 body |
| 09_switch_balanced | PASS {0} | FAIL {0,1} | 同上，fallthrough 缺失 |
| 11_break_in_loop | PASS {0} | FAIL {-1,0} | 裸 `for {}` 不应有 0 次迭代路径 |

## 修复方案

### 1. continue 语句支持

与 break 对称。CFGBuilder 新增 `_continue_targets` 栈，进入 for 循环时压入 `loop_head` 节点 ID，遇到 `continue_statement` 时将当前节点连接到栈顶的 `loop_head`，返回空 tails（无 fall-through）。

```
continue → 跳转到 loop_head（与 break → loop_exit 对称）
```

### 2. fallthrough 支持

Go 的 switch 默认不穿透，`fallthrough` 显式声明穿透到下一个 case 的 body。

修复方式：将 switch 的所有 case 按源码顺序收集到列表中。处理每个 case 时检测是否包含 `fallthrough_statement`。若有，将当前 case 的 tails 通过一个 `fallthrough` 中间节点连接到下一个 case 的 body 语句，而非直接汇入 switch 的出口。

```
case 2: fallthrough  →  不汇入 switch_exit，而是连接到 case 3 的 body
```

### 3. for 循环条件中的函数调用

`for f_cond() {}` 这种写法中，`f_cond()` 出现在 for 语句的条件位置，每次循环迭代都会执行。tree-sitter 将其解析为 `for_statement` 的直接子节点（`call_expression`），而非 body 内部。

修复方式：在 `_build_for` 中遍历 for_statement 的子节点，识别 `for_clause`（三段式 for）、`call_expression`/`identifier` 等条件节点、以及直接的 `block`（裸 for）。对条件中的 `f_xxx()` 调用，在 `loop_head` 之后插入对应的 call 节点。

```
loop_head → call:f_cond → [loop_exit | for_body]
                              ↑ 每次迭代都经过 f_cond
```

### 4. 裸 for 循环无 0 次迭代路径

`for {}` 是 Go 的无限循环，没有条件判断，唯一出口是 break 或 return。原实现无条件添加 `loop_head → loop_exit` 边，导致分析器认为循环可以不执行。

修复方式：只有当检测到条件存在时（`for_clause` 或条件表达式），才添加 0 次迭代的 `loop_head → loop_exit` 边。裸 `for {}` 不添加此边。

```
修复前: loop_head → loop_exit (所有 for 都有)
修复后: loop_head → loop_exit (仅有条件的 for 才有)
```

### 5. SCC 递归 bootstrap 策略

初版为解决递归函数分析的 BOTTOM 死锁问题，将 SCC 内函数的初始 summary 设为 `{0}`。但这引入了虚假路径：对于 `f_expr` 递归调用自身的场景，`{0}` 意味着"递归调用不改变 depth"，但实际上每次递归终止时必须走 base case（如 default 分支的 Wrap），delta 应为 -1。

修复方式：改回 BOTTOM 初始化。BOTTOM 在 compose 时会剪枝整条路径，第一轮迭代只有 base case 路径存活，产生正确的初始 delta。后续轮次用已收敛的 summary 展开递归路径，自然达到不动点。

```
Round 1: f_expr 递归调用 → compose(cur, BOTTOM) = BOTTOM → 路径剪枝
         default 分支 → Wrap → delta = {-1}
         f_expr summary = {-1}

Round 2: f_expr 递归调用 → compose(+1, {-1}) = {0}
         default 分支 → {-1}
         switch 后 Wrap → {0-1, -1-1} = {-1, -2}...
         实际: case1 = +1 + (-1) = 0, Wrap → -1; default = 0, Wrap → -1
         f_expr summary = {-1} (收敛)
```

## 验证

修复后 11 个测试全部通过，覆盖了简单配对、跨函数调用、递归、循环（含 break/continue）、switch（含 fallthrough/panic）、提前 return 等场景。
