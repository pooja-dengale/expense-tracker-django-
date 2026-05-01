#!/usr/bin/env python
import os
import sys
import django
import sqlite3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
django.setup()

from django.conf import settings

# Get database path
db_path = settings.DATABASES['default']['NAME']
print(f"Database path: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

# Connect to database directly
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Check all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()
print("\nAll tables in database:")
for table in tables:
    print(f"  - {table[0]}")

# Check migrations
cursor.execute("SELECT * FROM django_migrations;")
migrations = cursor.fetchall()
print("\nRecorded migrations:")
for mig in migrations:
    print(f"  - {mig}")

conn.close()

# Now check Django's perspective
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
executor = MigrationExecutor(connection)
print("\nDjango migration plan:")
print(f"  Graph: {executor.loader.graph.leaf_nodes()}")
