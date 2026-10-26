# Walk Master 接续快照

截至 2026-10-25。先读本页，再只读核对实时工程、源文件和证据；用户可能自行切场景或 Play，不把快照当实时状态。

## 用户要求

原版原本的场景、布局、动作、UI、玩法，不能近似小游戏冒充。当前先做好新手教程，最近重点是背景和地面对齐，再验可玩。竖屏 **667×1334**，Canvas 同参考分辨率。最后简体中文单语言、中文字体、压缩包体、WebGL。不要先扩大到其他关或过早删除资源。

Unity 操作优先 **MCP 27841**；原版 MuMu 作画面/行为对照。MuMu 留 **E 盘** 已获用户接受，不再迁 D；主程序和虚拟机不放 C，但少量系统组件和缓存可能在 C。原安装条款曾经用户明确同意，不代表将来任何新条款或权限已获同意。

## 路径

| 内容 | 路径 |
|---|---|
| 工具工作区 | `F:/1.Unity资料/逆向` |
| 修复工程 | `F:/.Untiy/NiXiang` |
| Unity | `D:/Unity/IDE/2022.3.14f1c1/Editor/Unity.exe` |
| MCP | `http://127.0.0.1:27841/`，工程 `Packages/com.gamebooom.unity.mcp` v0.7.0 |
| base APK | 工作区 `原包/fi.twomenandadog.walkmaster.apk` |
| 完整 XAPK | `downloads/WalkMaster-full.xapk` |
| 合并输入 | `samples/WalkMaster-complete/assets/bin/Data` |
| 原始导出 | `exports/WalkMaster-complete/ExportedProject`，不要覆盖 |
| IL 候选输出 | `exports/WalkMaster-il-source`、`exports/WalkMaster-il-recovery`，不等于可用源码 |
| 回滚备份 | 工程 `RecoveryQuarantine` |
| 当前记录 | 工程 `RecoveryStatus.md`、`需求与验收.md`；工作区 `恢复进度.md` 可能较旧 |
| MuMu CLI | `E:/Program Files/Netease/MuMuPlayer/nx_main/mumu-cli.exe` |
| MuMu 数据 | `E:/Program Files/Netease/MuMuPlayer/vms/MuMuPlayerGlobal-15.0-0` |
| ADB | `D:/Android/android-sdk/platform-tools/adb.exe` |

原版 **Unity 6000.3.20f1 / IL2CPP metadata v39 / ARM64**，运行版 **1.6.8**、versionCode **1066004**；目标降到 Unity 2022.3.14f1c1，存在跨版本修复。

- base 130240781 bytes，SHA256 `06753d6f329b3d6a8ecc6d36e6ed3e5b91d91b821f0f61d4d660e66999a29a8b`
- XAPK 163583884 bytes，SHA256 `f8d8661a31c37d3401bf4f64cce0ed2173ec7b2002d86a3da1b3e7c2042e917b`
- 完整包有 base 和 config.arm64_v8a.apk；base 与原文件相同，libil2cpp.so 64459280 bytes。

## 已做过什么

- AssetRipper 2.0 导出 8 场景、575 预制体；GameplayScene 原有 4612 对象/14 根对象，不是只有散素材。
- Cpp2IL 恢复类型、字段和部分候选方法，但大量空方法/NoteDecompilerIssue；教程方法体没有完整恢复。不要重新声称“有 C# 就是原源码”。
- 已修 UGUI/TMP MissingScript 映射，原场景 MissingScripts 曾验 0；新修改仍需复查。
- Spine JSON 3.7.93 对应官方 3.7 runtime，提交 `9639bcc81722d7178fd9d1cdc1a3d55a4c91f989`；35 SkeletonDataAsset 曾解析成功。
- 原 Tag、物理层和 14 Sorting Layers 已恢复；中文 TMP 材质从 Dummy shader 改为真实 Mobile SDF。
- 797 个 Sprite 图片/原 GUID 引用已修。原始 UnityPy 1117 个 Sprite 中 320 个未匹配导出索引，不能把这个数直接当缺失数；原导出 Sprite 文件约 1029。
- 第一轮 UnityPy 旧 UV 映射生成碎片，第二轮采用 atlas rect/rotation + geometry mask 修正；裁切边缘/偏移仍需抽样。
- MuMu 已装完整分包并进入竖屏教程；索引 0、Android 15，最近 ADB `127.0.0.1:16384`，用 `mumu-cli info --vmindex all` 刷新。Google Play 电脑版也能试玩，非主要分析环境。
- **没有完成 Frida runtime dump**，不能声称已采集原版对象位置。树木目前按原配置重新随机放置，真实视差相机未恢复。

## 当前实现（明确属于重建）

目录 `Assets/Scripts/Assembly-CSharp/Recovery/`：
- RecoveryCatalog：50 普通关、39 其他关、34 角色、起点/终点/教学关。资源 `Assets/Resources/RecoveryCatalog.asset`。
- RecoveredGameFlow：当前修订号 4，tutorialMode 默认 true，直接进入原 LevelBlock_Tutorial_Walk，临时黄色菜单隐藏。教学拼接 3 块，长约 109.98。
- RecoveredTutorial：克隆原 TutorialPanel / TouchTutorialPortrait，复用手指、虚线和勾选框，中文提示；步骤和距离阈值为重建/简化，尚未完整通关。
- RecoveredStiltMotor：基于原 torso/poles/WheelJoint 的重建物理控制。已修站立扭矩、抬腿范围和输入后的重心，隐藏默认失败星星/Rocket/旧标志，处理重复 Spine 分段渲染。手脚 IK、姿态、气球和原版手感仍不一致。
- RecoveredGeometry 与 TMAAD/GroundBlockShape：原轮廓三角化、碰撞、GroundConfig 草皮材质；坡面、悬崖包边、水面、装饰仍不完整。
- BackgroundGenerator、BackgroundSpriteScaler、TMAAD/PrefabPlacer：修天空左轴心和 Clamp、树丛/底色共用轮廓；改为实际地面碰撞采样，避免起点高墙最大高度插值制造长斜坡。
- PoleDistort：拼片子网格与独立纹理材质。
- Assets/Shader/RecoveredVertexColor.shader：透明队列、ZWrite Off，修天空盖地面。另 12 个空壳 Shader 是近似重写，不是原 Shader 源码。
- Assets/Editor/RecoveryWebGLImportPolicy.cs：平台导入策略已写，最近目标仍 StandaloneWindows64 用于调试；WebGL 构建/浏览器尚未完成。

## 最新证据与接续重点

技能交接时已通过 27841 只读复核：工程 `F:/.Untiy/NiXiang/Assets`、Unity 2022.3.14f1c1、当前 `Assets/Scenes/GameplayScene.unity`、无未保存场景修改、未在 Play、修订号 4。原始结果在工作区 `tools/skill-handoff-live-state.json`。

用户提供的原版横屏悬崖截图已另存工程 `RecoveryEvidence/Reference/original-first-level-cliff.png`，不依赖聊天临时附件；这是原版对照图，不能与修复工程截图混淆。

工程 `RecoveryEvidence/tutorial-forest-profile-v5.png` 是最新截图：天空盖地面、横条和伪斜坡明显改善，树林底色连接更完整；**树木布局、视差、坡面/包边和角色动作未达到原版一比一**。

`tutorial-ground-compare.png`、`tutorial-forest-fill-v4.png`、`tutorial-render-v3.png` 是更旧中间结果，不要当最终。

工作区 `tools/tutorial-latest-errors.json` 最近一次 120 秒 Console 缓存无 error，仅限该时间窗。

`tools/TestTutorialInput.cs` 经 MCP 跨帧真实 InputSystem 验证；`tools/ReadTutorialTest.cs` 读 SessionState RecoveryTutorialInputTest。曾见任务进入 WalkToCheckpoint、净前进约 +1.14；当次 drag count 为 4，不是精确单步原版手感证明。完整教程通关未验。

接续顺序：
1. 核对实时 GameplayScene、版本、编译、修订号、截图。不要自动重新导出覆盖修复。
2. 与 MuMu **同一教程起点/比例** 对照背景、地面和角色；用户提供的横屏跷跷板悬崖是另一位置，不能用比例不同掩盖结构差异。
3. 优先修视差、树底/布局、镜头、草皮厚度、坡面和悬崖包边，再补教学动作/气球。
4. 验连续交替迈步、重试、检查点、障碍、通关，再做中文字体精简、WebGL 和批处理。

## 工具索引（工作区 tools）

- mcp_client.py / invoke_code.py：JSON-RPC 和 C# 片段；旧 invoke_code 可能内部失败仍退出 0。
- recover_sprite_images.py：本包专用，依赖 tools/pythonlibs 的 UnityPy 1.25.4；从 RecoveryQuarantine/Sprite-before-pixel-repair 建索引，因当前 Sprite render key 已变化。输出 exports/recovered-sprite-pixels/manifest.json，不要盲覆盖工程。
- 工程 Assets/Editor/RecoverySpriteRepair.cs：分帧保 GUID 修复；SessionState 索引，状态 RecoverySpriteRepairStatus.json。旧 completed 数不能证明新输入已经处理。
- TutorialInventory.cs / TutorialUiInventory.cs / GameplayRuntimeProbe.cs / TutorialPhysicsProbe.cs / BackgroundShapeProbe.cs / PlacerProbe.cs / GrassProbe.cs：定向盘点，避免读完整巨型场景 YAML。
- ConfigurePortrait.cs / ConfigureChineseWebGL.cs / RestoreRenderLayers.cs / ConfigureTutorial.cs：已执行过的配置脚本；重跑先查是否覆盖用户新设置。
- tools/font-source/NotoSansSC-Bold.otf（8543168 bytes）与 LICENSE：待生成精简静态中文字体。旧中文 SDF 覆盖原表 549 字，新文案未全验，曾缺“菜”和 underline；不要把源字体全量打包当压缩完成。

本文件是接续快照，不是恢复完成证明。
