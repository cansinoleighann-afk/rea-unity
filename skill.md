# rea-unity 逆向技能

这是本项目的逆向技能入口和维护位置。按输入和目标选流程，只读当前阶段需要的详文。原始资料来自 F:\AI技能库\逆向技能。

## 选择流程

| 输入或目标 | 入口 |
| --- | --- |
| APK、XAPK、APKS 或多个 Android 分包 | [Unity APK 恢复](.agents/skills/unity-apk-recovery/SKILL.md)。先用 [recovery_manifest.py](.agents/skills/unity-apk-recovery/scripts/recovery_manifest.py) 检查输入。分包可能分别携带 Unity 资源和原生库。 |
| Windows 或其他桌面平台的 Unity 构建产物 | [Unity 桌面游戏恢复](.agents/skills/unity-pc-game-recovery/SKILL.md)。盘点完整游戏目录，确认 Unity 版本、Mono 或 IL2CPP、平台和架构。 |
| 已有可编辑工程，且用户明确要处理逆向项目 | 使用下方“逆向工程处理”。原技能位于 `F:\AI技能库\逆向技能\处理项目\unity-reverse-project-workflow\SKILL.md`。 |
| 查加载入口、资源键、方法地址或静态调用关系 | [REA 分析](.agents/skills/reverse-engineer-anything/SKILL.md)。选范围最小的只读查询，保留路径、哈希、版本和覆盖范围。 |

## APK 和电脑端恢复

1. 检查输入是否齐全。Windows Mono 通常可从 `*_Data/Managed/Assembly-CSharp.dll` 开始。IL2CPP 使用同一构建的 `global-metadata.dat` 和 Android 的 `libil2cpp.so` 或 Windows 的 `GameAssembly.dll`。
2. 原包、原始导出、分析证据和修复工程分开。AssetRipper 导出场景与资源，UnityPy 做单项检查。ILSpy 反编译保留方法体的托管程序集。REA、Cpp2IL、Il2CppDumper、Ghidra 用于查 IL2CPP 结构、地址和可分析的方法逻辑。JADX 用于 Android 的 manifest 与 Java/Kotlin 层。
3. 逐项记录从包中提取的证据、推断、人工重建和缺口。按实际覆盖范围记录 DummyDll、空方法、伪代码和缺失引用。
4. 导入验证副本，从一个代表性场景开始。用 Unity API 或 MCP 修复序列化资源并保留 GUID 和 fileID。检查编译、Console、场景引用、Play Mode、真实输入及状态结果。按需求补测构建或设备。
5. 对齐构建版本、场景、分辨率和状态。先用结构化结果定位差异，再补截图。接续历史项目时先核对现有路径、版本和端口。 [APK 流程](.agents/skills/unity-apk-recovery/references/recovery-workflow.md) · [桌面流程](.agents/skills/unity-pc-game-recovery/references/desktop-workflow.md) · [Unity MCP 验证](.agents/skills/unity-apk-recovery/references/mcp-27841.md)

Windows 的 Ghidra 安装目录与临时项目目录使用纯英文或数字路径，避开中文路径和以点开头的目录。Ghidra 12.2 配 JDK 25。REA 6.10.1 支持连接 Ghidra 12.2。

## 逆向工程处理

开工前核对项目根目录、Unity 与 SDK 版本、目标平台、当前场景、输出和基线。完整流程按 T1–T12 推进，每项记录改动和验收证据。单项任务使用所需步骤及其前置依赖。原规范与任务清单位于 `F:\AI技能库\逆向技能\处理项目\unity-reverse-project-workflow\references`。

| 阶段 | 工作与验收 |
| --- | --- |
| T1–T2 | 接入 Unity MCP，按项目要求安装两项框架包。核对项目、端口、场景、已加载包版本和编译状态。 |
| T3–T5 | 盘点可达文本、汉化、替换字体并生成中文子集。保留格式占位符、富文本和动态参数，验证缺字、排版、回退字体后再清理旧引用。 |
| T6–T8 | 修复 UI 贴图导入类型，设置 WebGL 贴图覆盖，优化音频。验证图集、遮罩和交互。资源优化排除 `Assets/WX-WASM-SDK-V2/**` 与 `Assets/WebGLTemplates/**`。源音频大于 102,400 字节才考虑外部转码。 |
| T9–T11 | 配置 WebGL 和微信小游戏，做构建前总检，然后生成并验收首包。核对 SDK 和生成配置、本地加载模式、非空 `data-package` 或已配置的本地子包。清缓存启动，条件允许时断网复测。 |
| T12 | 分析 `webgl.data` 或解包后的 `data.unity3d`。记录大小、哈希、表示形式和资源分布。Brotli 与未压缩体积分别统计，按同一口径比较。WASM 和 JavaScript 单列为运行时诊断。 |

按实际 SDK 和构建日志确认包体门槛。CDN 回退按过渡构建记录。每轮优化保留前置设置和回滚依据，等待重导入后检查 Console，重新构建再复核收益。

## 维护约定

- 后续新增或调整本项目的逆向技能，先更新本文件的入口、适用条件和验收规则。长流程、模板和脚本放进仓库对应的技能目录，并更新这里的链接。
- 外部技能库作为资料来源。本项目的流程变更落在本仓库。工具版本、安装路径和验证结果以实测为准。
- 交接记录输入版本和哈希、输出位置、已恢复和手工重建的内容、验证结果及剩余缺口。
