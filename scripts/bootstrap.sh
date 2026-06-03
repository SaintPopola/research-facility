#!/usr/bin/env bash
# Research Facility bootstrap — fetches dependencies once D1 (base path) is chosen.
# Do not run this until docs/DECISIONS.md has D1 locked.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Research Facility bootstrap"
echo "    root: $ROOT"

# --- preflight ---
need() { command -v "$1" >/dev/null 2>&1 || { echo "missing: $1"; exit 1; }; }
need git
need cmake
need ninja || true  # optional; CMake can fall back to Make/Xcode
echo "==> tools ok"

# --- choose base path ---
PATH_CHOICE="${RF_PATH:-}"   # set RF_PATH=A or B in env, or pass --path=A
for a in "$@"; do
  case "$a" in
    --path=A|--path=a) PATH_CHOICE=A ;;
    --path=B|--path=b) PATH_CHOICE=B ;;
  esac
done

if [[ -z "$PATH_CHOICE" ]]; then
  cat <<EOF
==> No base path specified.

   Path A: fork Surge XT (GPL-3, recommended, see docs/RESEARCH.md)
   Path B: scratch JUCE 8 plugin from Pamplejuce (license-free)

   Re-run with:  ./scripts/bootstrap.sh --path=A
            or:  ./scripts/bootstrap.sh --path=B
EOF
  exit 2
fi

mkdir -p third_party
cd third_party

case "$PATH_CHOICE" in
  A)
    echo "==> Path A: fork Surge XT"
    if [[ ! -d surge ]]; then
      git clone --recursive https://github.com/surge-synthesizer/surge.git
    else
      echo "    surge already cloned"
    fi
    if [[ ! -d shortcircuit-xt ]]; then
      git clone --recursive https://github.com/surge-synthesizer/shortcircuit-xt.git
    fi
    if [[ ! -d sfizz ]]; then
      git clone --recursive https://github.com/sfztools/sfizz.git
    fi
    ;;
  B)
    echo "==> Path B: scratch from Pamplejuce"
    if [[ ! -d JUCE ]]; then
      git clone --branch master https://github.com/juce-framework/JUCE.git
    fi
    if [[ ! -d clap-juce-extensions ]]; then
      git clone --recursive https://github.com/free-audio/clap-juce-extensions.git
    fi
    if [[ ! -d sfizz ]]; then
      git clone --recursive https://github.com/sfztools/sfizz.git
    fi
    if [[ ! -d pamplejuce ]]; then
      git clone https://github.com/sudara/pamplejuce.git
    fi
    ;;
esac

cd "$ROOT"
echo "==> bootstrap complete"
echo "    next: read docs/ROADMAP.md → Phase 0"
