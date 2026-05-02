#!/usr/bin/env python3
"""
Export Superset configurations to JSON for version control
"""
import sqlite3
import json
import os
import sys
import subprocess

EXPORTS_DIR = "./exports"
IMPORTANT_TABLES = [
    'dashboards', 'slices', 'tables', 'dbs', 
    'table_columns', 'dashboard_slices', 'sql_metrics',
    'saved_query', 'query', 'database_connection'
]

def export_from_container():
    """Extract and export Superset config from container"""
    
    print("🐳 Copie de la BD depuis le conteneur...")
    db_file = f"{EXPORTS_DIR}/superset-temp.db"
    
    result = subprocess.run(
        ["docker", "cp", "superset_app:/app/superset_home/superset.db", db_file],
        capture_output=True
    )
    
    if result.returncode != 0:
        print(f"❌ Erreur: {result.stderr.decode()}")
        return False
    
    print(f"✅ BD copiée")
    
    # Export depuis SQLite
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print(f"\n📦 Export des tables importantes...")
        for table in IMPORTANT_TABLES:
            try:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                data = [dict(row) for row in rows]
                
                output_file = f"{EXPORTS_DIR}/{table}.json"
                with open(output_file, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
                
                count = len(rows)
                print(f"   ✅ {table}.json ({count} items)")
            except sqlite3.OperationalError:
                pass  # Table doesn't exist
        
        conn.close()
        os.remove(db_file)
        
        print("\n✅ Export terminé!")
        print(f"📁 Fichiers dans: {EXPORTS_DIR}/")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        if os.path.exists(db_file):
            os.remove(db_file)
        return False

if __name__ == "__main__":
    if not os.path.isdir(EXPORTS_DIR):
        os.makedirs(EXPORTS_DIR)
    
    success = export_from_container()
    sys.exit(0 if success else 1)
