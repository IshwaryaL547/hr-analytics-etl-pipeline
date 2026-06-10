"""
transform.py

Transform validated data
into SQLAlchemy objects.
"""

import pandas as pd

from models.hr_models import (
    DepartmentsSilver,
    EmployeesSilver,
    AttendanceSilver
)

from src.logger import logger


def transform_departments(etl):

    department_objects = []

    for _, row in (
        etl.departments_df.iterrows()
    ):

        department_objects.append(

            DepartmentsSilver(
                department_id=int(
                    row["department_id"]
                ),
                department_name=str(
                    row["department_name"]
                )
            )
        )

    etl.departments_silver = (
        department_objects
    )

    logger.info(
        f"Departments transformed: "
        f"{len(department_objects)}"
    )


def transform_employees(etl):

    employee_objects = []

    for _, row in (
        etl.employees_df.iterrows()
    ):

        hire_date = pd.to_datetime(
            row["hire_date"]
        ).date()

        termination_date = None

        if pd.notna(
            row["termination_date"]
        ):

            termination_date = (
                pd.to_datetime(
                    row["termination_date"]
                ).date()
            )

        employee_objects.append(

            EmployeesSilver(
                employee_id=int(
                    row["employee_id"]
                ),
                employee_name=str(
                    row["employee_name"]
                ),
                department_id=int(
                    row["department_id"]
                ),
                hire_date=hire_date,
                termination_date=(
                    termination_date
                ),
                gender=str(
                    row["gender"]
                )
            )
        )

    etl.employees_silver = (
        employee_objects
    )

    logger.info(
        f"Employees transformed: "
        f"{len(employee_objects)}"
    )


def transform_attendance(etl):

    attendance_objects = []

    for _, row in (
        etl.attendance_df.iterrows()
    ):

        attendance_objects.append(

            AttendanceSilver(
                attendance_id=int(
                    row["attendance_id"]
                ),
                employee_id=int(
                    row["employee_id"]
                ),
                attendance_date=(
                    pd.to_datetime(
                        row["attendance_date"]
                    )
                ),
                hours_worked=float(
                    row["hours_worked"]
                )
            )
        )

    etl.attendance_silver = (
        attendance_objects
    )

    logger.info(
        f"Attendance transformed: "
        f"{len(attendance_objects)}"
    )


def run_transform(etl):

    transform_departments(etl)

    transform_employees(etl)

    transform_attendance(etl)

    logger.info(
        "Transformation completed."
    )