"""
validate.py

Data Quality Validation
"""

import pandas as pd

from config.config import Config

from src.logger import logger


def add_invalid_record(
        etl,
        record,
        reason
):

    record["error_reason"] = reason

    etl.invalid_records.append(
        record
    )

    etl.audit_metrics[
        "records_failed"
    ] += 1


# =====================================================
# DEPARTMENTS
# =====================================================

def validate_departments(etl):

    df = etl.departments_df.copy()

    # Missing Department ID

    missing_id = df[
        df["department_id"].isna()
    ]

    for _, row in missing_id.iterrows():

        add_invalid_record(
            etl,
            row.to_dict(),
            "Missing Department ID"
        )

    df = df[
        df["department_id"].notna()
    ]

    # Missing Department Name

    missing_name = df[
        df["department_name"].isna()
    ]

    for _, row in missing_name.iterrows():

        add_invalid_record(
            etl,
            row.to_dict(),
            "Missing Department Name"
        )

    df = df[
        df["department_name"].notna()
    ]

    # Duplicate Departments

    duplicate_mask = df.duplicated(
        subset=["department_id"]
    )

    duplicates = df[
        duplicate_mask
    ]

    for _, row in duplicates.iterrows():

        add_invalid_record(
            etl,
            row.to_dict(),
            "Duplicate Department"
        )

        etl.audit_metrics[
            "duplicate_rows"
        ] += 1

    df = df[
        ~duplicate_mask
    ]

    etl.departments_df = df


# =====================================================
# EMPLOYEES
# =====================================================

def validate_employees(etl):

    df = etl.employees_df.copy()

    # Missing Employee ID

    missing_id = df[
        df["employee_id"].isna()
    ]

    for _, row in missing_id.iterrows():

        add_invalid_record(
            etl,
            row.to_dict(),
            "Missing Employee ID"
        )

    df = df[
        df["employee_id"].notna()
    ]

    # Missing Employee Name

    missing_name = df[
        df["employee_name"].isna()
    ]

    for _, row in missing_name.iterrows():

        add_invalid_record(
            etl,
            row.to_dict(),
            "Missing Employee Name"
        )

    df = df[
        df["employee_name"].notna()
    ]

    # Invalid Hire Date

    invalid_dates = []

    for idx, value in df[
        "hire_date"
    ].items():

        try:

            pd.to_datetime(
                value
            )

        except Exception:

            invalid_dates.append(
                idx
            )

    for idx in invalid_dates:

        add_invalid_record(
            etl,
            df.loc[idx].to_dict(),
            "Invalid Hire Date"
        )

    df = df.drop(
        invalid_dates
    )

    # Duplicate Employees

    duplicate_mask = df.duplicated(
        subset=["employee_id"]
    )

    duplicates = df[
        duplicate_mask
    ]

    for _, row in duplicates.iterrows():

        add_invalid_record(
            etl,
            row.to_dict(),
            "Duplicate Employee"
        )

        etl.audit_metrics[
            "duplicate_rows"
        ] += 1

    df = df[
        ~duplicate_mask
    ]

    # Orphan Department

    valid_departments = set(
        etl.departments_df[
            "department_id"
        ]
    )

    orphan_mask = (
        ~df["department_id"]
        .isin(valid_departments)
    )

    orphans = df[
        orphan_mask
    ]

    for _, row in orphans.iterrows():

        add_invalid_record(
            etl,
            row.to_dict(),
            "Orphan Department"
        )

    df = df[
        ~orphan_mask
    ]

    etl.employees_df = df


# =====================================================
# ATTENDANCE
# =====================================================

def validate_attendance(etl):

    df = etl.attendance_df.copy()

    # Missing Attendance ID

    missing_id = df[
        df["attendance_id"].isna()
    ]

    for _, row in missing_id.iterrows():

        add_invalid_record(
            etl,
            row.to_dict(),
            "Missing Attendance ID"
        )

    df = df[
        df["attendance_id"].notna()
    ]

    # Duplicate Attendance

    duplicate_mask = df.duplicated(
        subset=["attendance_id"]
    )

    duplicates = df[
        duplicate_mask
    ]

    for _, row in duplicates.iterrows():

        add_invalid_record(
            etl,
            row.to_dict(),
            "Duplicate Attendance"
        )

        etl.audit_metrics[
            "duplicate_rows"
        ] += 1

    df = df[
        ~duplicate_mask
    ]

    # Orphan Employee

    valid_employees = set(
        etl.employees_df[
            "employee_id"
        ]
    )

    orphan_mask = (
        ~df["employee_id"]
        .isin(valid_employees)
    )

    orphans = df[
        orphan_mask
    ]

    for _, row in orphans.iterrows():

        add_invalid_record(
            etl,
            row.to_dict(),
            "Orphan Employee"
        )

    df = df[
        ~orphan_mask
    ]

    # Negative Hours

    negative_hours = df[
        df["hours_worked"] < 0
    ]

    for _, row in negative_hours.iterrows():

        add_invalid_record(
            etl,
            row.to_dict(),
            "Negative Hours Worked"
        )

    df = df[
        df["hours_worked"] >= 0
    ]

    # Invalid Attendance Date

    invalid_dates = []

    for idx, value in df[
        "attendance_date"
    ].items():

        try:

            pd.to_datetime(
                value
            )

        except Exception:

            invalid_dates.append(
                idx
            )

    for idx in invalid_dates:

        add_invalid_record(
            etl,
            df.loc[idx].to_dict(),
            "Invalid Attendance Date"
        )

    df = df.drop(
        invalid_dates
    )

    df["attendance_date"] = pd.to_datetime(
        df["attendance_date"]
    )

    etl.attendance_df = df


# =====================================================
# INVALID RECORD REPORT
# =====================================================

def save_invalid_records(etl):

    if not etl.invalid_records:
        return

    invalid_df = pd.DataFrame(
        etl.invalid_records
    )

    invalid_df.to_csv(
        Config.INVALID_RECORDS_REPORT,
        index=False
    )


# =====================================================
# MASTER VALIDATION
# =====================================================

def run_validation(etl):

    validate_departments(etl)

    validate_employees(etl)

    validate_attendance(etl)

    save_invalid_records(etl)

    logger.info(
        "Validation completed."
    )