# Unity 恢复工具安装指南

以 Windows x64 为例。表中的版本是本项目安装或验证过的版本。用发布包做分析时，把工具、输入、原始导出和修复工程放在不同目录。

## 工具清单

| 工具                                         | 用途                                                             | 版本和安装来源                                                                                                                                                                                                                                               |
| -------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Git 与 PowerShell                            | 拉取仓库、运行安装与配置命令                                     | [Git for Windows](https://gitforwindows.org/) · [PowerShell](https://learn.microsoft.com/powershell/scripting/install/installing-powershell-on-windows)                                                                                                      |
| Node.js 与 npm                               | 运行 REA CLI、MCP 和仓库构建                                     | [Node.js 24.22.1 x64](https://nodejs.org/dist/v24.22.1/) 自带 npm。本仓库支持的范围见 [package.json](package.json)。                                                                                                                                         |
| REA / rea-unity                              | 检查 IL2CPP 元数据、UnityFS、程序集和 APK                        | 6.10.1。下面给出 npm 安装和仓库构建两种入口。                                                                                                                                                                                                                |
| Codex                                        | 通过 MCP 调用 REA 或 Unity Editor                                | 使用已有 Codex 客户端。命令行用 `codex mcp get rea` 验证注册。                                                                                                                                                                                               |
| AssetRipper                                  | 导出场景、资源和可编辑项目                                       | [2.0.0 Windows x64](https://github.com/AssetRipper/AssetRipper/releases/tag/2.0.0)。使用仓库脚本下载并校验。                                                                                                                                                 |
| Python 与 UnityPy                            | 检查资源、运行仓库的 APK 盘点脚本                                | [Python 3.12.10 x64](https://www.python.org/downloads/release/python-31210/) · [UnityPy 1.25.4](https://pypi.org/project/UnityPy/1.25.4/)                                                                                                                    |
| ILSpy 与 ilspycmd                            | 把保留托管方法体的 Mono DLL 反编译成可读 C#                      | [ILSpy 11.2](https://github.com/icsharpcode/ILSpy/releases/tag/v11.2) · [ilspycmd 11.2.0.10050](https://www.nuget.org/packages/ilspycmd/11.2.0.10050)                                                                                                        |
| .NET 10                                      | 运行 ILSpy 桌面版和相应 .NET 工具                                | [微软官方下载](https://dotnet.microsoft.com/download/dotnet/10.0)。桌面版用 Desktop Runtime，使用 `dotnet tool install` 时装 SDK。                                                                                                                           |
| Cpp2IL                                       | 解析 IL2CPP 并尝试恢复部分方法逻辑                               | [2022.1.0-pre-release.21](https://github.com/SamboyCoding/Cpp2IL/releases/tag/2022.1.0-pre-release.21)。Windows x64 选 `Cpp2IL-2022.1.0-pre-release.21-Windows.exe`。                                                                                        |
| Il2CppDumper                                 | 导出类型、方法地址和占位程序集                                   | [6.7.46](https://github.com/Perfare/Il2CppDumper/releases/tag/v6.7.46)。解压 Windows 发布包。                                                                                                                                                                |
| Ghidra 与 Temurin JDK                        | 反编译 Windows PE 或 Android ELF 原生库                          | [Ghidra 12.2](https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.2_build) · [Temurin JDK 25 x64](https://adoptium.net/temurin/releases/?version=25)。Windows 下将工具和临时项目放在无中文、目录名不以点开头的路径。                     |
| JADX CLI 与 JADX MCP 桥                      | 查看 APK 的 manifest、Java/Kotlin 层。REA 通过桥接 JAR 调用 JADX | [JADX 1.5.7](https://github.com/skylot/jadx/releases/tag/v1.5.7) · [jadx-headless-mcp 0.7.1](docs/guides/android/android-analysis.md)。桥接文档有下载地址和 SHA-256。                                                                                        |
| Unity Hub、Unity Editor 与 Funplay Unity MCP | 导入、编译、验证场景与运行状态                                   | [Unity Hub](https://unity.com/download) · [Editor 归档](https://unity.com/releases/editor/archive) · [Funplay 0.7.0 安装说明](https://github.com/FunplayAI/funplay-unity-mcp)。Editor 优先选与样本或目标工程兼容的版本。Windows 样本验证使用 2022.3.14f1c1。 |

按目标补充模块。连接 Android 真机时用 [Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools) 的 `adb`。构建 Android 或 WebGL 时，在 Unity Hub 安装目标 Editor 对应的构建模块。微信小游戏项目使用项目要求的转换 SDK 和 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)。Spine 资源只在实际用到时按项目版本引入 [Spine Unity Runtime](https://github.com/EsotericSoftware/spine-runtimes)。

## 安装 REA

只用发布包时，安装 Node.js 后运行以下命令。

```powershell
npm install --global rea-agents@6.10.1
rea --version
```

要运行这个仓库的版本，在仓库根目录执行下面的命令。Windows 构建需要同版本发布包中的 Windows 原生组件，因此先从 npm 安装一份固定版本，取出组件，再构建源码。

```powershell
npm ci
npm install --prefix .\.cache\rea-runtime --no-audit --no-fund --ignore-scripts rea-agents@6.10.1
New-Item -ItemType Directory -Force .\native\windows\build | Out-Null
Copy-Item .\.cache\rea-runtime\node_modules\rea-agents\native\windows\build\* .\native\windows\build
npm run build
node .\scripts\rea.mjs --version
```

## 安装资源与代码工具

在仓库根目录运行 AssetRipper 安装脚本。它会核对 SHA-256，默认把文件放到 `.cache/assetripper/2.0.0/win-x64`。需要使用已下载的发布包时，传 `-ArchivePath`。

```powershell
.\scripts\install-assetripper.ps1
& .\.cache\assetripper\2.0.0\win-x64\AssetRipper.GUI.Free.exe --version

py -3.12 -m venv .\.cache\unity-python
& .\.cache\unity-python\Scripts\python.exe -m pip install UnityPy==1.25.4
& .\.cache\unity-python\Scripts\python.exe -c "import UnityPy; print(UnityPy.__version__)"

winget install --id icsharpcode.ILSpy --exact --source winget
dotnet tool install --global ilspycmd --version 11.2.0.10050
ilspycmd --version
```

Cpp2IL 下载后运行 `--list-output-formats`。Il2CppDumper 用同一构建的 `GameAssembly.dll` 或 `libil2cpp.so`、`global-metadata.dat` 和空输出目录验收。自动执行时可把它的 `config.json` 中 `RequireAnyKey` 设为 `false`。如果旧版发布包找不到它声明的 .NET 运行时，先按错误中的版本安装相应运行时。本项目也用 .NET 10 和当前进程的 `DOTNET_ROLL_FORWARD=Major` 跑通过同版本样本。

## 为 Codex 配置 REA MCP

解压 JDK、Ghidra、JADX CLI，再下载桥接 JAR 并按 Android 指南校验哈希。以下路径为示例，改成实际安装路径。只做 Mono 或资源分析时，可以省略对应外部工具的环境变量。

```powershell
$env:JAVA_HOME = 'C:\UnityTools\jdk-25'
$env:GHIDRA_INSTALL_DIR = 'C:\UnityTools\ghidra_12.2_PUBLIC'
$env:REA_JADX_MCP_JAR = 'C:\UnityTools\jadx-headless-mcp-0.7.1-all.jar'
$node = (Get-Command node -ErrorAction Stop).Source
$rea = (Resolve-Path .\scripts\rea.mjs).Path

& "$env:JAVA_HOME\bin\java.exe" -version
& 'C:\UnityTools\jadx-1.5.7\bin\jadx.bat' --version
& $node $rea providers --json

codex mcp add rea --env "JAVA_HOME=$env:JAVA_HOME" --env "GHIDRA_INSTALL_DIR=$env:GHIDRA_INSTALL_DIR" --env "REA_JADX_MCP_JAR=$env:REA_JADX_MCP_JAR" -- $node $rea mcp
codex mcp get rea
```

只装了全局 npm 版时，使用 `npm root --global` 输出目录下的 `rea-agents/scripts/rea.mjs` 作为 `$rea`。注册完成后新开 Codex 会话。Windows 版 REA 的 Ghidra 接口用于支持的原生 PE 等格式。分析 Android ELF 时可直接用 Ghidra，IL2CPP 元数据和匹配 ELF 也可以先交给 REA 的内置检查。

Unity 工程在 Package Manager 使用 Funplay 安装页的 Git URL 或 OpenUPM 入口，再从 Unity 菜单 `Funplay > MCP Server` 启动。按实际端口连接，先读项目和场景状态，再做导入或 Play Mode 验证。

## 验收顺序

1. Windows Mono 用 `ilspycmd <Assembly-CSharp.dll>` 查看 C#。IL2CPP 用 `rea inspect-il2cpp-metadata <global-metadata.dat> --binary <同一构建的二进制> --json` 查看方法名和地址。
2. 资源用 `rea inspect-artifact <UnityFS资源包> --json` 查看成员清单，再用 AssetRipper 导出到空目录。
3. Android 用 `rea inspect-android-package <base.apk> --json` 验证 JADX 桥。完整游戏输入还要核对同一构建的架构和资源分包。
4. 用 Unity 打开导出的副本，记录编译、场景引用和实机运行结果。工具安装通过、资源导出通过、原生方法分析通过和可玩验收分别记录。

下一步按 [项目技能入口](skill.md) 选择 Android、桌面端或工程处理流程。更多配置见 [REA 安装文档](docs/getting-started/installation.md) 和 [Windows Ghidra 指南](docs/providers/windows-ghidra-p0.md)。
