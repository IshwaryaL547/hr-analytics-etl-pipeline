"""
enrich.py

Business enrichment layer.
"""

from datetime import date
from datetime import datetime

from models.hr_models import (
    DepartmentDim,
    EmployeeDim,
    AttendanceFact,
    EmployeeMetricsAgg,
    DepartmentMetricsAgg
)

from src.logger import logger


# =====================================================
# BUSINESS FUNCTIONS
# =====================================================

def calculate_tenure_days(
        hire_date,
        termination_date
):

    end_date = (
        termination_date
        if termination_date
        else date.today()
    )

    return (
        end_date - hire_date
    ).days


def calculate_absenteeism_rate(
        absent_days,
        total_days
):

    if total_days == 0:

        return 0

    return (
        absent_days /
        total_days
    )


def determine_attrition_risk(
        tenure_days,
        absenteeism_rate
):

    if (
        tenure_days < 365
        and
        absenteeism_rate > 0.40
    ):

        return "HIGH"

    if absenteeism_rate > 0.30:

        return "MEDIUM"

    return "LOW"


# =====================================================
# GOLD LAYER CREATION
# =====================================================

def create_department_dim(etl):

    employee_counts = (
        etl.employees_df
        .groupby("department_id")
        .size()
        .to_dict()
    )

    department_dim = []

    for _, row in (
        etl.departments_df.iterrows()
    ):

        department_dim.append(

            DepartmentDim(
                department_id=int(
                    row["department_id"]
                ),
                department_name=str(
                    row["department_name"]
                ),
                employee_count=(
                    employee_counts.get(
                        row["department_id"],
                        0
                    )
                )
            )
        )

    etl.department_dim = (
        department_dim
    )


def create_employee_dim(etl):

    employee_dim = []

    for employee in (
        etl.employees_silver
    ):

        employee_dim.append(

            EmployeeDim(
                employee_id=(
                    employee.employee_id
                ),
                employee_name=(
                    employee.employee_name
                ),
                department_id=(
                    employee.department_id
                ),
                hire_date=(
                    employee.hire_date
                ),
                termination_date=(
                    employee.termination_date
                ),
                gender=employee.gender
            )
        )

    etl.employee_dim = (
        employee_dim
    )


def create_attendance_fact(etl):

    employee_department = {

        employee.employee_id:
        employee.department_id

        for employee in (
            etl.employees_silver
        )
    }

    attendance_fact = []

    for attendance in (
        etl.attendance_silver
    ):

        attendance_fact.append(

            AttendanceFact(
                attendance_id=(
                    attendance.attendance_id
                ),
                employee_id=(
                    attendance.employee_id
                ),
                department_id=(
                    employee_department[
                        attendance.employee_id
                    ]
                ),
                attendance_date=(
                    attendance.attendance_date
                ),
                hours_worked=(
                    attendance.hours_worked
                )
            )
        )

    etl.attendance_fact = (
        attendance_fact
    )


def create_employee_metrics(etl):

    metrics = []

    attendance_df = (
        etl.attendance_df
    )

    for employee in (
        etl.employees_silver
    ):

        emp_attendance = (
            attendance_df[
                attendance_df[
                    "employee_id"
                ] ==
                employee.employee_id
            ]
        )

        total_days = len(
            emp_attendance
        )

        absent_days = len(

            emp_attendance[
                emp_attendance[
                    "hours_worked"
                ] < 4
            ]
        )

        absenteeism_rate = (
            calculate_absenteeism_rate(
                absent_days,
                total_days
            )
        )

        tenure_days = (
            calculate_tenure_days(
                employee.hire_date,
                employee.termination_date
            )
        )

        attrition_risk = (
            determine_attrition_risk(
                tenure_days,
                absenteeism_rate
            )
        )

        metrics.append(

            EmployeeMetricsAgg(
                employee_id=(
                    employee.employee_id
                ),
                department_id=(
                    employee.department_id
                ),
                tenure_days=(
                    tenure_days
                ),
                absent_days=(
                    absent_days
                ),
                total_working_days=(
                    total_days
                ),
                absenteeism_rate=(
                    absenteeism_rate
                ),
                attrition_risk=(
                    attrition_risk
                ),
                last_updated=(
                    datetime.utcnow()
                )
            )
        )

    etl.employee_metrics = (
        metrics
    )


def create_department_metrics(etl):

    department_metrics = []

    metric_df = etl.employee_metrics

    departments = (
        etl.departments_df[
            "department_id"
        ].tolist()
    )

    for department_id in departments:

        rows = [

            row

            for row in metric_df

            if row.department_id
            == department_id
        ]

        if len(rows) == 0:

            continue

        avg_tenure = sum(
            r.tenure_days
            for r in rows
        ) / len(rows)

        avg_absenteeism = sum(
            r.absenteeism_rate
            for r in rows
        ) / len(rows)

        high_risk = len(

            [
                r
                for r in rows
                if r.attrition_risk
                == "HIGH"
            ]
        )

        department_metrics.append(

            DepartmentMetricsAgg(
                department_id=department_id,
                employee_count=len(rows),
                avg_tenure_days=avg_tenure,
                avg_absenteeism_rate=(
                    avg_absenteeism
                ),
                high_risk_count=(
                    high_risk
                ),
                last_updated=(
                    datetime.utcnow()
                )
            )
        )

    etl.department_metrics = (
        department_metrics
    )


def run_enrichment(etl):

    create_department_dim(etl)

    create_employee_dim(etl)

    create_attendance_fact(etl)

    create_employee_metrics(etl)

    create_department_metrics(etl)

    logger.info(
        "Enrichment completed."
    )