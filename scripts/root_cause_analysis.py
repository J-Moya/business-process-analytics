import pandas as pd
from pathlib import Path


# =========================================================
# FILE LOCATIONS
# =========================================================

project_folder = Path(__file__).resolve().parent.parent

input_file = (
    project_folder
    / "data"
    / "raw"
    / "business_requests_v21.csv"
)

output_file = (
    project_folder
    / "data"
    / "processed"
    / "business_requests_clean_v21.csv"
)


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    input_file,
    parse_dates=[
        "Created_Date",
        "Closed_Date"
    ]
)


# =========================================================
# BASIC KPIs
# =========================================================

print("\n=== BUSINESS KPIs ===")

print(f"Total Requests: {len(df):,}")

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


# =========================================================
# 1. MISASSIGNMENT ANALYSIS
# =========================================================

assignment_analysis = (
    df.groupby("Misassigned")
    .agg(
        Requests=("Request_ID", "count"),

        Avg_Resolution_Hours=(
            "Resolution_Time_Hours",
            "mean"
        ),

        SLA_Breach_Rate=(
            "SLA_Breached",
            "mean"
        )
    )
    .reset_index()
)

assignment_analysis["SLA_Breach_Rate"] *= 100


print("\n=== ASSIGNMENT ANALYSIS ===")

print(
    assignment_analysis.to_string(
        index=False
    )
)


# =========================================================
# 2. DATA QUALITY ANALYSIS
# =========================================================

dq_analysis = (
    df.groupby("Has_DQ_Error")
    .agg(
        Requests=("Request_ID", "count"),

        Avg_Resolution_Hours=(
            "Resolution_Time_Hours",
            "mean"
        ),

        SLA_Breach_Rate=(
            "SLA_Breached",
            "mean"
        )
    )
    .reset_index()
)

dq_analysis["SLA_Breach_Rate"] *= 100


print("\n=== DATA QUALITY ANALYSIS ===")

print(
    dq_analysis.to_string(
        index=False
    )
)


# =========================================================
# 3. REOPEN ANALYSIS
# =========================================================

reopen_analysis = (
    df.groupby("Reopened")
    .agg(
        Requests=("Request_ID", "count"),

        Avg_Resolution_Hours=(
            "Resolution_Time_Hours",
            "mean"
        ),

        SLA_Breach_Rate=(
            "SLA_Breached",
            "mean"
        )
    )
    .reset_index()
)

reopen_analysis["SLA_Breach_Rate"] *= 100


print("\n=== REOPEN ANALYSIS ===")

print(
    reopen_analysis.to_string(
        index=False
    )
)


# =========================================================
# 4. REQUEST TYPE ANALYSIS
# =========================================================

request_type_analysis = (
    df.groupby("Request_Type")
    .agg(
        Requests=("Request_ID", "count"),

        Avg_Resolution_Hours=(
            "Resolution_Time_Hours",
            "mean"
        ),

        SLA_Breach_Rate=(
            "SLA_Breached",
            "mean"
        ),

        Misassignment_Rate=(
            "Misassigned",
            "mean"
        )
    )
    .reset_index()
)

request_type_analysis["SLA_Breach_Rate"] *= 100
request_type_analysis["Misassignment_Rate"] *= 100

request_type_analysis = (
    request_type_analysis
    .sort_values(
        "SLA_Breach_Rate",
        ascending=False
    )
)


print("\n=== REQUEST TYPE ANALYSIS ===")

print(
    request_type_analysis.to_string(
        index=False
    )
)


# =========================================================
# 5. PRIORITY ANALYSIS
# =========================================================

priority_analysis = (
    df.groupby("Priority")
    .agg(
        Requests=("Request_ID", "count"),

        Avg_Resolution_Hours=(
            "Resolution_Time_Hours",
            "mean"
        ),

        SLA_Breach_Rate=(
            "SLA_Breached",
            "mean"
        )
    )
    .reset_index()
)

priority_analysis["SLA_Breach_Rate"] *= 100

priority_analysis = (
    priority_analysis
    .sort_values(
        "SLA_Breach_Rate",
        ascending=False
    )
)


print("\n=== PRIORITY ANALYSIS ===")

print(
    priority_analysis.to_string(
        index=False
    )
)


# =========================================================
# 6. BACKLOG AGING
# =========================================================

backlog = df[
    df["Status"] == "Open"
]

age_order = [
    "0-24 Hours",
    "24-48 Hours",
    "48-72 Hours",
    "3-7 Days",
    "7+ Days"
]

backlog_analysis = (
    backlog["Backlog_Age_Bucket"]
    .value_counts()
    .reindex(
        age_order,
        fill_value=0
    )
)


print("\n=== BACKLOG AGING ===")

print(backlog_analysis)


# =========================================================
# SAVE CLEAN DATASET
# =========================================================

df.to_csv(
    output_file,
    index=False
)


print("\nClean analytical dataset saved at:")

print(output_file)