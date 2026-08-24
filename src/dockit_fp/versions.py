"""Immutable Git-source version manifests and historical site builds."""

from __future__ import annotations

from dataclasses import dataclass
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

from .build import build_site
from .errors import DocKitError
from .safety import prepare_output

MOVING_REFS = {"head", "main", "master", "develop", "development", "latest"}
COMMIT = re.compile(r"^[0-9a-fA-F]{40}$")


@dataclass(frozen=True)
class Version:
    release: str
    source_ref: str


@dataclass(frozen=True)
class VersionManifest:
    current: str
    versions: tuple[Version, ...]


@dataclass(frozen=True)
class BuildAllResult:
    release_count: int
    page_count: int


def load_manifest(root: Path) -> VersionManifest:
    path = root / "docs" / "versions.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise DocKitError(f"{path}: invalid version manifest: {error}") from error
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise DocKitError(f"{path}: field 'schema_version' must be 1")
    current, entries = data.get("current"), data.get("versions")
    if not isinstance(current, str) or not isinstance(entries, list) or not entries:
        raise DocKitError(f"{path}: fields 'current' and non-empty 'versions' are required")
    versions: list[Version] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or not isinstance(entry.get("release"), str) or not isinstance(entry.get("source_ref"), str):
            raise DocKitError(f"{path}: versions[{index}] needs string release and source_ref")
        versions.append(Version(entry["release"], entry["source_ref"]))
    releases = [entry.release for entry in versions]
    if len(set(releases)) != len(releases) or current not in releases:
        raise DocKitError(f"{path}: releases must be unique and include current {current!r}")
    return VersionManifest(current, tuple(versions))


def _run_git(root: Path, *arguments: str, binary: bool = False) -> str | bytes:
    completed = subprocess.run(["git", *arguments], cwd=root, capture_output=True, text=not binary)
    if completed.returncode:
        detail = completed.stderr.decode() if binary else completed.stderr
        raise DocKitError(f"Git {' '.join(arguments)} failed: {detail.strip()}")
    return completed.stdout


def _is_immutable(root: Path, source_ref: str) -> bool:
    if source_ref.lower() in MOVING_REFS:
        return False
    if COMMIT.fullmatch(source_ref):
        return True
    completed = subprocess.run(["git", "show-ref", "--verify", "--quiet", f"refs/tags/{source_ref}"], cwd=root)
    return completed.returncode == 0


def check_release(root: Path) -> VersionManifest:
    root = root.resolve()
    manifest = load_manifest(root)
    for entry in manifest.versions:
        if not _is_immutable(root, entry.source_ref):
            raise DocKitError(
                f"docs/versions.json: published release {entry.release!r} must not use moving source_ref {entry.source_ref!r}; use a tag or full commit SHA."
            )
        try:
            _run_git(root, "rev-parse", "--verify", f"{entry.source_ref}^{{commit}}")
        except DocKitError as error:
            raise DocKitError(
                f"Cannot build documentation version {entry.release}: source_ref {entry.source_ref!r} does not resolve to a Git object."
            ) from error
    return manifest


def _archive_to(root: Path, source_ref: str, destination: Path) -> None:
    archive = _run_git(root, "archive", "--format=tar", source_ref, binary=True)
    assert isinstance(archive, bytes)
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        for member in bundle.getmembers():
            target = (destination / member.name).resolve()
            if not target.is_relative_to(destination.resolve()):
                raise DocKitError(f"Git archive contains unsafe path {member.name!r}")
        bundle.extractall(destination, filter="data")


def build_all(*, root: Path, output: Path) -> BuildAllResult:
    """Build all manifest releases exclusively from their immutable Git source."""
    root = root.resolve()
    manifest = check_release(root)
    output = output.resolve()
    prepare_output(output)
    page_count = 0
    with tempfile.TemporaryDirectory(prefix="dockit-fp-") as temporary:
        staging = Path(temporary)
        targets = tuple((item.release, f"{item.release}/index.html") for item in manifest.versions)
        for item in manifest.versions:
            source = staging / item.release
            source.mkdir()
            _archive_to(root, item.source_ref, source)
            result = build_site(root=source, output=output / item.release, release=item.release, versions=targets)
            page_count += result.page_count
    (output / "versions.json").write_text(json.dumps({
        "schema_version": 1, "current": manifest.current,
        "versions": [{"release": item.release, "source_ref": item.source_ref} for item in manifest.versions],
    }, indent=2) + "\n", encoding="utf-8")
    (output / "index.html").write_text(
        f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={manifest.current}/index.html"><a href="{manifest.current}/index.html">Open {manifest.current} documentation</a>\n',
        encoding="utf-8",
    )
    return BuildAllResult(len(manifest.versions), page_count)
