import pandas as pd
import sqlite3
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent

database_file = (
    project_folder
    / "sql"
    / "analytics.db"
)

sql_file = (
    project_folder
    / "sql"
    / "analysis_queries.sql"
)

# Leer el archivo SQL
with open(sql_file, "r", encoding="utf-8") as file:
    query = file.read()

# Conectarse a la base de datos
connection = sqlite3.connect(database_file)

# Ejecutar la consulta
result = pd.read_sql_query(
    query,
    connection
)

# Mostrar resultado
print("\n=== QUERY RESULT ===")

print(
    result.to_string(
        index=False
    )
)

connection.close()