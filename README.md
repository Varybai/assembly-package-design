# Assembly Package Design

独立的标准 Agent Skill 仓库。提供 **Assembly Design Baseline 0.1.0**，用于设计机械、电子、控制、仿真及混合工程系统的 Assembly package。

本仓库只包含设计知识、规范、模板和验证脚本。安装的 Skill 仅含 Markdown 文件。LEGO 构建工具、Python 后端、Pi 扩展、模型数据和渲染器均不在本仓库中。

## 安装

使用标准 [skills CLI](https://github.com/vercel-labs/skills)：

```bash
npx skills add Varybai/assembly-package-design
```

指定安装到当前项目的 Pi：

```bash
npx skills add Varybai/assembly-package-design --agent pi --skill assembly-package-design
```

非交互安装，使用独立文件副本：

```bash
npx skills add Varybai/assembly-package-design --agent pi --skill assembly-package-design --copy --yes
```

默认安装范围为当前项目。经 skills CLI 1.7.1 验证，Pi 的安装目录是 `.agents/skills/assembly-package-design/`，Pi 会扫描该标准目录。需要用户级安装时显式添加 `--global`；其他受支持 Agent 可使用各自的 `--agent` 参数。

仓库当前为私有仓库。安装者需要 GitHub 访问权限，并已配置可用的 Git 凭据，例如通过 `gh auth login`。安装不需要 npm 发布或 npm 账号权限；`npx` 获取的是公共的 `skills` CLI，Skill 内容由 GitHub 获取。

仅查看可安装内容：

```bash
npx skills add Varybai/assembly-package-design --list
```

## 在 Pi 中使用

已有会话执行 `/reload`，然后输入：

```text
/skill:assembly-package-design 为 KiCad 设计一个 Assembly package。沿用通用基线，明确原生文件、功能模块、网络接口、复用规则、验证门槛和 Pi 安装方案。
```

读取和使用本 Skill 不需要 `/assembly-setup`、LDraw、LeoCAD、OpenViking 或其他工程后端。实际实现某个领域的 package 时，再按该领域需要选择依赖、知识库和求解器。

如果旧版 `assembly-tools` package 已经提供同名 Skill，切换时可在 Pi 的包资源设置中关闭旧包的 `assembly-package-design`，保留其 LEGO 工具。这样可避免同名 Skill 的来源冲突；本安装不会自动修改旧包。

## 内容

| 内容 | 文件 |
|---|---|
| Skill 入口与实施方法 | [SKILL.md](skills/assembly-package-design/SKILL.md) |
| 12 条设计宪章、思想与取舍原则 | [charter.md](skills/assembly-package-design/references/charter.md) |
| 对象、接口、关系和多文件契约 | [object-contract.md](skills/assembly-package-design/references/object-contract.md) |
| 检索、执行、证据、缓存和交付 | [execution-evidence.md](skills/assembly-package-design/references/execution-evidence.md) |
| 领域适配与跨领域组合 | [domain-adapters.md](skills/assembly-package-design/references/domain-adapters.md) |
| Pi package 接入和多包共存 | [pi-package.md](skills/assembly-package-design/references/pi-package.md) |
| 20 类可具体化的验收用例 | [conformance.md](skills/assembly-package-design/references/conformance.md) |
| 外部 LEGO 参照实现的范围 | [implementation-map.md](skills/assembly-package-design/references/implementation-map.md) |
| 新 package 设计模板 | [PACKAGE-DESIGN.template.md](skills/assembly-package-design/assets/PACKAGE-DESIGN.template.md) |
| 设计决策记录模板 | [DECISION.template.md](skills/assembly-package-design/assets/DECISION.template.md) |
| CAD、PCB、热仿真与混合系统示例 | [DOMAIN-EXAMPLES.md](skills/assembly-package-design/assets/DOMAIN-EXAMPLES.md) |

设计资料描述预期契约和验收方法，不代表相应工程算法已经实现或通过实体验证。

## 仓库结构

```text
skills/assembly-package-design/
  SKILL.md
  references/
  assets/
scripts/validate_skill.py       # 维护检查；不随 Skill 安装
.github/workflows/validate.yml  # CI；不随 Skill 安装
```

## 验证与维护

```bash
python3 scripts/validate_skill.py
npx skills add . --list
```

CI 还会在临时目录中使用固定版本的 skills CLI 执行真实安装，然后检查安装后的 Skill、参考资料和模板。安装不要求 Python；上面的 Python 命令只用于仓库维护检查。

来源：从 [Varybai/assembly-tools 的设计基线提交](https://github.com/Varybai/assembly-tools/tree/ed6e4bba1bdc807ae3322b96e728e5f7fff62a36/skills/assembly-package-design) 提取。该仓库中的 LEGO 运行工具作为外部参照保留；这里独立维护通用设计 Skill。
