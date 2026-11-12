#!/usr/bin/env python3
"""CI gate (docs/21 licence boundary): personal-use sample libraries never enter the repo.

The SAMPLES page reads a private index that lives in the plug-in's AppData folder.
That index, its source database and any renders of personal-use sounds must stay
out of git. This fails when a tracked file names them. Patterns are assembled from
pieces so this file does not match itself.
"""
import subprocess
import sys

VENDOR = "Spl" + "ice"
# a library path or its database name in tracked code means private data leaked in;
# the index file NAME in a comment does not, so only tracked index files are checked
PATTERNS = ["/" + VENDOR + "/", "sounds" + ".db"]
SCOPES = ["hise_project", "scripts", ".github", "assets", "packaging"]


def main():
    bad = []
    for pat in PATTERNS:
        r = subprocess.run(["git", "grep", "-n", "-I", "-F", pat, "--"] + SCOPES, capture_output=True, text=True)
        bad += [ln for ln in r.stdout.splitlines() if ln]
    tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.splitlines()
    bad += [f + ": tracked private data file" for f in tracked
            if f.endswith(("index.json", "user.json")) and "SampleBrowser" in f or f.endswith("sounds" + ".db")]
    if bad:
        print("licence boundary check FAILED: private sample data or paths in tracked files")
        print("\n".join(bad[:40]))
        sys.exit(1)
    print("licence boundary check: clean")


if __name__ == "__main__":
    main()
