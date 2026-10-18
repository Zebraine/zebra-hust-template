import argparse
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile


def run(*command, cwd=None):
    print("+ " + " ".join(map(str, command)), flush=True)
    return subprocess.run(
        list(map(str, command)), cwd=cwd, check=True, text=True, stdout=subprocess.PIPE,
    ).stdout.strip()


def main():
    parser = argparse.ArgumentParser(description="Validate and submit a Typst package using jj and gh.")
    parser.add_argument("--dry-run", action="store_true", help="Only prepare and compile locally; no GitHub changes.")
    parser.add_argument("--draft", action="store_true", help="Create a draft PR.")
    parser.add_argument("--font-path", action="append", default=[], help="Additional font directory (repeatable).")
    args = parser.parse_args()
    required = ("typst",) if args.dry_run else ("typst", "jj", "gh")
    for executable in required:
        if shutil.which(executable) is None:
            raise RuntimeError(f"Missing command: {executable}")

    root = Path(__file__).resolve().parents[1]
    release = runpy.run_path(str(root / "scripts/prepare-release.py"))
    package = release["package"]
    manifest = release["manifest"]
    name, version = package["name"], package["version"]
    if not args.dry_run:
        run("gh", "auth", "status")
        if run("jj", "diff", "--name-only", cwd=root):
            raise RuntimeError("Commit the source changes with jj before submitting.")

    (root / "build").mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="submit-", dir=root / "build"))
    local_packages = work / "packages"
    staged = release["prepare_release"](local_packages / "preview" / name / version)
    spec = f"@preview/{name}:{version}"
    project = work / "project"
    print(run("typst", "init", "--package-path", local_packages, spec, project))
    font_args = []
    for font_path in args.font_path:
        font_args.extend(("--font-path", str(Path(font_path).resolve())))
    entrypoint = project / manifest["template"]["entrypoint"]
    for source in sorted(project.glob("*.typ")):
        run("typst", "compile", "--package-path", local_packages, *font_args,
            source, source.with_suffix(".pdf"))
    thumbnail = staged / manifest["template"]["thumbnail"]
    run("typst", "compile", "--package-path", local_packages, *font_args,
        "--pages", "1", "--ppi", "150", entrypoint, thumbnail)
    if thumbnail.stat().st_size > 3 * 1024 * 1024:
        raise RuntimeError("Thumbnail exceeds 3 MiB")
    print(f"Validated release: {staged}")
    if args.dry_run:
        print("No remote changes made.")
        return

    owner = run("gh", "api", "user", "--jq", ".login")
    branch = f"release-{name}-{version}"
    existing = json.loads(run(
        "gh", "pr", "list", "--repo", "typst/packages", "--state", "open",
        "--head", f"{owner}:{branch}", "--json", "url",
    ))
    if existing:
        raise RuntimeError(f"An open PR already exists: {existing[0]['url']}")
    run("gh", "repo", "fork", "typst/packages", "--clone=false")
    fork = json.loads(run("gh", "api", f"repos/{owner}/packages"))
    if fork.get("parent", {}).get("full_name") != "typst/packages":
        raise RuntimeError("The target repository is not a fork of typst/packages")

    registry = work / "registry"
    run("jj", "git", "clone", "--depth", "1", "--branch", "main",
        "--remote", "upstream", "https://github.com/typst/packages.git", registry)
    destination = registry / "packages" / "preview" / name / version
    if destination.exists():
        raise RuntimeError(f"{spec} is already published; increment the version")
    run("jj", "git", "remote", "add", "origin", fork["ssh_url"], cwd=registry)
    run("jj", "git", "fetch", "--remote", "origin", "--branch", branch, cwd=registry)
    if run("jj", "bookmark", "list", "--remote", "origin", cwd=registry):
        raise RuntimeError(f"Remote bookmark {branch} already exists; refusing to overwrite it")
    shutil.copytree(staged, destination)
    run("jj", "describe", "-m", f"{name}:{version}", cwd=registry)
    run("jj", "bookmark", "create", branch, cwd=registry)
    run("jj", "bookmark", "track", f"{branch}@origin", cwd=registry)
    run("jj", "git", "push", "--remote", "origin", "--bookmark", branch, cwd=registry)
    body = (
        f"## Summary\n\nAdd {spec}.\n\n"
        f"{package['description']}\n\n"
        f"Source: {package.get('repository', '')}\n\n"
        "## Validation\n\n"
        "- Initialized the staged template with typst init.\n"
        "- Compiled all top-level template examples.\n"
        "- Generated the thumbnail from the initialized default template.\n"
        "- Excluded font files and development artifacts.\n\n"
        "This is an unofficial HUST template.\n"
    )
    flags = ["--draft"] if args.draft else []
    print(run("gh", "pr", "create", "--repo", "typst/packages", "--base", "main",
              "--head", f"{owner}:{branch}", "--title", f"{name}:{version}",
              "--body", body, *flags))
    print(f"Submission checkout retained at {registry}")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, OSError, subprocess.CalledProcessError) as error:
        sys.exit(str(error))
