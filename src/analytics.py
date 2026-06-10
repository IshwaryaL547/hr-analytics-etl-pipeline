"""
analytics.py

Generate business reports
from Gold Layer.
"""

import pandas as pd

from sqlalchemy import text

from src.db_connection import (
    get_session
)

from config.config import (
    Config
)

from src.logger import (
    logger
)


# =====================================================
# DEPARTMENT ATTENDANCE
# =====================================================

def generate_department_attendance_report():

    session = get_session()

    query = text("""

        SELECT

            d.department_id,
            d.department_name,

            COUNT(
                a.attendance_id
            ) AS total_attendance,

            ROUND(
                AVG(
                    a.hours_worked
                )::numeric,
                2
            ) AS avg_hours_worked

        FROM attendance_fact a

        JOIN department_dim d

            ON a.department_id =
               d.department_id

        GROUP BY

            d.department_id,
            d.department_name

        ORDER BY
            d.department_id

    """)

    engine = session.get_bind()

    df = pd.read_sql(
        query,
        engine
    )

    df.to_csv(
        Config.DEPARTMENT_ATTENDANCE_REPORT,
        index=False
    )

    session.close()


# =====================================================
# ABSENTEEISM REPORT
# =====================================================

def generate_absenteeism_report():

    session = get_session()

    query = text("""

        SELECT *

        FROM employee_metrics_agg

        ORDER BY
            absenteeism_rate DESC

    """)

    engine = session.get_bind()

    df = pd.read_sql(
        query,
        engine
    )

    df.to_csv(
        Config.ABSENTEEISM_REPORT,
        index=False
    )

    session.close()


# =====================================================
# ATTRITION REPORT
# =====================================================

def generate_attrition_report():

    session = get_session()

    query = text("""

        SELECT *

        FROM employee_metrics_agg

        WHERE attrition_risk = 'HIGH'

        ORDER BY
            absenteeism_rate DESC

    """)

    engine = session.get_bind()

    df = pd.read_sql(
        query,
        engine
    )

    df.to_csv(
        Config.ATTRITION_REPORT,
        index=False
    )

    session.close()


# =====================================================
# MONTHLY ATTENDANCE TREND
# =====================================================

def generate_monthly_attendance_report():

    session = get_session()

    query = text("""

        SELECT

            DATE_TRUNC(
                'month',
                attendance_date
            ) AS month,

            COUNT(*) AS attendance_count,

            ROUND(
                AVG(
                    hours_worked
                )::numeric,
                2
            ) AS avg_hours

        FROM attendance_fact

        GROUP BY month

        ORDER BY month

    """)

    engine = session.get_bind()

    df = pd.read_sql(
        query,
        engine
    )

    df.to_csv(
        Config.MONTHLY_ATTENDANCE_REPORT,
        index=False
    )

    session.close()


# =====================================================
# TENURE DISTRIBUTION
# =====================================================

def generate_tenure_report():

    session = get_session()

    query = text("""

        SELECT

            employee_id,
            department_id,
            tenure_days

        FROM employee_metrics_agg

        ORDER BY
            tenure_days DESC

    """)

    engine = session.get_bind()

    df = pd.read_sql(
        query,
        engine
    )

    df.to_csv(
        Config.TENURE_REPORT,
        index=False
    )

    session.close()


# =====================================================
# TURNOVER REPORT
# =====================================================

def generate_turnover_report():

    session = get_session()

    query = text("""

        SELECT

            department_id,

            COUNT(*) AS high_risk_employees

        FROM employee_metrics_agg

        WHERE attrition_risk = 'HIGH'

        GROUP BY department_id

        ORDER BY high_risk_employees DESC

    """)

    engine = session.get_bind()

    df = pd.read_sql(
        query,
        engine
    )

    df.to_csv(
        Config.TURNOVER_REPORT,
        index=False
    )

    session.close()


# =====================================================
# PRODUCTIVITY REPORT
# =====================================================

def generate_productivity_report():

    session = get_session()

    query = text("""

        SELECT

            employee_id,

            department_id,

            ROUND(
                AVG(
                    hours_worked
                )::numeric,
                2
            ) AS avg_hours_worked

        FROM attendance_fact

        GROUP BY

            employee_id,
            department_id

        ORDER BY
            avg_hours_worked DESC

    """)

    engine = session.get_bind()

    df = pd.read_sql(
        query,
        engine
    )

    df.to_csv(
        Config.PRODUCTIVITY_REPORT,
        index=False
    )

    session.close()


# =====================================================
# MASTER REPORT GENERATOR
# =====================================================

def generate_reports():

    logger.info(
        "Generating reports..."
    )

    generate_department_attendance_report()

    generate_absenteeism_report()

    generate_attrition_report()

    generate_monthly_attendance_report()

    generate_tenure_report()

    generate_turnover_report()

    generate_productivity_report()

    logger.info(
        "All reports generated."
    )