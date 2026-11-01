# AssetRipper

AssetRipper is a separately licensed Unity asset analysis and export tool, not a component of REA. The free edition is distributed under [GNU GPL v3.0](https://github.com/AssetRipper/AssetRipper/blob/2.0.0/LICENSE.md); its authors and contributors are credited in the [upstream project](https://github.com/AssetRipper/AssetRipper). REA does not bundle or relicense the executable.

For Windows x64, run the optional installer from the repository root:

```powershell
./scripts/install-assetripper.ps1
```

It downloads the official [2.0.0 release](https://github.com/AssetRipper/AssetRipper/releases/tag/2.0.0), verifies SHA-256 `9a7ef0e7c5c3ea5b90b4e6d855e2d98d5f7ec8c3f9e26fccbc194c6a7b01baf7`, and extracts the archive to `.cache/assetripper/2.0.0/win-x64`. This directory is local and ignored by Git. The installer refuses to overwrite an existing destination, does not install other software, and does not launch AssetRipper. To use a previously downloaded official archive, provide `-ArchivePath <path>`; `-Destination <path>` selects a different new directory.

Launch `AssetRipper.GUI.Free.exe` manually, then use the address printed in its window. Before loading or exporting, check that the service is not being used by another session; preserve original files and export to a new directory. See the [desktop recovery skill](../../.agents/skills/unity-pc-game-recovery/SKILL.md) for the analysis and validation workflow. For other platforms, obtain the appropriate release directly from upstream.
