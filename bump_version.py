import sys
import re

def bump_version(version: str, part: str = "patch") -> str:
    major, minor, patch = map(int, version.strip().split("."))

    if part == "patch":
        if patch < 9:
            patch += 1
        elif minor < 9:
            minor += 1
            patch = 0
        else:
            major += 1
            minor = 0
            patch = 0
    elif part == "minor":
        if minor < 9:
            minor += 1
            patch = 0
        else:
            major += 1
            minor = 0
            patch = 0
    elif part == "major":
        major += 1
        minor = 0
        patch = 0

    return f"{major}.{minor}.{patch}"


if __name__ == "__main__":
    version_file = sys.argv[1]  # e.g. "version.txt"
    part = sys.argv[2] if len(sys.argv) > 2 else "patch"

    with open(version_file) as f:
        current = f.read().strip()

    new_version = bump_version(current, part)
    print(f"Bumping {current} → {new_version}")

    with open(version_file, "w") as f:
        f.write(new_version + "\n")
