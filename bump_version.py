import sys

with open("VERSION", "r") as f:
    version = f.read().strip()

major, minor, patch = version.split(".")

# Default bumps patch, but you can pass "minor" or "major" as argument
bump_type = sys.argv[1] if len(sys.argv) > 1 else "patch"

if bump_type == "major":
    major = int(major) + 1
    minor = 0
    patch = 0
elif bump_type == "minor":
    minor = int(minor) + 1
    patch = 0
else:
    patch = int(patch) + 1

new_version = f"{major}.{minor}.{patch}"

with open("VERSION", "w") as f:
    f.write(new_version)

print(new_version)
