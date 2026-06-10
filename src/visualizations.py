"""
visualizations.py

Generate business charts
for HR Analytics reporting.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sqlalchemy import text

from config.config import Config

from src.db_connection import (
    get_session
)

from src.logger import logger

import warnings

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="Using categorical units*"
)
# =====================================================
# CHART DIRECTORY
# =====================================================

Config.CHARTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def save_chart():

    plt.tight_layout()

    plt.grid(
        axis="y",
        alpha=0.3
    )


# =====================================================
# QUERY 1
# EMPLOYEES BY DEPARTMENT
# =====================================================

def employees_by_department_chart():

    session = get_session()

    query = text("""

        SELECT
            department_name,
            employee_count

        FROM department_dim

        ORDER BY employee_count DESC

    """)

    df = pd.read_sql(
        query,
        session.get_bind()
    )

    plt.figure(
        figsize=(10, 6)
    )

    x = range(len(df))

    bars = plt.bar(
        x,
        df["employee_count"]
    )

    plt.xticks(
        x,
        df["department_name"],
        rotation=45
    )

    for bar in bars:
        plt.text(

            bar.get_x()
            + bar.get_width() / 2,

            bar.get_height(),

            f"{int(bar.get_height())}",

            ha="center",

            va="bottom",

            fontsize=8
        )

    plt.title(
        "Employees By Department"
    )

    plt.xlabel(
        "Department"
    )

    plt.ylabel(
        "Employee Count"
    )

    plt.xticks(
        rotation=45
    )

    save_chart()

    plt.savefig(
        Config.CHARTS_DIR /
        "employees_by_department.png"
    )

    plt.close()

    session.close()


# =====================================================
# QUERY 2
# TOP ABSENTEEISM
# =====================================================

def absenteeism_chart():

    session = get_session()

    query = text("""

        SELECT

            employee_id,
            absenteeism_rate

        FROM employee_metrics_agg

        ORDER BY absenteeism_rate DESC

        LIMIT 10

    """)

    df = pd.read_sql(
        query,
        session.get_bind()
    )

    plt.figure(
        figsize=(10, 6)
    )

    x = range(len(df))

    bars = plt.bar(
        x,
        df["absenteeism_rate"]
    )

    plt.xticks(
        x,
        df["employee_id"],
        rotation=45
    )

    for bar in bars:
        plt.text(

            bar.get_x()
            + bar.get_width() / 2,

            bar.get_height(),

            f"{bar.get_height():.2f}",

            ha="center",

            va="bottom",

            fontsize=8
        )

    plt.title(
        "Top 10 Employees By Absenteeism"
    )

    plt.xlabel(
        "Employee ID"
    )

    plt.ylabel(
        "Absenteeism Rate"
    )

    save_chart()

    plt.savefig(
        Config.CHARTS_DIR /
        "absenteeism.png"
    )

    plt.close()

    session.close()


# =====================================================
# QUERY 3
# HIGH ATTRITION RISK
# =====================================================

def attrition_risk_chart():

    session = get_session()

    query = text("""

        SELECT

            d.department_id,

            COALESCE(
                COUNT(
                    CASE
                        WHEN e.attrition_risk = 'HIGH'
                        THEN 1
                    END
                ),
                0
            ) AS employees

        FROM department_dim d

        LEFT JOIN employee_metrics_agg e

            ON d.department_id =
               e.department_id

        GROUP BY d.department_id

        ORDER BY d.department_id

    """)

    df = pd.read_sql(
        query,
        session.get_bind()
    )

    plt.figure(
        figsize=(12, 6)
    )

    x = range(len(df))

    bars = plt.bar(
        x,
        df["employees"]
    )

    plt.xticks(
        x,
        df["department_id"]
    )

    for bar in bars:

        plt.text(

            bar.get_x()
            + bar.get_width() / 2,

            bar.get_height(),

            f"{int(bar.get_height())}",

            ha="center",

            va="bottom",

            fontsize=8,

            fontweight="bold"
        )

    plt.title(
        "High Attrition Risk By Department"
    )

    plt.xlabel(
        "Department ID"
    )

    plt.ylabel(
        "High Risk Employees"
    )

    save_chart()

    plt.savefig(

        Config.CHARTS_DIR /

        "high_attrition_risk.png",

        dpi=300,

        bbox_inches="tight"
    )

    plt.close()

    session.close()

# =====================================================
# QUERY 4
# AVG HOURS BY DEPARTMENT
# =====================================================

def avg_hours_department_chart():

    session = get_session()

    query = text("""

        SELECT

            d.department_name,

            ROUND(
                AVG(a.hours_worked)::numeric,
                2
            ) avg_hours

        FROM attendance_fact a

        JOIN department_dim d

            ON a.department_id =
               d.department_id

        GROUP BY d.department_name

        ORDER BY avg_hours DESC

    """)

    df = pd.read_sql(
        query,
        session.get_bind()
    )

    plt.figure(
        figsize=(10, 6)
    )

    x = range(len(df))

    bars = plt.bar(
        x,
        df["avg_hours"]
    )

    plt.xticks(
        x,
        df["department_name"],
        rotation=45
    )

    for bar in bars:
        plt.text(

            bar.get_x()
            + bar.get_width() / 2,

            bar.get_height(),

            f"{bar.get_height():.2f}",

            ha="center",

            va="bottom",

            fontsize=8
        )

    plt.title(
        "Average Hours Worked By Department"
    )

    plt.xlabel(
        "Department"
    )

    plt.ylabel(
        "Average Hours"
    )

    plt.xticks(
        rotation=45
    )

    save_chart()

    plt.savefig(
        Config.CHARTS_DIR /
        "avg_hours_department.png"
    )

    plt.close()

    session.close()


# =====================================================
# QUERY 5
# MONTHLY ATTENDANCE TREND
# =====================================================

def monthly_attendance_chart():

    session = get_session()

    query = text("""

        SELECT

            DATE_TRUNC(
                'month',
                attendance_date
            ) AS month,

            COUNT(*) AS attendance_count

        FROM attendance_fact

        GROUP BY month

        ORDER BY month

    """)

    df = pd.read_sql(
        query,
        session.get_bind()
    )

    plt.figure(
        figsize=(12, 6)
    )

    df["month"] = pd.to_datetime(
        df["month"]
    )

    labels = df["month"].dt.strftime(
        "%Y-%m"
    )

    x = range(
        len(df)
    )

    bars = plt.bar(
        x,
        df["attendance_count"]
    )

    plt.xticks(
        x,
        labels,
        rotation=45
    )

    # =====================================
    # ADD VALUES ON TOP OF BARS
    # =====================================

    for bar in bars:

        plt.text(

            bar.get_x()
            + bar.get_width() / 2,

            bar.get_height(),

            f"{int(bar.get_height()):,}",

            ha="center",

            va="bottom",

            fontsize=8,

            fontweight="bold"
        )

    plt.title(
        "Monthly Attendance Trend"
    )

    plt.xlabel(
        "Month"
    )

    plt.ylabel(
        "Attendance Count"
    )

    save_chart()

    plt.savefig(

        Config.CHARTS_DIR /

        "monthly_attendance.png",

        dpi=300,

        bbox_inches="tight"
    )

    plt.close()

    session.close()

# =====================================================
# QUERY 6
# TURNOVER BY DEPARTMENT
# =====================================================

def turnover_chart():

    session = get_session()

    query = text("""

        SELECT

            d.department_id,

            COALESCE(
                COUNT(
                    CASE
                        WHEN e.attrition_risk = 'HIGH'
                        THEN 1
                    END
                ),
                0
            ) AS risk_count

        FROM department_dim d

        LEFT JOIN employee_metrics_agg e

            ON d.department_id =
               e.department_id

        GROUP BY d.department_id

        ORDER BY d.department_id

    """)

    df = pd.read_sql(
        query,
        session.get_bind()
    )

    plt.figure(
        figsize=(12, 6)
    )

    x = range(len(df))

    bars = plt.bar(
        x,
        df["risk_count"]
    )

    plt.xticks(
        x,
        df["department_id"]
    )

    for bar in bars:

        plt.text(

            bar.get_x()
            + bar.get_width() / 2,

            bar.get_height(),

            f"{int(bar.get_height())}",

            ha="center",

            va="bottom",

            fontsize=8,

            fontweight="bold"
        )

    plt.title(
        "Turnover Risk By Department"
    )

    plt.xlabel(
        "Department ID"
    )

    plt.ylabel(
        "High Risk Employee Count"
    )

    save_chart()

    plt.savefig(

        Config.CHARTS_DIR /

        "turnover_risk.png",

        dpi=300,

        bbox_inches="tight"
    )

    plt.close()

    session.close()

# =====================================================
# QUERY 7
# TOP PRODUCTIVE EMPLOYEES
# =====================================================

def productivity_chart():

    session = get_session()

    query = text("""

        SELECT

            employee_id,

            ROUND(
                AVG(hours_worked)::numeric,
                2
            ) avg_hours

        FROM attendance_fact

        GROUP BY employee_id

        ORDER BY avg_hours DESC

        LIMIT 10

    """)

    df = pd.read_sql(
        query,
        session.get_bind()
    )

    plt.figure(
        figsize=(10, 6)
    )

    x = range(len(df))

    bars = plt.bar(
        x,
        df["avg_hours"]
    )

    plt.xticks(
        x,
        df["employee_id"],
        rotation=45
    )

    for bar in bars:
        plt.text(

            bar.get_x()
            + bar.get_width() / 2,

            bar.get_height(),

            f"{bar.get_height():.2f}",

            ha="center",

            va="bottom",

            fontsize=8,

            fontweight="bold"
        )

    plt.title(
        "Top Productive Employees"
    )

    plt.xlabel(
        "Employee ID"
    )

    plt.ylabel(
        "Average Hours"
    )

    save_chart()

    plt.savefig(
        Config.CHARTS_DIR /
        "productivity.png"
    )

    plt.close()

    session.close()


# =====================================================
# QUERY 8
# DEPARTMENT KPI SUMMARY
# =====================================================

def department_kpi_chart():

    session = get_session()

    query = text("""

        SELECT

            department_id,

            avg_absenteeism_rate

        FROM department_metrics_agg

        ORDER BY department_id

    """)

    df = pd.read_sql(
        query,
        session.get_bind()
    )

    plt.figure(
        figsize=(10, 6)
    )

    x = range(len(df))

    bars = plt.bar(
        x,
        df["avg_absenteeism_rate"]
    )

    plt.xticks(
        x,
        df["department_id"]
    )

    for bar in bars:
        plt.text(

            bar.get_x()
            + bar.get_width() / 2,

            bar.get_height(),

            f"{bar.get_height():.2f}",

            ha="center",

            va="bottom",

            fontsize=8
        )

    plt.title(
        "Department KPI Summary"
    )

    plt.xlabel(
        "Department"
    )

    plt.ylabel(
        "Avg Absenteeism Rate"
    )

    save_chart()

    plt.savefig(
        Config.CHARTS_DIR /
        "department_kpi.png"
    )

    plt.close()

    session.close()


# =====================================================
# MASTER
# =====================================================

def generate_all_charts():

    logger.info(
        "Generating charts..."
    )

    employees_by_department_chart()

    absenteeism_chart()

    attrition_risk_chart()

    avg_hours_department_chart()

    monthly_attendance_chart()

    turnover_chart()

    productivity_chart()

    department_kpi_chart()

    logger.info(
        "All charts generated."
    )