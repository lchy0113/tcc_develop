#!/usr/bin/env bash
# Usage:
#   ./smartthings_token_check.sh               # 환경변수 SMARTTHINGS_TOKEN 사용
#   ./smartthings_token_check.sh <TOKEN>      # 인자 전달
# Env (optional):
#   CLI=smartthings  # smartthings CLI 바이너리 경로/이름 (기본: smartthings)

set -euo pipefail
CLI="${CLI:-smartthings}"
TOKEN="${1:-${SMARTTHINGS_TOKEN:-}}"

if [[ -z "${TOKEN}" ]]; then
  echo "❌ Token is empty. export SMARTTHINGS_TOKEN=... 또는 인자로 토큰을 주세요." >&2
  exit 2
fi

OUT="$(${CLI} locations --token="${TOKEN}" 2>&1 || true)"
RC=$?

if [[ ${RC} -eq 0 ]]; then
  echo "✅ Token is valid"
  exit 0
fi

if echo "${OUT}" | grep -qiE "401|authorization required|unauthorized|invalid token"; then
  echo "❌ Token invalid (401). 새 토큰 발급 필요." >&2
  exit 1
fi

if echo "${OUT}" | grep -qiE "429|Too Many Requests"; then
  echo "⚠️  Rate limited (429). 잠시 후 재시도." >&2
  exit 3
fi

echo "❌ Unknown error while checking token:" >&2
echo "${OUT}" >&2
exit 4
