#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

INSTALL_TOOLS=false
if [[ "${1:-}" == "--install-tools" ]]; then
  INSTALL_TOOLS=true
fi

echo "== Agent workflow bootstrap =="
echo "root: $ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "missing: python3"
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  if [[ "$INSTALL_TOOLS" == "true" ]]; then
    echo "installing uv"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
  else
    echo "missing: uv"
    echo "run: tools/agent-workflow/bootstrap-dev.sh --install-tools"
    exit 1
  fi
fi

if ! command -v git >/dev/null 2>&1; then
  echo "missing: git"
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "initializing git repository"
  git init
  git branch -m main >/dev/null 2>&1 || true
fi

if ! command -v br >/dev/null 2>&1; then
  if [[ "$INSTALL_TOOLS" == "true" ]]; then
    echo "installing beads_rust br"
    curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/beads_rust/main/install.sh?$(date +%s)" | bash -s -- --skip-skills
  else
    echo "missing: br"
    echo "run: tools/agent-workflow/bootstrap-dev.sh --install-tools"
  fi
fi

uv sync
uv run awf bootstrap
uv run awf install-hooks

if command -v br >/dev/null 2>&1 && [[ ! -f .beads/beads.db ]]; then
  echo "initializing br workspace"
  RUST_LOG=error br init || true
fi

echo "next:"
echo "  uv run awf context-index"
echo "  uv run awf repo-hygiene"
echo "  uv run awf workflow-fixture-test"
