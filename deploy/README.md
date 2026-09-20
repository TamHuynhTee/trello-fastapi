# Staging deployment

Target: `deploy@206.189.83.9`, `https://staging-api.tamhuynh.site`.
Requires Docker Compose supporting `up --wait`, curl, flock, direct Neon database
URL and `/opt/trello/.env` owned by deploy with mode 600. Put values in single
quotes in that file to preserve literal dollar signs. Never commit the file.

## One-time setup

1. Allow inbound TCP 80/443 in the DigitalOcean firewall and any host firewall.
   SSH on TCP 22 must also be reachable by the GitHub-hosted runner. Retain key-only
   SSH authentication. Only Caddy publishes ports; API port 8000 stays internal.
   Ensure the domain's A record points to the VPS and no stale AAAA points elsewhere.
2. On your Mac, create a dedicated automation key (do not overwrite an existing key):

   ```bash
   ssh-keygen -t ed25519 -C trello-staging-github -f ~/.ssh/trello_staging_ci -N ''
   ```

   Append the public `.pub` file to `/home/deploy/.ssh/authorized_keys` on the VPS.
   Optionally prefix this automation key's line with `restrict ` to disable SSH
   forwarding and PTY allocation. Never upload the private key to the VPS.
3. In the DigitalOcean console, obtain the SSH host public key and its fingerprint:

   ```bash
   cat /etc/ssh/ssh_host_ed25519_key.pub
   ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
   ```

   Construct known_hosts as `206.189.83.9 ssh-ed25519 BASE64_PUBLIC_HOST_KEY`.
   Use the public host key, not your personal login key. Verify via the provider
   console; do not blindly trust a key collected from the network.
4. In GitHub repository Settings > Environments, create `staging`, restrict deployment
   branches to `main`, and add environment secrets:

   | Secret | Value |
   | --- | --- |
   | VPS_HOST | 206.189.83.9 |
   | VPS_USER | deploy |
   | VPS_SSH_PRIVATE_KEY | Entire dedicated private key, including BEGIN/END lines |
   | VPS_KNOWN_HOSTS | Verified known_hosts line from step 3 |

5. The GHCR package is private by default. Create a GitHub personal access token
   (classic) with `read:packages` for an account allowed to read the package.
   On the VPS as deploy, log in without putting the token in shell history:

   ```bash
   read -rsp 'GHCR read token: ' GHCR_READ_TOKEN
   printf '\n'
   printf '%s' "$GHCR_READ_TOKEN" | docker login ghcr.io -u TamHuynhTee --password-stdin
   unset GHCR_READ_TOKEN
   ```

   Docker stores this credential in the deploy user's Docker config. Protect this
   account: docker group membership grants root-equivalent access. The workflow
   publishes using its own GITHUB_TOKEN; it does not need your personal token.

## First run and subsequent updates

Commit the app, tests, CI files and deploy directory together. PRs only run CI.
Merging into main runs verify, builds/publishes an amd64 image on the GitHub runner,
then deploys the exact digest through SSH. No build runs on the 512 MB VPS.
Alternatively run the workflow manually on main after setup.

Each upload is stored in a separate directory under `/opt/trello/releases`.
A host lock and GitHub concurrency serialize deploys. Migration failure aborts
before replacing the running app. Once replacement starts, failures do NOT
automatically rollback; consult logs and the previous successful release.
This single-container staging deployment has brief downtime and is not HA.

The deploy script runs `alembic upgrade head`, starts the app and Caddy, then checks
`/api/v1/health` over public HTTPS (including DB access). A root-page liveness check
runs periodically without waking Neon. Caddy certificate volumes are persistent.
No auth rate limiter is implemented; use test data/accounts on staging.

Validate after deployment:

```bash
curl -fsS https://staging-api.tamhuynh.site/api/v1/health
```

Then test register, login and `/me` via `/docs`.

## Troubleshooting and recovery

Inspect containers with `docker ps -a` and logs with
`docker logs --tail 100 trello-staging-api-1` or `trello-staging-caddy-1`.
Do not paste logs publicly without checking for connection strings.
If migration fails, fix the migration/configuration and rerun the workflow.
If health fails after replacement, an operator can restore the last successful
app and configuration, provided the current database schema remains compatible:

```bash
cd /opt/trello
export APP_IMAGE="$(cat last-successful-image)"
release_dir="$(cat last-successful-release)"
docker compose -p trello-staging -f "$release_dir/compose.staging.yml" up -d --wait
curl -fsS https://staging-api.tamhuynh.site/api/v1/health
```

These files exist only after a successful deployment. After a successful upgrade,
`previous-image`/`previous-release` identify the earlier successful version.
Rollback does not undo migrations; don't run `alembic downgrade` automatically.
Watch `free -h` and `df -h`: tagged images accumulate on the 10 GB disk. Remove
specific obsolete image tags after confirming they are not current or rollback
versions. Do not prune certificate volumes.
