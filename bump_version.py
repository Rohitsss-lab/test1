import sys, re
from pathlib import Path

bump_type = sys.argv[1] if len(sys.argv) > 1 else "patch"
version   = Path("VERSION").read_text().strip()
major, minor, patch = map(int, version.split("."))

if bump_type == "major": major += 1; minor = 0; patch = 0
elif bump_type == "minor": minor += 1; patch = 0
else: patch += 1

new_version = f"{major}.{minor}.{patch}"
Path("VERSION").write_text(new_version)
print(new_version)
