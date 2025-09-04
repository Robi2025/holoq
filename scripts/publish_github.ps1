# scripts/publish_github.ps1
# Uso:
#   pwsh -File scripts/publish_github.ps1 -RepoName holoq -Visibility public -DefaultBranch main
# Requisitos: git (obligatorio), gh (opcional).

param(
  [string]$RepoName = "holoq",
  [ValidateSet("public","private","internal")] [string]$Visibility = "public",
  [string]$DefaultBranch = "main"
)

function Require-Command($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
    Write-Error "ERROR: se requiere '$name' instalado y en el PATH."
    exit 1
  }
}

Require-Command git

if (-not (Test-Path ".git")) {
  Write-Host "Inicializando repo git..."
  git init | Out-Null
}

Write-Host "Agregando archivos y creando commit inicial (si aplica)..."
git add . | Out-Null
# Evitar fallo si ya existe un commit
git commit -m "Initial commit: HoloQ MVP" 2>$null | Out-Null

Write-Host "Ajustando rama por defecto a '$DefaultBranch'..."
git branch -M $DefaultBranch | Out-Null

if (Get-Command gh -ErrorAction SilentlyContinue) {
  Write-Host "Creando repo remoto con GitHub CLI (gh)..."
  # Para usar una organización, pasa ORG/REPO en -RepoName
  gh repo create $RepoName --$Visibility --source . --remote origin --push | Out-Null
  Write-Host "Listo ✅ Repositorio publicado en GitHub."
} else {
  Write-Warning "No se encontró 'gh'. Crea el repo manualmente en GitHub y luego ejecuta:"
  Write-Host "  git remote add origin https://github.com/<USUARIO>/$RepoName.git"
  Write-Host "  git push -u origin $DefaultBranch"
}
