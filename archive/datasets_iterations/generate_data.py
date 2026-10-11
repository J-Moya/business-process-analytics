import pandas as pd
import numpy as np
from pathlib import Path

# Para obtener siempre los mismos resultados
np.random.seed(42)

# Cantidad de registros
n = 50000

# -----------------------------
# Datos disponibles
# -----------------------------

countries = [
    "Costa Rica",
    "United States",
    "Germany",
    "Mexico",
    "Brazil",
    "India",
    "Japan"
]

departments = [
    "Finance",
    "Regulatory",
    "Procurement",
    "Operations",
    "Commercial",
    "IT"
]

request_types = [
    "Master Data Update",
    "Access Request",
    "Regulatory Document",
    "Supplier Request",
    "System Issue",
    "Reporting Request"
]

priorities = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

# Equipo correcto según tipo de solicitud
team_mapping = {
    "Master Data Update": "Master Data",
    "Access Request": "IT Support",
    "Regulatory Document": "Regulatory Operations",
    "Supplier Request": "Procurement Operations",
    "System Issue": "IT Support",
    "Reporting Request": "Data & Analytics"
}

# SLA según prioridad
sla_mapping = {
    "Low": 72,
    "Medium": 48,
    "High": 24,
    "Critical": 8
}

# -----------------------------
# Generar datos
# -----------------------------

df = pd.DataFrame()

df["Request_ID"] = [
    f"REQ-{i:06d}"
    for i in range(1, n + 1)
]

df["Country"] = np.random.choice(
    countries,
    size=n
)

df["Requester_Department"] = np.random.choice(
    departments,
    size=n
)

df["Request_Type"] = np.random.choice(
    request_types,
    size=n
)

df["Priority"] = np.random.choice(
    priorities,
    size=n,
    p=[0.25, 0.45, 0.23, 0.07]
)

# -----------------------------
# Equipo correcto
# -----------------------------

df["Correct_Team"] = df["Request_Type"].map(
    team_mapping
)

df["Assigned_Team"] = df["Correct_Team"]

# Aproximadamente 12% de solicitudes mal asignadas
misassigned = np.random.random(n) < 0.12

all_teams = list(set(team_mapping.values()))

for index in df[misassigned].index:

    correct_team = df.loc[index, "Correct_Team"]

    incorrect_teams = [
        team
        for team in all_teams
        if team != correct_team
    ]

    df.loc[index, "Assigned_Team"] = np.random.choice(
        incorrect_teams
    )

df["Misassigned"] = (
    df["Assigned_Team"]
    != df["Correct_Team"]
)

# -----------------------------
# SLA
# -----------------------------

df["SLA_Hours"] = df["Priority"].map(
    sla_mapping
)

# Tiempo base de resolución
df["Resolution_Time_Hours"] = np.random.gamma(
    shape=2.5,
    scale=10,
    size=n
)

# Las solicitudes mal asignadas tardan más
df.loc[
    df["Misassigned"],
    "Resolution_Time_Hours"
] += np.random.uniform(
    12,
    30,
    df["Misassigned"].sum()
)

df["Resolution_Time_Hours"] = (
    df["Resolution_Time_Hours"]
    .round(2)
)

# -----------------------------
# SLA Breach
# -----------------------------

df["SLA_Breached"] = (
    df["Resolution_Time_Hours"]
    > df["SLA_Hours"]
)

# -----------------------------
# Data Quality
# -----------------------------

dq_errors = [
    "No Error",
    "Missing Required Field",
    "Invalid Country",
    "Duplicate Record",
    "Invalid Product Code"
]

df["Data_Quality_Error"] = np.random.choice(
    dq_errors,
    size=n,
    p=[0.86, 0.05, 0.03, 0.03, 0.03]
)

# -----------------------------
# Guardar archivo
# -----------------------------

project_folder = Path(__file__).resolve().parent.parent

output_file = (
    project_folder
    / "data"
    / "raw"
    / "business_requests.csv"
)

df.to_csv(
    output_file,
    index=False
)

# -----------------------------
# Mostrar resultados
# -----------------------------

print("Dataset created successfully!")
print()

print("Total records:")
print(len(df))

print()

print("Misassignment rate:")
print(df["Misassigned"].mean())

print()

print("SLA breach rate:")
print(df["SLA_Breached"].mean())

print()

print("First 5 rows:")
print(df.head())

print()

print("File saved at:")
print(output_file)