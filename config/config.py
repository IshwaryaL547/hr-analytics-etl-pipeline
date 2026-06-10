"""
config.py

Centralized project configuration.
"""

from pathlib import Path
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()


class Config:

    # =====================================================
    # ROOT PATHS
    # =====================================================

    BASE_DIR = Path(__file__).resolve().parent.parent

    DATA_DIR = BASE_DIR / "data"

    REPORT_DIR = BASE_DIR / "reports"

    LOG_DIR = BASE_DIR / "logs"

    # =====================================================
    # SOURCE FILES
    # =====================================================

    DEPARTMENTS_FILE = (
        DATA_DIR / "departments.csv"
    )

    EMPLOYEES_FILE = (
        DATA_DIR / "employees.csv"
    )

    ATTENDANCE_FILE = (
        DATA_DIR / "attendance.csv"
    )

    # =====================================================
    # POSTGRESQL
    # =====================================================

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # =====================================================
    # AWS S3 BRONZE
    # =====================================================

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

    # =====================================================
    # PERFORMANCE
    # =====================================================

    CHUNK_SIZE = 1000

    # =====================================================
    # REPORTS
    # =====================================================

    INVALID_RECORDS_REPORT = (
        REPORT_DIR /
        "invalid_records.csv"
    )

    DEPARTMENT_ATTENDANCE_REPORT = (
        REPORT_DIR /
        "department_attendance_summary.csv"
    )

    ABSENTEEISM_REPORT = (
        REPORT_DIR /
        "absenteeism_report.csv"
    )

    ATTRITION_REPORT = (
        REPORT_DIR /
        "attrition_risk_report.csv"
    )

    MONTHLY_ATTENDANCE_REPORT = (
        REPORT_DIR /
        "monthly_attendance_trend.csv"
    )

    TENURE_REPORT = (
        REPORT_DIR /
        "tenure_distribution_report.csv"
    )

    TURNOVER_REPORT = (
        REPORT_DIR /
        "turnover_report.csv"
    )

    PRODUCTIVITY_REPORT = (
        REPORT_DIR /
        "productivity_report.csv"
    )

    CHARTS_DIR = (
            REPORT_DIR / "charts"
    )
