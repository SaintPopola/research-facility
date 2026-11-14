#!/usr/bin/env python3
"""CI gate (docs/21, doc 23 B21): personal-use sound libraries never enter the repo.

The SAMPLES page reads a private index in the plug-in's AppData folder, and some
recordings are made from instruments whose licences forbid redistribution. Neither
the libraries, their databases, their file paths nor any audio from them may be
tracked here. Three checks, all case-insensitive:

1. Code and data (hise_project, scripts, .github, assets, packaging): no vendor
   library path fragments or library database names.
2. Docs and design: no concrete path INTO a library (a folder or file below the
   library root). Naming a product or a database in prose is fine.
3. Sample maps: no absolute FileName (a map must point at the project's Samples).
Plus: no tracked private index, user data or database files.

Every pattern is assembled from pieces so this file does not match itself.
"""
import re
import subprocess
import sys

S = "spl" + "ice"
SP = "spectra" + "sonics"
DB = "sounds" + ".db"

CODE_SCOPES = ["hise_project", "scripts", ".github", "assets", "packaging"]
CODE_FRAGMENTS = ["/" + S + "/", "com." + S + ".", DB, SP + "/steam", "/key" + "scape/", "/omni" + "sphere/"]

DOC_SCOPES = ["docs", "design"]
DOC_REGEXES = [S + r"/sounds/packs/[a-z0-9]", SP + r"/steam/[a-z]", r"/users/[^/\s]+/" + S + "/"]

PRIVATE_FILE_RE = re.compile(r"(^|/)(sample" + "browser/.*\\.json|" + re.escape(DB) + r"(-wal|-shm)?)$", re.I)
ABS_MAP_RE = re.compile(r'FileName="(/|[a-z]:\\\\)', re.I)


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True, text=True).stdout


def main():
    bad = []
    for frag in CODE_FRAGMENTS:
        bad += [ln for ln in git("grep", "-n", "-I", "-i", "-F", frag, "--", *CODE_SCOPES).splitlines() if ln]
    for rx in DOC_REGEXES:
        bad += [ln for ln in git("grep", "-n", "-I", "-i", "-E", rx, "--", *DOC_SCOPES).splitlines() if ln]
    tracked = git("ls-files").splitlines()
    bad += [f + ": tracked private data file" for f in tracked if PRIVATE_FILE_RE.search(f)]
    for f in tracked:
        if "/SampleMaps/" in f and f.endswith(".xml"):
            with open(f, encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh, 1):
                    if ABS_MAP_RE.search(line):
                        bad.append("%s:%d: absolute sample path in a map" % (f, i))
                        break
    if bad:
        print("licence boundary check FAILED: private library data or paths in tracked files")
        print("\n".join(bad[:40]))
        sys.exit(1)
    print("licence boundary check: clean (code, docs, sample maps, tracked files)")


if __name__ == "__main__":
    main()
