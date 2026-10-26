---
name: unity-apk-recovery
description: 分析 Unity APK/XAPK/APKS，提取资源、场景和脚本结构，对照原版恢复可编辑工程并通过 Unity MCP 验证。用于 APK 逆向恢复、场景/教程还原和相关批处理，不承诺一键恢复完整源码。
---

# Unity APK 逆向恢复

目标是可验证的原版画面和行为。资源导出、代码结构恢复、方法体恢复、重建实现、编辑器运行、目标平台运行是不同成果，分别记录。

## 入口

- 继续本机 Walk Master：先读 [references/walkmaster-handoff.md](references/walkmaster-handoff.md)，核对实时状态，不重复从头导出。
- 新 APK 或批处理：读 [references/recovery-workflow.md](references/recovery-workflow.md)。各游戏独立输出、记录来源和失败阶段。
- Unity MCP：读 [references/mcp-27841.md](references/mcp-27841.md)，使用附带 [scripts/unity_mcp.py](scripts/unity_mcp.py) 调用 HTTP MCP，或使用已连接的原生工具。
- 自动编排：先运行 `scripts/recovery_manifest.py INPUT --output OUTPUT/recovery-manifest.json`，再按 manifest 决定解包、导出和验证阶段；不要把完整日志塞进上下文。

## 统一工作目录

每个输入包使用独立目录，禁止覆盖人工修复：

```text
OUTPUT/
├── input/              # 原包副本、哈希和分包清单
├── raw-export/         # AssetRipper/UnityPy 原始结果
├── recovered-project/  # 可编辑工程和人工修复
├── analysis/           # REA/JADX/IL2CPP 摘要
├── evidence/           # 原版/修复版截图和状态快照
├── logs/
└── recovery-report.json
```

每个对象和结论标记 `restored`、`missing-reference`、`runtime-generated`、`reconstructed` 或 `unknown`。恢复报告必须区分原始证据、推断和手工重建。

## 低上下文验证

先验证结构化状态，再截图：场景、对象数、Missing Reference、脚本编译、关键状态和输入结果优先用 JSON 快照比较。只对差异切片抓图。先验证教学关、普通关、复杂关和特殊机制关，再批量做其余关卡健康检查。

REA 用于定位加载入口、资源 key、状态枚举和 IL2CPP/Android 逻辑；AssetRipper/UnityPy 用于资源；Unity MCP 用于导入、编译、运行和证据采集。三者结果必须写入同一份报告，不能把 REA 的分析结果当成已恢复源码。

## 关键约束

1. 识别完整分包、Unity 版本、Mono/IL2CPP 和 ABI。base APK 可能缺运行库或资源。
2. 原包、原始导出与修复工程分开；重新导出不得覆盖人工修复。
3. DummyDll、空方法、默认返回值、NoteDecompilerIssue 不是完整源码。逐项区分恢复代码和手工重建代码。
4. 优先复用原场景、预制体、关卡块、配置、UI 和动画；先研究运行时生成规则，再补缺失逻辑。用户要原版时，不以自制菜单、平地或自动跑动代替。
5. 对照同版本、关卡、位置、方向和画面比例。先查贴图/材质/图层/镜头，再改位置；不要为掩盖丢失资源随意染色或缩放。
6. Unity 打开时，序列化资源优先经 Unity API/MCP 修改，保留 GUID/fileID 和备份；源文件编辑后明确导入、编译，再测试新程序集。
7. 技能不扩大用户授权，不自行发送外部消息、发布、删除数据或授予访问权限，不关闭 MCP 安全检查。

## 验收与交接

- 从具体垂直切片开始，如教学起点、拖动抬腿、松手落脚、任务切换；通过输入和状态证明，不能只凭工具返回 dispatched。
- 检查编译、Console、引用、Play Mode、连续操作和失败重试；按需求另验目标平台构建与真实浏览器/设备。
- 画面未对齐、方法为空、教程未通关或 WebGL 未实测时，保留限制，不报完成。
- 项目进度记录实际路径、版本、哈希、修改文件、最新截图、验证结果、失败原因及下一步，避免在新对话重读全部日志。
- 批量工具可自动诊断、分包合并、资源导出与生成问题清单；每款游戏逻辑还原通常需要专项分析，不能宣称批量一键完整恢复。
