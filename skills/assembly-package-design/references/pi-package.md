# Pi package 接入规范

本规范依据当前已核对的 Pi 0.87.1 package/extension 接口。新包应记录实际验证的 Pi 和运行时版本；升级宿主后重新检查接口行为。

## 包内容与命名

package 用于分发原生扩展、运行 Skill、领域后端及必要资源。显式声明 `pi.extensions` 和 `pi.skills`。`pi-package` keyword 用于包发现。Pi 提供的包与 TypeBox 使用 peer dependencies，不捆绑第二套宿主。

下面是结构示意；发布前需替换名称并完成实际实现：

```json
{
  "name": "@owner/pcb-assembly-tools",
  "version": "0.1.0",
  "type": "module",
  "keywords": ["pi-package"],
  "pi": {
    "extensions": ["./extensions/index.ts"],
    "skills": ["./skills"]
  },
  "peerDependencies": {
    "@earendil-works/pi-coding-agent": "*",
    "typebox": "*"
  }
}
```

Python、Rust、原生 CAD 库等由领域选型决定，不把当前 Python/POSIX 条件当作通用要求。声明支持平台、依赖版本、许可和安装方法。禁止依赖作者机器上的路径、现成虚拟环境或凭据。

## 多包共存

每个独立包需要稳定的 `package_id` 和工具前缀。例如：

| 范围 | 示例 |
|---|---|
| 包 | `@owner/pcb-assembly-tools` |
| 工具 | `pcb_assembly_search`、`pcb_assembly_build` |
| 命令 | `/pcb-assembly-setup` |
| 运行 Skill | `pcb-assembly-building` |
| 项目配置 | `.pi/assemblies/pcb-assembly-tools.json` |
| 数据/缓存/输出 | `.assembly/pcb-assembly-tools/` 下各自目录 |
| 提示区块 | `pcb_assembly_workflow` |

不要让所有新包注册同名的 `assembly_build`，或共同覆盖 `.pi/assembly.json`。当前 LEGO 包的这些名字是历史接口，需要保留或明确迁移。

若未来采用统一路由器，应由一个明确的宿主扩展注册共享入口，各领域通过稳定协议登记。路由器必须携带 domain/package 身份和权限边界。统一路由器是可选设计，当前并未实现。

## 注册与生命周期

- factory 仅注册工具、命令和事件；不启动长驻进程、监听端口、定时器或下载任务。
- 工具声明真实名称、用途、TypeBox schema、`execute()` 及 `content/details`。
- 失败通过抛出错误进入 Pi 原生错误结果。领域验证失败也需在返回契约中清楚表达，不能只输出“任务完成”。
- 有共享写入的工具使用顺序执行和 `withFileMutationQueue`；跨进程仍需后端锁或等效事务机制。
- 后台资源有明确所有者。处理取消和 `session_shutdown`，终止该调用拥有的工作并保留准确状态。
- 修改提示优先使用独立的 `systemPromptOptions.sections`，保留其他包的提示。不要全局改写用户意图或扩大任务。
- 返回结果控制上下文大小。完整结构、日志和工程文件放入可定位的产物，必要时按预算读取。

## Skill、工具、后端的职责

Skill 告诉 Agent 什么时候检索、如何比较、如何使用和解释结果。工具负责输入输出与执行入口。领域后端执行可计算约束和算法。关键正确性不能只依赖 Agent 是否读到了 Skill。

本设计 Skill 用于创建 package。新 package 应有自己的领域运行 Skill，并按任务按需加载。无需把本设计宪章全文放进每次工程构建上下文。

## 安装、setup 与项目状态

```text
pi install npm:<已发布名称>@<固定版本> --local --approve
```

命令仅在对应 registry 已发布并可访问时成立。GitHub 推送、npm 发布和项目安装分别记录。未发布 npm 时，可使用获授权的 Git 源安装。项目级安装写入项目设置；全局安装影响用户级设置。

显式 setup 检查或创建所需运行环境，记录下载/网络要求。默认不在 npm postinstall 中启动外部应用或修改工程数据。更新包时保留项目目录，按明确规则迁移 schema；旧版固定依赖仍可追溯。

解析代码和资源路径时以安装包为基准；数据、缓存和输出以消费项目为基准。验证路径与符号链接边界。外部工程库使用显式配置，不能被当作本包私有可删除目录。

## 能力发现与验证

`status/capabilities` 应能报告当前支持的格式、操作、验证器、运行环境和缺项，而不是只报告进程存活。读写权限和外部能力按任务环境判定。

发布包至少验证：tarball 内容、在无作者环境依赖的新项目中安装、工具与 Skill 发现、原生错误返回、取消、缓存、项目隔离，以及与另一个同类包共存。离线测试 provider 可以证明接线；真实模型能否正确设计，需要另行评估。

包内容 allowlist 应排除凭据、个人路径、捕获的私人文档、第三方受限库、缓存和生成工作数据。库的文件格式描述可以分发，不代表有权分发全部原始库文件。
