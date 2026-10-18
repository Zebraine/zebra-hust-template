import argparse
import base64
import json
from pathlib import Path
import runpy
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib


def run(*command, cwd=None):
    print("+ " + " ".join(map(str, command)), flush=True)
    return subprocess.run(
        list(map(str, command)), cwd=cwd, check=True, text=True, stdout=subprocess.PIPE,
    ).stdout.strip()


def check_dependencies(staged, package):
    dependencies = set()
    for source in staged.rglob("*.typ"):
        dependencies.update(re.findall(r'@preview/([a-z0-9-]+):(\d+\.\d+\.\d+)', source.read_text()))
    errors = []
    for name, version in sorted(dependencies):
        if name == package["name"]:
            if version != package["version"]:
                errors.append(f"Incorrect self import: {name}:{version}")
            continue
        endpoint = f"repos/typst/packages/contents/packages/preview/{name}"
        versions = json.loads(run("gh", "api", endpoint))
        stable = [entry["name"] for entry in versions if re.fullmatch(r"\d+\.\d+\.\d+", entry["name"])]
        latest = max(stable, key=lambda value: tuple(map(int, value.split("."))))
        if version != latest:
            errors.append(f"{name}:{version} is outdated; latest is {latest}")
        encoded = run("gh", "api", f"{endpoint}/{version}/typst.toml", "--jq", ".content")
        dependency = tomllib.loads(base64.b64decode(encoded).decode())["package"]
        minimum = dependency.get("compiler", "0.0.0")
        if tuple(map(int, minimum.split("."))) > tuple(map(int, package["compiler"].split("."))):
            errors.append(f"{name} requires Typst {minimum}; update package.compiler")
    if errors:
        raise RuntimeError("\n".join(errors))


def prepare_pr_body(package, work):
    encoded = run("gh", "api", "repos/typst/packages/contents/.github/pull_request_template.md",
                  "--jq", ".content")
    official = re.sub(r"<!--.*?-->", "", base64.b64decode(encoded).decode(), flags=re.S).strip()
    if "Description: Explain what the package does and why it's useful." not in official:
        raise RuntimeError("The official PR template changed; review the script before proceeding")
    body = official.replace("- [ ] a new package", "- [x] a new package")
    body = body.replace(
        "Description: Explain what the package does and why it's useful.",
        f"Description: {package['description']} Students can start with course-report or cs-thesis "
        "and examples of figures, tables, citations, and appendices. This is an unofficial template.",
    )
    body = body.replace("  - Explanation:", "  - Explanation: zebra is a non-descriptive prefix; "
                        "HUST is the university abbreviation. The name does not claim official status.", 1)
    body += f"\n\nPackage: @preview/{package['name']}:{package['version']}\n"
    body += f"Source: {package['repository']}\n"
    body += "\nCode is MIT; template text is MIT-0. Third-party images retain their own rights.\n"
    body += "Please review the asset permissions and license notices before checking the licensing boxes.\n"
    destination = work / "pr-body.md"
    destination.write_text(body)
    return destination, official


def validate_pr_body(body, official):
    required = [line for line in official.splitlines()
                if line.startswith("- [ ] ") and line != "- [ ] an update for a package"]
    for line in required:
        if line.replace("- [ ]", "- [x]", 1) not in body:
            raise RuntimeError("PR checklist is incomplete: " + line)
    if "- [x] an update for a package" in body:
        raise RuntimeError("This workflow submits a new package version, not an update to an existing version")


def main():
    parser = argparse.ArgumentParser(description="Validate and submit a Typst package using jj and gh.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and prepare PR text; GitHub reads only.")
    parser.add_argument("--draft", action="store_true", help="Create a draft PR.")
    parser.add_argument("--font-path", action="append", default=[], help="Additional font directory (repeatable).")
    parser.add_argument("--branch", help="New fork bookmark to create; existing bookmarks are never overwritten.")
    parser.add_argument("--upstream-url", default="https://github.com/typst/packages.git",
                        choices=("https://github.com/typst/packages.git", "git@github.com:typst/packages.git"),
                        help="Transport used to clone the official registry with jj.")
    args = parser.parse_args()
    required = ("typst", "gh") if args.dry_run else ("typst", "jj", "gh")
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
    check_dependencies(staged, package)
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
    body_path, official = prepare_pr_body(package, work)
    print(f"PR checklist awaiting review: {body_path}")
    if args.dry_run:
        print("No remote changes made.")
        return

    input(f"Review {body_path}, verify permissions, and check the applicable boxes. Press Enter when done: ")
    body = body_path.read_text()
    validate_pr_body(body, official)
    owner = run("gh", "api", "user", "--jq", ".login")
    branch = args.branch or f"release-{name}-{version}"
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]*", branch):
        raise RuntimeError("Use a simple bookmark name containing letters, digits, dots, underscores, or hyphens")
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
        "--remote", "upstream", args.upstream_url, registry)
    destination = registry / "packages" / "preview" / name / version
    if destination.exists():
        raise RuntimeError(f"{spec} is already published; increment the version")
    run("jj", "git", "remote", "add", "origin", fork["ssh_url"], cwd=registry)
    run("jj", "git", "fetch", "--remote", "origin", "--branch", branch, cwd=registry)
    if run("jj", "bookmark", "list", "--remote", "origin", cwd=registry):
        raise RuntimeError(f"Remote bookmark {branch} already exists; refusing to overwrite it")
    shutil.copytree(staged, destination)
    expected = {str(path.relative_to(registry)) for path in destination.rglob("*") if path.is_file()}
    changed = set(run("jj", "diff", "--name-only", cwd=registry).splitlines())
    if changed != expected:
        raise RuntimeError("Registry diff contains missing or unexpected files")
    base = run("jj", "log", "-r", "@-", "--no-graph", "-T", "commit_id", cwd=registry)
    run("jj", "describe", "-m", f"{name}:{version}", cwd=registry)
    run("jj", "bookmark", "create", branch, cwd=registry)
    run("jj", "bookmark", "track", f"{branch}@origin", cwd=registry)
    commit = run("jj", "log", "-r", "@", "--no-graph", "-T", "commit_id", cwd=registry)
    print(run("jj", "diff", "--stat", cwd=registry))
    if input("Type push to publish this jj commit to your fork: ").strip() != "push":
        raise RuntimeError(f"Stopped before push. Checkout retained at {registry}")
    run("jj", "git", "push", "--remote", "origin", "--bookmark", branch, cwd=registry)
    remote = run("gh", "api", f"repos/{owner}/packages/git/ref/heads/{branch}", "--jq", ".object.sha")
    if remote != commit:
        raise RuntimeError("Fork commit does not match the local jj commit")
    remote_files = set(run("gh", "api", f"repos/{owner}/packages/compare/{base}...{commit}",
                           "--paginate", "--jq", ".files[].filename").splitlines())
    if remote_files != expected:
        raise RuntimeError("Fork diff does not match the staged package")
    print(f"Review fork diff: https://github.com/{owner}/packages/compare/{base}...{commit}")
    print(body)
    if input("Type create-pr to submit this reviewed fork commit: ").strip() != "create-pr":
        raise RuntimeError("Stopped after push; no PR created")
    flags = ["--draft"] if args.draft else []
    print(run("gh", "pr", "create", "--repo", "typst/packages", "--base", "main",
              "--head", f"{owner}:{branch}", "--title", f"{name}:{version}",
              "--body", body, *flags))
    print(f"Submission checkout retained at {registry}")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, OSError, EOFError, KeyboardInterrupt, subprocess.CalledProcessError) as error:
        sys.exit(str(error))
