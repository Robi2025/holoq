#!/usr/bin/env bash
# scripts/publish_github.sh
# Uso:
#   ./scripts/publish_github.sh <repo-name> [public|private|internal]
# Requisitos: git (obligatorio), gh (opcional pero recomendado).
# Si 'gh' no está instalado, el script mostrará los comandos manuales para hacer push.

set -euo pipefail

REPO_NAME="${1:-holoq}"
VISIBILITY="${2:-public}"  # public|private|internal
DEFAULT_BRANCH="${DEFAULT_BRANCH:-main}"

if ! command -v git >/dev/null 2>&1; then
  echo "ERROR: se requiere 'git' instalado y en el PATH." >&2
  exit 1
fi

if [ ! -d .git ]; then
  echo "Inicializando repo git..."
  git init
fi

echo "Agregando archivos y creando commit inicial (si aplica)..."
git add .
# Evitar fallo si ya existe un commit
git commit -m "Initial commit: HoloQ MVP" || true

echo "Ajustando rama por defecto a '$DEFAULT_BRANCH'..."
git branch -M "$DEFAULT_BRANCH"

if command -v gh >/dev/null 2>&1; then
  echo "Creando repo remoto con GitHub CLI (gh)..."
  # Si quieres usar una org: pasa ORG/REPO como primer argumento
  gh repo create "$REPO_NAME" --"$VISIBILITY" --source . --remote origin --push
  echo "Listo ✅ Repositorio publicado en GitHub."
else
  echo "AVISO: No se encontró 'gh'. Crea el repo manualmente en GitHub y luego ejecuta:"
  echo "  git remote add origin https://github.com/<USUARIO>/$REPO_NAME.git"
  echo "  git push -u origin $DEFAULT_BRANCH"
fi
