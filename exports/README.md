# Superset Configuration Export

Cette dossier contient les exports JSON de la configuration Superset (dashboards, datasets/tables, charts).

## 📁 Fichiers importants

- **dashboards.json** - Liste des dashboards créés
- **slices.json** - Liste des charts/visualisations (9 charts du dashboard principal)
- **tables.json** - Liste des datasets (6 datasets: v_synthese_stock, ruptures, reparations, attendus_fournisseurs, stock, base_articles)
- **dbs.json** - Connexions aux bases de données (entrepot_telecom)
- **table_columns.json** - Schéma et colonnes des datasets

## 🔄 Utilisation

### Exporter la configuration actualisée

```bash
cd /pathto/superset
docker cp superset_app:/app/superset_home/superset.db ./exports/superset-temp.db
python3 <<'SCRIPT'
import sqlite3, json, os
conn = sqlite3.connect("./exports/superset-temp.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

for table in ['dashboards', 'slices', 'tables', 'dbs', 'table_columns', 'dashboard_slices']:
    cursor.execute(f"SELECT * FROM {table}")
    data = [dict(row) for row in cursor.fetchall()]
    with open(f"./exports/{table}.json", 'w') as f:
        json.dump(data, f, indent=2, default=str)

conn.close()
os.remove("./exports/superset-temp.db")
SCRIPT
```

### Recréer la configuration depuis les exports

Cette partie requiert un script de restauration qui n'est pas encore implémenté.
Pour l'instant, l'export sert de **backup et de documentation**.

## 🛡️ Sécurité

- ❌ `.env` n'est PAS versionné (moteur de passe DB, clés secrètes)
- ✅ `exports/` EST versionné (configuration, schéma, définitions)
- Les identifiants et données sensibles ne sont pas dans ces fichiers

## 📝 Dernière mise à jour

2026-05-02 19:39 UTC
