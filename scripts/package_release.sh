#!/usr/bin/env bash
# Create a clean, portable download archive of the application source.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-$ROOT/dist}"
ARCHIVE="$OUT_DIR/genai-job-pipeline.zip"
mkdir -p "$OUT_DIR"
rm -f "$ARCHIVE"

cd "$ROOT"
git archive --format=zip --prefix=genai-job-pipeline/ HEAD \
  .env.example .gitignore Dockerfile README.md docker-compose.yml requirements.txt \
  app applications dashboard jobs matching resumes sheets tests scripts \
  -o "$ARCHIVE"
printf 'Created download archive: %s\n' "$ARCHIVE"
