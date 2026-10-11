import pandas as pd
from pathlib import Path


# ----------------------------------------
# File locations
# ----------------------------------------

project_folder = Path(__file__).resolve().parent.parent

input_file = (
    project_folder
    / "data"
    / "raw"
    / "business_requests.csv"
)

output_folder = (
    project_folder
    / "data"
    / "processed"
)


# ----------------------------------------
# Load data
# ----------------------------------------

df = pd.read_csv(input_file)


# ----------------------------------------
# Create analytical variables
# ----------------------------------------

df["Has_DQ_Error"] = (
    df["Data_Quality_Error"] != "No Error"
)


# ========================================
# 1. MISASSIGNMENT ANALYSIS
# ========================================

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


# ========================================
# 2. REQUEST TYPE ANALYSIS
# ========================================

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

request_type_analysis[
    "SLA_Breach_Rate"
] *= 100

request_type_analysis[
    "Misassignment_Rate"
] *= 100


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


# ========================================
# 3. COUNTRY ANALYSIS
# ========================================

country_analysis = (
    df.groupby("Country")
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

country_analysis[
    "SLA_Breach_Rate"
] *= 100

country_analysis = (
    country_analysis
    .sort_values(
        "SLA_Breach_Rate",
        ascending=False
    )
)


print("\n=== COUNTRY ANALYSIS ===")

print(
    country_analysis.to_string(
        index=False
    )
)


# ========================================
# 4. PRIORITY ANALYSIS
# ========================================

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

priority_analysis[
    "SLA_Breach_Rate"
] *= 100

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


# ========================================
# 5. DATA QUALITY ANALYSIS
# ========================================

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

dq_analysis[
    "SLA_Breach_Rate"
] *= 100


print("\n=== DATA QUALITY ANALYSIS ===")

print(
    dq_analysis.to_string(
        index=False
    )
)


# ========================================
# SAVE RESULTS
# ========================================

output_folder.mkdir(
    parents=True,
    exist_ok=True
)

assignment_analysis.to_csv(
    output_folder / "assignment_analysis.csv",
    index=False
)

request_type_analysis.to_csv(
    output_folder / "request_type_analysis.csv",
    index=False
)

country_analysis.to_csv(
    output_folder / "country_analysis.csv",
    index=False
)

priority_analysis.to_csv(
    output_folder / "priority_analysis.csv",
    index=False
)

dq_analysis.to_csv(
    output_folder / "data_quality_analysis.csv",
    index=False
)

df.to_csv(
    output_folder / "business_requests_clean.csv",
    index=False
)


print("\nAnalysis files successfully saved.")