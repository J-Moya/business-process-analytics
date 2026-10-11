import pandas as pd
import sqlite3
from pathlib import Path


# =========================================================
# FILE LOCATIONS
# =========================================================

project_folder = Path(__file__).resolve().parent.parent

csv_file = (
    project_folder
    / "data"
    / "processed"
    / "business_requests_clean_v21.csv"
)

database_file = (
    project_folder
    / "sql"
    / "analytics.db"
)


# =========================================================
# LOAD CSV
# =========================================================

df = pd.read_csv(csv_file)

print("\nCSV loaded successfully.")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")


# =========================================================
# CONNECT TO SQLITE
# =========================================================

connection = sqlite3.connect(database_file)


# =========================================================
# LOAD DATA INTO DATABASE
# =========================================================

df.to_sql(
    "business_requests",
    connection,
    if_exists="replace",
    index=False
)


# =========================================================
# VALIDATION
# =========================================================

query = """
SELECT COUNT(*) AS total_rows
FROM business_requests;
"""

result = pd.read_sql_query(
    query,
    connection
)

print("\nRows loaded into SQLite:")

print(result)


# =========================================================
# CLOSE CONNECTION
# =========================================================

connection.close()

print("\nDatabase created successfully:")
print(database_file)