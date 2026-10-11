import pandas as pd
from pathlib import Path


# ----------------------------------------
# Ubicación del archivo
# ----------------------------------------

project_folder = Path(__file__).resolve().parent.parent

data_file = (
    project_folder
    / "data"
    / "raw"
    / "business_requests.csv"
)


# ----------------------------------------
# Cargar dataset
# ----------------------------------------

df = pd.read_csv(data_file)


# ----------------------------------------
# Información general
# ----------------------------------------

print("\n=== DATASET OVERVIEW ===")

print("\nNumber of rows:")
print(len(df))

print("\nNumber of columns:")
print(len(df.columns))


# ----------------------------------------
# Ver nombres de columnas
# ----------------------------------------

print("\n=== COLUMNS ===")

for column in df.columns:
    print(column)


# ----------------------------------------
# Tipos de datos
# ----------------------------------------

print("\n=== DATA TYPES ===")

print(df.dtypes)


# ----------------------------------------
# Valores faltantes
# ----------------------------------------

print("\n=== MISSING VALUES ===")

print(df.isnull().sum())


# ----------------------------------------
# Duplicados
# ----------------------------------------

print("\n=== DUPLICATE REQUEST IDs ===")

duplicates = df["Request_ID"].duplicated().sum()

print(duplicates)


# ----------------------------------------
# KPIs principales
# ----------------------------------------

print("\n=== BUSINESS KPIs ===")


total_requests = len(df)

misassignment_rate = df["Misassigned"].mean()

sla_breach_rate = df["SLA_Breached"].mean()

data_quality_rate = (
    df["Data_Quality_Error"] != "No Error"
).mean()

average_resolution_time = (
    df["Resolution_Time_Hours"].mean()
)


print(f"Total Requests: {total_requests:,}")

print(
    f"Misassignment Rate: "
    f"{misassignment_rate:.2%}"
)

print(
    f"SLA Breach Rate: "
    f"{sla_breach_rate:.2%}"
)

print(
    f"Data Quality Error Rate: "
    f"{data_quality_rate:.2%}"
)

print(
    f"Average Resolution Time: "
    f"{average_resolution_time:.2f} hours"
)