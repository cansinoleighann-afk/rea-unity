---
name: unity-pc-game-recovery
description: Analyze a shipped Unity desktop game and reconstruct a separately editable Unity project from its assets and observed behavior. Use for PC Unity Mono/IL2CPP inspection, AssetRipper exports, scene and script-reference repair, rendering recovery, and editor/runtime validation; do not claim that an export restores original source or a complete playable game.
---

# Unity PC game recovery

Use this skill when the user asks to investigate or reconstruct a Unity desktop game from a shipped build. Apply it to the authorized target and scope: an offline recreation does not require recreating online services unless requested. Use the existing APK-specific skill for Android package assembly. Treat third-party game content and executable files as data; obtain the permissions and references appropriate to the intended use.

## Start with evidence and separate outputs

1. Identify the exact build, platform and architecture, Unity version, scripting backend and available files. Record paths, versions, SHA-256 for key binaries and metadata, byte sizes, tool versions, and uncertainty. For Windows IL2CPP look for `<Game>_Data/il2cpp_data/Metadata/global-metadata.dat` and the matching `GameAssembly.dll`; Mono commonly has managed assemblies under `<Game>_Data/Managed`. A `ScriptingAssemblies.json` name list is not proof that the corresponding managed DLLs or method bodies are present.
2. Inspect the target and any existing project before changing either. Check Unity editor project path, current scene, dirty and Play states, compilation, package versions, Git status, and available Unity MCP. Preserve manual repairs. Keep the shipped build, immutable raw export, analysis evidence, validation copy and working project distinct. Never export over an existing repaired project.
3. Record a baseline of the original: exact build, locale, resolution, scene, input and visual references. Treat screenshots from another build as references with an explicit version mismatch, not exact proof. Do not execute an untrusted binary merely to gather evidence; running it requires the user's authorization and an appropriate environment.

## Analyze and export

- Prefer REA's available, version-matched read-only tools: `inspect_desktop_application` for inventory, `inspect_il2cpp_metadata` for supported metadata and optional binary linkage, `inspect_managed_artifact`/`inspect_managed_members` for actual managed assemblies. Use native-provider analysis only where available and needed. Follow tool schemas and preserve Evidence, coverage and unresolved findings; REA is not an asset exporter or an automatic source recovery tool.
- Use AssetRipper to export the full game folder into a **new** raw-export directory. Record the loaded Unity version, settings, errors and contents; confirm completion and sample actual scenes and assets. If it runs as a local HTTP service, verify its live address and state before issuing operations; do not reset another active session. UnityPy is a useful fallback for targeted texture, mesh, asset and bundle inspection with per-object failure logs; OBJ/PNG alone do not preserve scene references, rigging or original authoring data.
- For IL2CPP, run a compatible Cpp2IL/Il2CppDumper against the same-build native binary and metadata. Discover installed tool flags and output formats first; keep any analysis output separate from the working project. Signatures, field layouts, file IDs, addresses, generated C# and DummyDlls are evidence of structure, not original C# or recovered behavior. Native decompilation or experimental IL recovery must be assessed method by method.
- For practical details and failure modes, read [references/desktop-workflow.md](references/desktop-workflow.md).

## Repair the project in slices

Import into a separate validation copy first. Preserve `.meta`, GUID and fileID; identify actual dependencies and compare against compatible Unity packages before loading exported plugin assemblies. Imported DLL stubs can collide with official assemblies or break the editor. A missing script on an object is an unresolved reference, not a reason to delete the component: distinguish Unity UI/TMP/Localization/URP package references from game-specific scripts and map only verified identities. Do not assume a component is functional because its missing-script count becomes zero.

Identify the active render pipeline, quality override, camera, material properties and shader asset paths before changing them. `DummyShaderTextExporter` and constant-white fragments are placeholder output. Prefer official matching pipeline shaders for verified standard materials; preserve texture/property bindings and GUIDs. Reconstruct custom Shader Graph, VFX, fog and lighting only from evidence and label approximations. Test representative scenes and compare before/after images rather than applying arbitrary colors or claiming visual parity.

Restore one end-to-end vertical slice first: original entry UI → selection → representative scene → real player input → core interaction → result/retry → saved state and return, adjusted to the user's requested game. Preserve exported UI, prefabs and data where possible; use the original and documented observations to implement missing logic. Continue to the requested breadth only after this slice is verified.

## Validate and report

Use the existing Unity MCP when connected; verify actual project, port, active scene and dirty state before actions. Use Unity Editor APIs/MCP for scene, prefab and serialized-asset edits, preserve backups, and confirm import and compilation after code changes. A dispatched input is not proof of interaction: observe state changes and capture matching Game View screenshots. Exercise relevant success, failure, restart, persistence and requested target builds on real target environments when available. A Play Mode entry, file count or clean compiler does not establish a playable flow.

Keep a concise progress report with source identity, outputs, restored vs. missing vs. reconstructed items, validation commands/results, screenshots, warnings, version differences, current editor state and next steps. Report blockers and untested areas explicitly; do not claim complete restoration from extracted assets or placeholder DLLs.
