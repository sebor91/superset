#!/bin/bash
set -e

# Configuration
SUPERSET_URL="http://localhost:8088"
EXPORTS_DIR="./exports"
ADMIN_USER="admin"
ADMIN_PASSWORD="${ADMIN_PASSWORD:?Set ADMIN_PASSWORD before running this script}"

echo "🔐 Récupération du token d'authentification..."
TOKEN=$(curl -s -X POST "$SUPERSET_URL/api/v1/security/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$ADMIN_USER\",\"password\":\"$ADMIN_PASSWORD\"}" \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Erreur d'authentification"
  exit 1
fi

echo "✅ Token obtenu"
echo ""

# Fonction pour exporter une ressource
export_resource() {
  local resource=$1
  local endpoint=$2
  local output_file="$EXPORTS_DIR/${resource}.json"
  
  echo "📦 Export des $resource..."
  curl -s -X GET "$SUPERSET_URL/api/v1/$endpoint" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    | python3 -m json.tool > "$output_file"
  
  if [ -f "$output_file" ]; then
    echo "   ✅ Sauvegardé: $output_file"
  else
    echo "   ❌ Erreur lors de l'export"
  fi
}

# Exports
export_resource "dashboards" "dashboards?q=(page_size:1000)"
export_resource "datasets" "datasets?q=(page_size:1000)"
export_resource "charts" "charts?q=(page_size:1000)"

echo ""
echo "🎉 Export terminé!"
ls -lh $EXPORTS_DIR/*.json
