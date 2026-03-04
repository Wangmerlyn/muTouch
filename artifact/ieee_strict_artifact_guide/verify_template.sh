#!/usr/bin/env bash
set -euo pipefail

base_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
local_cls="${base_dir}/IEEEtran.cls"
upstream_cls="${base_dir}/upstream_template/IEEEtran.cls"

if [[ ! -f "${local_cls}" ]]; then
  echo "ERROR: missing ${local_cls}" >&2
  exit 1
fi

if [[ ! -f "${upstream_cls}" ]]; then
  echo "ERROR: missing ${upstream_cls}" >&2
  exit 1
fi

local_hash="$(sha256sum "${local_cls}" | awk '{print $1}')"
upstream_hash="$(sha256sum "${upstream_cls}" | awk '{print $1}')"

echo "local    : ${local_hash}"
echo "upstream : ${upstream_hash}"

if [[ "${local_hash}" != "${upstream_hash}" ]]; then
  echo "FAIL: IEEEtran.cls does not match upstream template copy" >&2
  exit 2
fi

echo "OK: IEEEtran.cls matches upstream template copy"
