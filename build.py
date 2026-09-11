import os
import shutil
import subprocess
import tempfile
import tomllib
from pathlib import Path

# This script is a poetry build directive which copies the alembic migrations
# from the branch, tag, or rev indicated in pyproject.toml for gearboxdatamodel.
#
# NOTE: The gearboxdatamodel's migrations/env.py should be verified to include
# compare_type=True in both run_migrations_offline() and run_migrations_online()
# so that `alembic revision --autogenerate` detects column-type changes. If it
# is omitted, type drift will be silently missed during autogenerate.


def _is_commit_sha(value: str) -> bool:
    """Return True if *value* looks like a Git commit SHA (7–40 hex chars)."""
    return 7 <= len(value) <= 40 and all(c in "0123456789abcdefABCDEF" for c in value)


def build(setup_kwargs):
    destination = Path(os.getcwd()) / "migrations"

    # Use the stdlib TOML parser (Python ≥ 3.11) instead of a fragile regex so
    # that any valid TOML formatting (multi-line tables, different key order,
    # single-quoted strings, etc.) is handled correctly.
    with open("pyproject.toml", "rb") as f:
        config = tomllib.load(f)

    deps = config.get("tool", {}).get("poetry", {}).get("dependencies", {})
    dep = deps.get("gearboxdatamodel")
    if dep is None:
        raise Exception(
            "Unable to locate gearboxdatamodel dependency in pyproject.toml."
        )
    if not isinstance(dep, dict) or "git" not in dep:
        raise Exception(
            "gearboxdatamodel dependency must be a table with a 'git' key "
            "(e.g., { git = '...', branch = '...' })."
        )

    repo_url = dep["git"]
    ref = dep.get("branch") or dep.get("rev") or dep.get("tag")
    if ref is None:
        raise Exception(
            "gearboxdatamodel dependency must specify 'branch', 'rev', or 'tag'."
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        # git clone -b accepts branch names and tags but NOT commit SHAs.
        # When ref looks like a SHA, clone the default branch then checkout.
        if _is_commit_sha(ref):
            clone_args = ["git", "clone", repo_url, tmpdir]
        else:
            clone_args = ["git", "clone", "-b", ref, repo_url, tmpdir]

        try:
            subprocess.run(clone_args, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            stderr_text = e.stderr.decode(errors="replace")
            print(f"ERROR: {stderr_text}")
            raise RuntimeError(
                f"Build.py: git clone failed (return code {e.returncode}): {stderr_text}"
            ) from e
        except Exception as e:
            raise RuntimeError(
                f"Build.py: unexpected error running git clone: {e}"
            ) from e

        if _is_commit_sha(ref):
            try:
                subprocess.run(
                    ["git", "-C", tmpdir, "checkout", ref],
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as e:
                stderr_text = e.stderr.decode(errors="replace")
                print(f"ERROR: {stderr_text}")
                raise RuntimeError(
                    f"Build.py: git checkout {ref} failed "
                    f"(return code {e.returncode}): {stderr_text}"
                ) from e

        source_dir = Path(tmpdir) / "migrations"
        if not source_dir.exists():
            raise FileNotFoundError(
                f"'migrations' directory not found in cloned repo at {tmpdir}."
            )

        # Copy to a sibling staging path first so that a failed copy never
        # leaves the project without a migrations/ directory.  Once the copy
        # succeeds, atomically replace the old directory with the new one.
        dest_parent = destination.parent
        dest_staging = dest_parent / f".migrations_new_{os.getpid()}"
        try:
            shutil.copytree(source_dir, dest_staging)
        except Exception:
            if dest_staging.exists():
                shutil.rmtree(dest_staging, ignore_errors=True)
            raise

        if destination.exists():
            shutil.rmtree(destination)
        dest_staging.rename(destination)
        print(f"Successfully copied {source_dir.name} to {destination}")


if __name__ == "__main__":
    build({})
