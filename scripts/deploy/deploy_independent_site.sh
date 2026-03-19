#!/usr/bin/env bash

set -euo pipefail

require_env() {
  local name="$1"
  if [[ -z "${!name:-}" ]]; then
    echo "Missing required environment variable: ${name}" >&2
    exit 1
  fi
}

require_env ARCHIVE_PATH
require_env SSH_PRIVATE_KEY
require_env DEPLOY_HOST
require_env DEPLOY_USER
require_env DEPLOY_PATH

DEPLOY_PORT="${DEPLOY_PORT:-22}"
RELEASE_ID="${RELEASE_ID:-$(date -u +%Y%m%d%H%M%S)-${GITHUB_SHA:-manual}}"
RELEASE_ID="${RELEASE_ID//\//-}"
REMOTE_ARCHIVE="/tmp/${RELEASE_ID}.tar.gz"

workdir="$(mktemp -d)"
trap 'rm -rf "${workdir}"' EXIT

key_path="${workdir}/deploy_key"
known_hosts="${workdir}/known_hosts"

printf '%s\n' "${SSH_PRIVATE_KEY}" > "${key_path}"
chmod 600 "${key_path}"
ssh-keyscan -p "${DEPLOY_PORT}" "${DEPLOY_HOST}" > "${known_hosts}" 2>/dev/null

ssh_base=(
  ssh
  -i "${key_path}"
  -o UserKnownHostsFile="${known_hosts}"
  -o StrictHostKeyChecking=yes
  -p "${DEPLOY_PORT}"
)

scp_base=(
  scp
  -i "${key_path}"
  -o UserKnownHostsFile="${known_hosts}"
  -o StrictHostKeyChecking=yes
  -P "${DEPLOY_PORT}"
)

remote_target="${DEPLOY_USER}@${DEPLOY_HOST}"

"${ssh_base[@]}" "${remote_target}" "mkdir -p '${DEPLOY_PATH}/releases'"
"${scp_base[@]}" "${ARCHIVE_PATH}" "${remote_target}:${REMOTE_ARCHIVE}"

"${ssh_base[@]}" "${remote_target}" \
  "DEPLOY_PATH='${DEPLOY_PATH}' RELEASE_ID='${RELEASE_ID}' REMOTE_ARCHIVE='${REMOTE_ARCHIVE}' bash -s" <<'EOF'
set -euo pipefail

release_dir="${DEPLOY_PATH}/releases/${RELEASE_ID}"
mkdir -p "${release_dir}"
tar -xzf "${REMOTE_ARCHIVE}" -C "${release_dir}"
ln -sfn "${release_dir}" "${DEPLOY_PATH}/current"
rm -f "${REMOTE_ARCHIVE}"

find "${DEPLOY_PATH}/releases" -mindepth 1 -maxdepth 1 -type d | sort | head -n -5 | xargs -r rm -rf --

echo "Deployed release: ${release_dir}"
EOF
