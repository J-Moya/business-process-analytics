import pandas as pd
import numpy as np
from pathlib import Path


# =========================================================
# CONFIGURATION
# =========================================================

RANDOM_SEED = 42
NUMBER_OF_RECORDS = 50000

rng = np.random.default_rng(RANDOM_SEED)

SNAPSHOT_DATE = pd.Timestamp("2026-10-01")
START_DATE = pd.Timestamp("2025-01-01")

project_folder = Path(__file__).resolve().parent.parent

output_file = (
    project_folder
    / "data"
    / "raw"
    / "business_requests_v2.csv"
)


# =========================================================
# MASTER DATA
# =========================================================

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

priority_probabilities = [
    0.25,
    0.45,
    0.23,
    0.07
]


# =========================================================
# TEAM MAPPING
# =========================================================

team_mapping = {
    "Master Data Update": "Master Data",
    "Access Request": "IT Support",
    "Regulatory Document": "Regulatory Operations",
    "Supplier Request": "Procurement Operations",
    "System Issue": "IT Support",
    "Reporting Request": "Data & Analytics"
}

teams = list(set(team_mapping.values()))


# =========================================================
# SLA MAPPING
# =========================================================

sla_mapping = {
    "Low": 72,
    "Medium": 48,
    "High": 24,
    "Critical": 8
}


# =========================================================
# REQUEST TYPE COMPLEXITY
# Base processing hours
# =========================================================

request_type_base_hours = {
    "Access Request": 12,
    "Reporting Request": 18,
    "Master Data Update": 22,
    "System Issue": 24,
    "Supplier Request": 28,
    "Regulatory Document": 34
}


# =========================================================
# PRIORITY EFFECT
# Higher priority = faster handling
# =========================================================

priority_factor = {
    "Low": 1.15,
    "Medium": 1.00,
    "High": 0.75,
    "Critical": 0.45
}


# =========================================================
# CREATE BASE DATAFRAME
# =========================================================

df = pd.DataFrame()

df["Request_ID"] = [
    f"REQ-{i:06d}"
    for i in range(1, NUMBER_OF_RECORDS + 1)
]


# =========================================================
# CREATED DATE
# =========================================================

total_hours = int(
    (SNAPSHOT_DATE - START_DATE).total_seconds()
    / 3600
)

random_hours = rng.integers(
    0,
    total_hours,
    NUMBER_OF_RECORDS
)

df["Created_Date"] = (
    START_DATE
    + pd.to_timedelta(
        random_hours,
        unit="h"
    )
)


# =========================================================
# BASIC ATTRIBUTES
# =========================================================

df["Country"] = rng.choice(
    countries,
    size=NUMBER_OF_RECORDS
)

df["Requester_Department"] = rng.choice(
    departments,
    size=NUMBER_OF_RECORDS
)

df["Request_Type"] = rng.choice(
    request_types,
    size=NUMBER_OF_RECORDS
)

df["Priority"] = rng.choice(
    priorities,
    size=NUMBER_OF_RECORDS,
    p=priority_probabilities
)


# =========================================================
# CORRECT TEAM
# =========================================================

df["Correct_Team"] = (
    df["Request_Type"]
    .map(team_mapping)
)

df["Assigned_Team"] = df["Correct_Team"]


# =========================================================
# MISASSIGNMENT
# =========================================================

misassignment_probability = np.full(
    NUMBER_OF_RECORDS,
    0.08
)

# Some request types are harder to route
misassignment_probability += np.where(
    df["Request_Type"] == "Supplier Request",
    0.08,
    0
)

misassignment_probability += np.where(
    df["Request_Type"] == "Regulatory Document",
    0.05,
    0
)

misassigned = (
    rng.random(NUMBER_OF_RECORDS)
    < misassignment_probability
)

for index in df[misassigned].index:

    correct_team = df.loc[
        index,
        "Correct_Team"
    ]

    possible_teams = [
        team
        for team in teams
        if team != correct_team
    ]

    df.loc[
        index,
        "Assigned_Team"
    ] = rng.choice(possible_teams)


df["Misassigned"] = (
    df["Assigned_Team"]
    != df["Correct_Team"]
)


# =========================================================
# DATA QUALITY
# =========================================================

dq_errors = [
    "No Error",
    "Missing Required Field",
    "Invalid Country",
    "Duplicate Record",
    "Invalid Product Code"
]

df["Data_Quality_Error"] = rng.choice(
    dq_errors,
    size=NUMBER_OF_RECORDS,
    p=[
        0.86,
        0.05,
        0.03,
        0.03,
        0.03
    ]
)

df["Has_DQ_Error"] = (
    df["Data_Quality_Error"]
    != "No Error"
)


# =========================================================
# REOPENED REQUEST
# =========================================================

df["Reopened"] = (
    rng.random(NUMBER_OF_RECORDS)
    < 0.06
)


# =========================================================
# SLA HOURS
# =========================================================

df["SLA_Hours"] = (
    df["Priority"]
    .map(sla_mapping)
)


# =========================================================
# BASE PROCESSING TIME
# =========================================================

base_hours = (
    df["Request_Type"]
    .map(request_type_base_hours)
    .astype(float)
)

priority_multiplier = (
    df["Priority"]
    .map(priority_factor)
)

resolution_hours = (
    base_hours
    * priority_multiplier
)


# Add normal operational variation
resolution_hours += rng.gamma(
    shape=2,
    scale=3,
    size=NUMBER_OF_RECORDS
)


# =========================================================
# MISASSIGNMENT PENALTY
# =========================================================

misassignment_penalty = np.where(
    df["Misassigned"],
    rng.uniform(
        12,
        30,
        NUMBER_OF_RECORDS
    ),
    0
)

resolution_hours += misassignment_penalty


# =========================================================
# DATA QUALITY PENALTY
# =========================================================

dq_penalty = np.where(
    df["Has_DQ_Error"],
    rng.uniform(
        6,
        18,
        NUMBER_OF_RECORDS
    ),
    0
)

resolution_hours += dq_penalty


# =========================================================
# REOPEN PENALTY
# =========================================================

reopen_penalty = np.where(
    df["Reopened"],
    rng.uniform(
        8,
        20,
        NUMBER_OF_RECORDS
    ),
    0
)

resolution_hours += reopen_penalty


resolution_hours = np.round(
    resolution_hours,
    2
)


# =========================================================
# CLOSED DATE / STATUS
# =========================================================

candidate_closed_date = (
    df["Created_Date"]
    + pd.to_timedelta(
        resolution_hours,
        unit="h"
    )
)

# Some requests remain open for operational reasons
randomly_closed = (
    rng.random(NUMBER_OF_RECORDS)
    < 0.92
)

closed_mask = (
    randomly_closed
    & (
        candidate_closed_date
        <= SNAPSHOT_DATE
    )
)

df["Status"] = np.where(
    closed_mask,
    "Closed",
    "Open"
)


df["Closed_Date"] = candidate_closed_date

df.loc[
    ~closed_mask,
    "Closed_Date"
] = pd.NaT


# =========================================================
# RESOLUTION TIME
# Only closed requests have final resolution time
# =========================================================

df["Resolution_Time_Hours"] = np.where(
    closed_mask,
    resolution_hours,
    np.nan
)


# =========================================================
# AGE OF OPEN REQUESTS
# =========================================================

df["Age_Hours"] = np.where(
    closed_mask,
    np.nan,
    (
        SNAPSHOT_DATE
        - df["Created_Date"]
    ).dt.total_seconds()
    / 3600
)

df["Age_Hours"] = (
    df["Age_Hours"]
    .round(2)
)


# =========================================================
# SLA BREACH
# =========================================================

elapsed_hours = np.where(
    closed_mask,
    resolution_hours,
    df["Age_Hours"]
)

df["SLA_Breached"] = (
    elapsed_hours
    > df["SLA_Hours"]
)


# =========================================================
# BACKLOG AGE BUCKET
# =========================================================

df["Backlog_Age_Bucket"] = "Closed"

open_mask = df["Status"] == "Open"

df.loc[
    open_mask & (df["Age_Hours"] <= 24),
    "Backlog_Age_Bucket"
] = "0-24 Hours"

df.loc[
    open_mask
    & (df["Age_Hours"] > 24)
    & (df["Age_Hours"] <= 48),
    "Backlog_Age_Bucket"
] = "24-48 Hours"

df.loc[
    open_mask
    & (df["Age_Hours"] > 48)
    & (df["Age_Hours"] <= 72),
    "Backlog_Age_Bucket"
] = "48-72 Hours"

df.loc[
    open_mask
    & (df["Age_Hours"] > 72)
    & (df["Age_Hours"] <= 168),
    "Backlog_Age_Bucket"
] = "3-7 Days"

df.loc[
    open_mask
    & (df["Age_Hours"] > 168),
    "Backlog_Age_Bucket"
] = "7+ Days"


# =========================================================
# SAVE FILE
# =========================================================

df.to_csv(
    output_file,
    index=False
)


# =========================================================
# SUMMARY
# =========================================================

print("\n=== DATASET V2 CREATED ===")

print(
    f"Total Requests: "
    f"{len(df):,}"
)

print(
    f"Misassignment Rate: "
    f"{df['Misassigned'].mean():.2%}"
)

print(
    f"Data Quality Error Rate: "
    f"{df['Has_DQ_Error'].mean():.2%}"
)

print(
    f"Reopen Rate: "
    f"{df['Reopened'].mean():.2%}"
)

print(
    f"SLA Breach Rate: "
    f"{df['SLA_Breached'].mean():.2%}"
)

print(
    f"Open Backlog: "
    f"{(df['Status'] == 'Open').sum():,}"
)

print(
    f"Closed Requests: "
    f"{(df['Status'] == 'Closed').sum():,}"
)

print("\nFile saved at:")
print(output_file)