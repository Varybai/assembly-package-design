# 外部 LEGO 参照实现与通用基线的边界

外部参照：[Varybai/assembly-tools 的固定提交](https://github.com/Varybai/assembly-tools/tree/64534fd3a56f5e1706faf47adfa670cbd45f0399)。本仓库不包含或安装其代码。下面是该提交的实现范围说明，用于比较设计差异；使用本 Skill 不要求先安装该参照实现。

| 通用方向 | 外部参照实现 | 新领域需补充的内容 |
|---|---|---|
| 功能先行 | 本地功能词/同义概念匹配，另由 Agent 调用 OV | 领域词表、精确约束和接口检查；不是通用最优选件算法 |
| 身份与实例 | `uid@version`、固定子引用、刚体局部位姿 | 跨包命名空间，非几何绑定与其他参数类型 |
| 原子/组合统一目录 | `kind=atomic/assembly` 的 JSON Registry | 原子边界、领域 schema 与多文件权威源 |
| 程序复用 | 有序 `place`；CLI 有 design replay | 领域动作与真实前后置检查；Pi build 不调用事务式 replay |
| 渐进抽象 | 显式历史选择与提取、局部布局重复建议 | 边界由 Agent/人判断；无自动功能边界学习 |
| 接口映射 | 组合端口映射到子端口；示例常为 layout_anchor | 类型兼容求解、物理连接和跨领域适配 |
| 编译缓存 | 递归 LDraw 编译，定义/参数/颜色等决定键 | 不同 UID 的几何等价不自动归并；其他领域需新编译器 |
| 内外验证 | 保守 AABB，子内部证据复用，实例邻域检查 | 网络、工况、时序、动力学和全局耦合检查 |
| 原生文件 | DAT/LDR/MPD、JSON、CSV、PNG、PDF | CAD/PCB/CAE 原生格式和往返保真 |
| 连续交付 | 数据包先生成；LeoCAD 渲染/PDF 可降级 | 每个领域重新定义必要阶段和交付合格门槛 |
| Pi package | 六工具、Skill、显式 setup、进程取消、项目状态 | 多个领域共存所需前缀、配置与数据隔离 |
| OV 解耦 | 普通知识投影、可选 API；当前 Pi 通过已有 OV 工具 | 可替换检索后端、按领域定位精确数据 |

特别注意：当前 `complete` 主要表示文件流水线执行完成。即使验证报告包含需要复核的候选，文件仍可生成。新的制造或部署类包必须另设与用途对应的验证门槛，不能照搬这个状态含义。

上述外部代码是一个 LEGO 参照实现。它不是已经完成的跨领域 Assembly 内核。本基线要求的多领域接口、图关系、通用 Artifact/Evidence 模型和统一路由器仍是设计工作，需要对应 package 实现和测试。

来源包括本次用户提出的功能语义、层级访问和多工程系统要求，以及原始 [Assembly 设计与复用](https://lcnx4jkvmory.feishu.cn/wiki/QlLCwhO8wiDJRtkNGJQcJUIVnWf) 文档的边界渐进形成、程序复用、减少规划成本和 Lazy Abstraction 原则。跨领域规范是这些原则的本次工程化推导，并非该文档声称已实现的功能。
