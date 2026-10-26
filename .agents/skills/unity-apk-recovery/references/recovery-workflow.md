# APK 恢复流程与实测经验

## 输入与导出

记录输入大小、SHA256、包名、versionName/versionCode、Unity 版本、ABI 和后端。列出 APK/XAPK/APKS 内文件，再识别 base、架构 split、资源 split、OBB。安全解包时检查路径穿越、解压体积和重复内容冲突。

Mono 优先读取真实 Assembly-CSharp.dll；IL2CPP 需要同版本 global-metadata.dat 和对应 ABI 的 libil2cpp.so。完整程序集结构不等于方法代码。先确认工具对实际 metadata/Unity 版本的支持，不以生成 C# 文件数量计算成功率。

AssetRipper 导出原始场景、预制体、配置和素材，放入新的输出目录。单独建立修复工程，避免覆盖。IL2CPP 可结合 Cpp2IL、Il2CppDumper、ILSpy、IDA/Ghidra；候选 IL 要审查，空方法和反编译错误不能直接进入可用逻辑。

本机工具 `F:/1.Unity资料/逆向/tools/export_package.py` 支持 APK/XAPK/APKS 和目录批导出，`--help` 核对参数；默认 AssetRipper 服务 57841，导出目录必须不存在。该脚本会 Reset 服务，不能与别的导出并行共用实例。`recovery_tool.py` 是诊断/GUI 原型，不是完整一键恢复器。

## 原版基线

安卓模拟器方便安装指定版本、ADB、日志和运行时采集；Google Play 游戏电脑版方便试玩，但文件通常在 userdata.img 内。安装分包使用 `adb -s HOST:PORT install-multiple -r BASE.apk ABI_SPLIT.apk`，验证版本、进程、真实首屏和输入。

先记录同一关/位置/分辨率的画面、镜头、操作和任务切换。原版可运行后，再评估 Frida IL2CPP bridge 采集层级、对象位置和配置；架构翻译、root、版本兼容未测前不宣称可用。运行时 dump 不能自动还原整个编辑器工程。

## 引用、图集和运行库

- UGUI/TMP 脚本 GUID/fileID 不匹配会 MissingScript，按真实脚本身份映射并复扫引用，不能只按文件名猜。
- Spine 等包可能是同名空壳。根据 JSON 版本恢复真实运行库，隔离旧 stub/重复解析器，验证骨骼、顶点和动画；保留可复用 GUID。
- Sprite 的 m_RD.texture=0 和空 atlas 指针不表示图像不存在；结合 render-data key、atlas 标签和 SpriteAtlas map 查图集。
- UnityPy 抽取后必须实际看整树、草丛、手指、细杆、透明边缘，不能只看 PNG 数量。
- 本案例默认 SpriteHelper 用旧 Sprite UV 重投影到新图集，生成了碎片树。修复为保留 atlas rect/packing rotation，禁用旧 UV 重投影，再按几何蒙版裁切。其他包先抽样，不能通用盲套。
- 本包 GUID hash 映射为四个 uint 各转八位 hex、各自反转后拼接，另保留整数 key；普通 little-endian byte hex 不等价。先拿多张已知 Sprite 验证。
- 恢复个图要维护 PPU、pivot、border、裁切偏移和图集缩放；禁止隐式 NPOT 拉伸，曾出现 258×858 变 256×1024。
- Sprite.Create + EditorUtility.CopySerialized 可保留原 Sprite GUID/fileID，需备份、保存并视觉验证。拆成多纹理后，高跷网格不能继续共用一个旧图集材质，需子网格/对应材质或重新打图集。

## 场景恢复与视觉陷阱

先检查原场景、教学关、关卡块、终点标记、主题配置和生成器。不要在有原 TutorialPanel 的情况下先新画一套黄色菜单。

恢复 Tag、物理层、Sorting Layer、Canvas、字体和镜头。Sorting Layer 无法补救 Geometry/Transparent 队列不同造成的覆盖；本案例 VertexColor 的错误 Geometry 队列让天空盖住地面。

左轴心天空不能按中心放置，渐变纹理需正确 Clamp 和 UV 变换。背景树丛与底色填充必须使用一致轮廓，保留色调和各层视差。不能用任意布局冒充已捕获的原版位置。

地形优先用原曲线和序列化轮廓。按相同 X 的最大高度线性连接会把垂直高墙与平地连成假斜坡，并抬高背景；本案例改为地面碰撞采样，在边界两侧取样。比较草皮厚度、平滑坡面、悬崖包边、土层、水面和装饰；平坦教程起点不能冒充后面的跷跷板悬崖。

## 行为与平台验证

先复用原任务枚举、UI、教学关和动画，再补缺失方法，标记 reconstructed。站立、方向、连续迈步、失败、重试、检查点和通关分别验证。

Funplay 旧版同步拖动的 duration 只控制插值数，所有事件可能同帧派发，不能证明 InputSystem 读到了持续拖动。本案例用 MCP execute_code 的 EditorApplication.update 跨帧 QueueStateEvent(MouseState)，结果存 SessionState，再读回。直接调用组件方法只是组件测试，不是输入链验证。

中文化先验证真实 TMP 材质、字体字符覆盖和静态子集，再删旧字体；不直接把 8MB 源字体当压缩结果。WebGL 要检查原生 SDK、纹理压缩、音频、Shader、构建模块和浏览器；配置 Brotli 不等于构建和浏览器已通过。

## 参考资料

- 用户文章：https://xinyi234.github.io/2026/02/01/unity%E6%B8%B8%E6%88%8F%E9%80%86%E5%90%91/index.html
- Il2CppDumper：https://github.com/Perfare/Il2CppDumper （官方明确方法代码不在 DLL 恢复范围）
- UnityPy：https://github.com/K0lb3/UnityPy
- Frida bridge：https://github.com/vfsfitvnm/frida-il2cpp-bridge
- 原版画面：https://www.twomenandadog.fi/walkmaster

资料链接不代表对当前版本兼容，也不代表已执行运行时采集。
