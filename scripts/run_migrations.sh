#!/usr/bin/env bash
# Run all SQL migrations in order.
set -euo pipefail

MIG_DIR="${MIG_DIR:-matchcore/db/migrations}"
DATABASE_URL="${DATABASE_URL:-postgresql://ccifa:ccifa@localhost:5432/matchcore}"

if ! command -v psql >/dev/null 2>&1; then
  echo "psql is required" >&2
  exit 1
fi

echo "Running migrations from $MIG_DIR"
for f in $(ls "$MIG_DIR"/*.sql 2>/dev/null | sort); do
  echo "  -> $f"
  psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f "$f"
done

echo "Migrations complete."
