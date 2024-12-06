"""Version Management Script for Vector SDK.

This script manages version numbers across the Vector SDK project files. It updates
version numbers in both pyproject.toml and __init__.py files consistently.

Usage:
    python bump_version.py <command> [version]

Commands:
    major     - Bump major version (X.y.z -> X+1.0.0)
    minor     - Bump minor version (x.Y.z -> x.Y+1.0)
    patch     - Bump patch version (x.y.Z -> x.y.Z+1)
    rc        - Bump/add release candidate (x.y.z -> x.y.zrc1 or x.y.zrcN -> x.y.zrcN+1)
    release   - Convert RC to release version (x.y.zrcN -> x.y.z)
    set       - Set to specific version (requires version argument)
"""

import re
import sys
from pathlib import Path

VERSION_FILES = [
    Path("pyproject.toml"),
    Path("src/vector_sdk/__init__.py"),
    Path("uv.lock"),
]


def read_version() -> str:
    """Read current version from pyproject.toml."""
    try:
        with open(VERSION_FILES[0]) as f:
            content = f.read()
        match = re.search(r'version\s*=\s*["\'](.+?)["\']', content)
        if not match:
            raise ValueError(f"Version not found in {VERSION_FILES[0]}")
        return match.group(1)
    except Exception as e:
        print(f"Error reading version: {e}")
        sys.exit(1)


def update_version(new_version: str) -> None:
    """Update version in all project files."""
    for file_path in VERSION_FILES:
        if not file_path.exists():
            print(f"Warning: {file_path} not found, skipping...")
            continue

        try:
            with open(file_path) as f:
                content = f.read()

            if file_path.name == "pyproject.toml":
                pattern = r'(\[project\][^\[]*version\s*=\s*["\'])(.+?)(["\'])'
            elif file_path.name == "__init__.py":
                pattern = r'(__version__\s*=\s*["\'])(.+?)(["\'])'
            elif file_path.name == "uv.lock":
                pattern = r'(version\s*=\s*")(.+?)(")'
            else:
                continue

            updated_content = re.sub(pattern, rf"\g<1>{new_version}\g<3>", content)

            # Verify the substitution worked
            if content == updated_content:
                print(f"Warning: No version pattern match in {file_path}")
                continue

            with open(file_path, "w") as f:
                f.write(updated_content)

            print(f"Updated version in {file_path} to {new_version}")

        except Exception as e:
            print(f"Error updating {file_path}: {e}")
            sys.exit(1)


def parse_version(version_str: str) -> tuple[str, str, str, int]:
    """Parse version string into parts."""
    try:
        if "rc" in version_str:
            main_part, rc_part = version_str.split("rc")
            rc_num = int(rc_part)
        else:
            main_part = version_str
            rc_num = 0

        parts = main_part.split(".")
        if len(parts) != 3:
            raise ValueError("Version must be in format X.Y.Z or X.Y.ZrcN")

        return parts[0], parts[1], parts[2], rc_num

    except Exception as e:
        print(f"Error parsing version: {e}")
        sys.exit(1)


def bump_version(bump_type: str, target_version: str | None = None) -> None:
    """Bump version according to specified type."""
    try:
        current_version = read_version()
        print(f"Current version: {current_version}")

        major, minor, patch, rc_num = parse_version(current_version)

        if target_version:
            new_version = target_version
        else:
            if bump_type == "major":
                new_version = f"{int(major) + 1}.0.0"
            elif bump_type == "minor":
                new_version = f"{major}.{int(minor) + 1}.0"
            elif bump_type == "patch":
                new_version = f"{major}.{minor}.{int(patch) + 1}"
            elif bump_type == "rc":
                if rc_num == 0:
                    new_version = f"{major}.{minor}.{patch}rc1"
                else:
                    new_version = f"{major}.{minor}.{patch}rc{rc_num + 1}"
            elif bump_type == "release":
                if rc_num > 0:
                    new_version = f"{major}.{minor}.{patch}"
                else:
                    new_version = f"{major}.{minor}.{int(patch) + 1}"
            else:
                raise ValueError(
                    'Invalid bump type. Use "major", "minor", "patch", "rc", '
                    '"release", or "set"'
                )

        update_version(new_version)
        print(f"Successfully bumped version from {current_version} to {new_version}")

        # Return the new version for use in scripts
        return new_version

    except Exception as e:
        print(f"Error bumping version: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python bump_version.py <major|minor|patch|rc|release>")
        print("   or: python bump_version.py set <version>")
        sys.exit(1)

    bump_type = sys.argv[1]
    try:
        if bump_type == "set" and len(sys.argv) == 3:
            target_version = sys.argv[2]
            bump_version(bump_type, target_version)
        else:
            bump_version(bump_type)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
