from pathlib import Path
import shutil
import tomllib
import re

root = Path(__file__).resolve().parents[1]
manifest = tomllib.loads((root / "typst.toml").read_text())
package = manifest["package"]


def prepare_release(destination):
    if not re.fullmatch(r"[a-z][a-z0-9-]*", package["name"]):
        raise ValueError("Invalid package name")
    if not re.fullmatch(r"\d+\.\d+\.\d+", package["version"]):
        raise ValueError("Expected a stable version such as 0.1.0")
    destination.mkdir(parents=True, exist_ok=False)
    for filename in ("typst.toml", "lib.typ", "config.typ", "README.md", "LICENSE", "thumbnail.png"):
        shutil.copy2(root / filename, destination / filename)
    for directory in ("modules", "presets", "template"):
        shutil.copytree(root / directory, destination / directory)
    (destination / "images").mkdir()
    shutil.copy2(root / "images/HUSTGreen.svg", destination / "images/HUSTGreen.svg")
    for filename in [destination / "README.md", *destination.rglob("*.typ")]:
        content = filename.read_text()
        content = re.sub(
            rf"@preview/{re.escape(package['name'])}:[0-9]+\.[0-9]+\.[0-9]+",
            f"@preview/{package['name']}:{package['version']}",
            content,
        )
        filename.write_text(content)
    return destination


if __name__ == "__main__":
    print(prepare_release(root / "build" / "preview" / package["name"] / package["version"]))
