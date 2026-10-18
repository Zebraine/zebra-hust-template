from pathlib import Path
import shutil
import tomllib

root = Path(__file__).resolve().parents[1]
manifest = tomllib.loads((root / "typst.toml").read_text())
package = manifest["package"]
destination = root / "build" / "preview" / package["name"] / package["version"]
destination.mkdir(parents=True, exist_ok=False)
for filename in ("typst.toml", "lib.typ", "config.typ", "README.md", "LICENSE", "thumbnail.png"):
    shutil.copy2(root / filename, destination / filename)
for directory in ("modules", "presets", "template"):
    shutil.copytree(root / directory, destination / directory)
(destination / "images").mkdir()
shutil.copy2(root / "images/HUSTGreen.svg", destination / "images/HUSTGreen.svg")
print(destination)
