# 🔧 Superset Configuration Management

Guide pour versionner les configurations Superset dans Git tout en sécurisant les secrets.

## 📋 Structure

```text
superset/
├── exports/                    ✅ VERSIONNÉ (Git)
│   ├── dashboards.json         # Dashboard configurations
│   ├── slices.json             # Charts/visualizations
│   ├── tables.json             # Datasets metadata
│   ├── dbs.json                # Database connections (no credentials)
│   ├── table_columns.json      # Dataset columns/schema
│   ├── README.md               # Documentation
│   └── ...autres exports
│
├── docker/
│   ├── .env                    ❌ IGNORÉ (Git) - Contains secrets!
│   ├── docker-compose.yml      ✅ VERSIONNÉ
│   └── ...
│
├── docker-compose-image-tag.yml ✅ VERSIONNÉ
└── ...autres fichiers

```

## 🔐 Sécurité

### Secrets IGNORÉS par Git

- `superset/docker/.env` - Contient DATABASE_PASSWORD, ADMIN_PASSWORD
- Fichiers temporaires `.db`, scripts de déploiement

### Configuration VERSIONNÉE

- `superset/exports/*.json` - Configuration des dashboards, charts, datasets
- `superset/docker-compose-image-tag.yml` - Version, image, services
- Documentation et README

## 📦 Exporter les configurations

Pour sauvegarder les changements dans Git:

```bash
cd /path/to/superset

# Copier la DB depuis le conteneur
docker cp superset_app:/app/superset_home/superset.db ./exports/superset-temp.db

# Extraire les configurations importantes
python3 << 'EOF'
import sqlite3, json, os

conn = sqlite3.connect("./exports/superset-temp.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Tables importantes
tables_to_export = [
    'dashboards', 'slices', 'tables', 'dbs', 
    'table_columns', 'dashboard_slices', 'sql_metrics'
]

for table in tables_to_export:
    cursor.execute(f"SELECT * FROM {table}")
    data = [dict(row) for row in cursor.fetchall()]
    with open(f"./exports/{table}.json", 'w') as f:
        json.dump(data, f, indent=2, default=str)
    print(f"✅ {table}.json exported")

conn.close()
os.remove("./exports/superset-temp.db")
print("✅ Export complete!")
EOF

# Commit dans Git
git add superset/exports/
git commit -m "chore: update Superset configuration export"
```

## 🔄 Restaurer les configurations

Pour recréer la configuration depuis Git (après un redéploiement):

1. Lancer Superset avec `docker-compose up`
2. Attendre l'initialisation (2-3 minutes)
3. Importer les dashboards/charts via l'UI Superset ou script (à implémenter)

Note: Pour l'instant, les exports servent de **backup et documentation**.
Une véritable restauration automatisée nécessiterait un script de restauration.

## ⚙️ .env Configuration

Le fichier `docker/.env` DOIT exister mais NE doit PAS être committé:

```env
# Ne JAMAIS committer ce fichier !
ADMIN_PASSWORD=SEB91_superset           # Secret!
DATABASE_PASSWORD=DbSuperset_2026!      # Secret!
POSTGRES_PASSWORD=DbSuperset_2026!      # Secret!

# OK de committer ces variables:
TAG=4.1.2
SECRET_KEY=/Jdzr7pI53iYE7w1...
```

## ✅ Checklist pour les développeurs

- [ ] Mettre à jour les dashboards/charts dans Superset
- [ ] Exécuter le script d'export
- [ ] `git add superset/exports/`
- [ ] `git commit`
- [ ] JAMAIS ajouter `.env` à Git (gitignore en place)

## 📚 Références

- Exports SQLite: `exports/README.md` pour plus de détails
- Configuration PostgreSQL: `documentations/superset.MD`
- Docker setup: `docker-compose-image-tag.yml`
