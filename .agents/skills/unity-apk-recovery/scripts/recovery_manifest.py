"""Create a deterministic, evidence-first inventory for Unity APK/XAPK/APKS inputs."""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory_archive(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        lower = [name.lower() for name in names]
        markers = {
            "unity": any("unityplayer" in name or "assets/bin/data" in name for name in lower),
            "il2cpp": any(name.endswith("global-metadata.dat") or "libil2cpp.so" in name for name in lower),
            "mono": any(name.endswith("assembly-csharp.dll") for name in lower),
            "assetbundles": sum("assetbundle" in name or "/bundles/" in name for name in lower),
            "splits": sum(name.endswith(".apk") for name in lower),
        }
        return {"fileCount": len(names), "markers": markers, "entries": names[:200]}


def build_manifest(input_path: Path, output_path: Path) -> dict:
    manifest = {
        "schema": "unity-apk-recovery/1",
        "input": str(input_path.resolve()),
        "name": input_path.name,
        "size": input_path.stat().st_size,
        "sha256": sha256(input_path),
        "kind": input_path.suffix.lower().lstrip("."),
        "archive": None,
        "next": ["extract", "detect-unity", "export-assets"],
    }
    if zipfile.is_zipfile(input_path):
        manifest["archive"] = inventory_archive(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"input file not found: {args.input}")
    print(json.dumps(build_manifest(args.input, args.output), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
