#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${1:-8000}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required to run local preview." >&2
  exit 1
fi

if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
  echo "Error: port must be a number. Example: ./scripts/preview.sh 8000" >&2
  exit 1
fi

if ! python3 - "$PORT" <<'PY'
import socket
import sys

port = int(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind(("127.0.0.1", port))
except OSError:
    sys.exit(1)
finally:
    s.close()
PY
then
  echo "Error: port $PORT is already in use on localhost." >&2
  echo "Try another port, e.g. ./scripts/preview.sh 18080" >&2
  exit 1
fi

echo "Serving muTouch project page from: $ROOT_DIR"
echo "Open: http://localhost:${PORT}"
echo "Press Ctrl+C to stop."

cd "$ROOT_DIR"
python3 -m http.server "$PORT"
