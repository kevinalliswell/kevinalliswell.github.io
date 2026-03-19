#!/usr/bin/env bash

set -euo pipefail

require_env() {
  local name="$1"
  if [[ -z "${!name:-}" ]]; then
    echo "Missing required environment variable: ${name}" >&2
    exit 1
  fi
}

require_env SITE_ROOT

DEPLOY_USER="${DEPLOY_USER:-deploy}"
WEB_GROUP="${WEB_GROUP:-www-data}"
RELEASES_TO_KEEP="${RELEASES_TO_KEEP:-5}"

if [[ "${EUID}" -ne 0 ]]; then
  echo "Please run as root." >&2
  exit 1
fi

install -d -m 2775 -o "${DEPLOY_USER}" -g "${WEB_GROUP}" "${SITE_ROOT}"
install -d -m 2775 -o "${DEPLOY_USER}" -g "${WEB_GROUP}" "${SITE_ROOT}/releases"
install -d -m 2775 -o "${DEPLOY_USER}" -g "${WEB_GROUP}" "${SITE_ROOT}/shared"
install -d -m 2775 -o "${DEPLOY_USER}" -g "${WEB_GROUP}" "${SITE_ROOT}/shared/logs"

if [[ ! -L "${SITE_ROOT}/current" ]]; then
  ln -sfn "${SITE_ROOT}/releases" "${SITE_ROOT}/current"
fi

cat <<EOF
Independent site bootstrap completed.

SITE_ROOT=${SITE_ROOT}
DEPLOY_USER=${DEPLOY_USER}
WEB_GROUP=${WEB_GROUP}
RELEASES_TO_KEEP=${RELEASES_TO_KEEP}

Next steps:
1. Put your web server root on ${SITE_ROOT}/current
2. Add the deploy user's public key to ~/.ssh/authorized_keys
3. Configure GitHub repository Variables and Secrets
4. Run the independent site workflow once
EOF
