#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

release_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd /opt/trello
exec 9>/opt/trello/deploy.lock
flock -w 600 9

export APP_IMAGE="${1:?Pass an immutable GHCR image digest}"
if [[ ! "$APP_IMAGE" =~ ^ghcr\.io/tamhuynhtee/trello-fastapi@sha256:[a-f0-9]{64}$ ]]; then
  echo 'Unexpected image reference' >&2
  exit 1
fi
test -s /opt/trello/.env
chmod 600 /opt/trello/.env
compose=(docker compose --project-name trello-staging -f "$release_dir/compose.staging.yml")

"${compose[@]}" config --quiet
"${compose[@]}" pull
"${compose[@]}" run --rm --no-deps caddy caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
# The migration uses the direct Neon URL from .env and runs only once.
# If it fails, set -e aborts before replacing the running application.
"${compose[@]}" run --rm --no-deps api alembic upgrade head
"${compose[@]}" up -d --wait --wait-timeout 180

# Check DB connectivity and public HTTPS once per deploy, not continuously.
curl --fail --silent --show-error --retry 12 --retry-all-errors \
  --retry-delay 5 --connect-timeout 10 --max-time 20 \
  https://staging-api.tamhuynh.site/api/v1/health

if [[ -f last-successful-image ]]; then
  cp last-successful-image previous-image
  cp last-successful-release previous-release
fi
printf '%s\n' "$APP_IMAGE" > last-successful-image
printf '%s\n' "$release_dir" > last-successful-release
echo 'Staging deploy succeeded.'
