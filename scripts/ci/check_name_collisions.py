#!/usr/bin/env python3
"""
CI gate: in HiseScript an identifier that names an inline function resolves to the
function even where a var of the same name is in scope. The kit list once drew every
row at y ~0 because its `var ky` met the STAGE camera helper `inline function ky`.
Fails if any var / local / reg / const name equals a function name in Scripts/.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "hise_project" / "ResearchFacility" / "Scripts"
src = "\n".join(p.read_text(errors="ignore") for p in ROOT.rglob("*.js"))
src = re.sub(r"//[^\n]*", "", src)
funcs = set(re.findall(r"\binline\s+function\s+([A-Za-z_]\w*)", src)) | set(re.findall(r"(?<!inline )\bfunction\s+([A-Za-z_]\w*)\s*\(", src))
names = set(re.findall(r"\b(?:var|local|reg|const\s+var|const)\s+([A-Za-z_]\w*)", src))
hits = sorted(funcs & names)
if hits:
    print("ERROR: variable names that shadow functions (HiseScript resolves them to the function):", ", ".join(hits))
    sys.exit(1)
print(f"name collision check: {len(funcs)} functions, {len(names)} variables, no collisions")
