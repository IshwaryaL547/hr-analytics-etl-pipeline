"""
load.py

Load Silver and Gold layers
using PostgreSQL batch UPSERTs.
"""

from sqlalchemy.dialects.postgresql import insert

from src.db_connection import (
    get_session
)

from src.logger import logger

from models.hr_models import (
    DepartmentsSilver,
    EmployeesSilver,
    AttendanceSilver,
    DepartmentDim,
    EmployeeDim,
    AttendanceFact,
    EmployeeMetricsAgg,
    DepartmentMetricsAgg
)


# =====================================================
# GENERIC BATCH UPSERT
# =====================================================

def batch_upsert(
        session,
        model,
        objects,
        primary_key
):
    """
    Batch UPSERT for PostgreSQL.
    """

    if not objects:
        return

    rows = []

    for obj in objects:

        rows.append({

            column.name:
            getattr(
                obj,
                column.name
            )

            for column
            in model.__table__.columns
        })

    stmt = insert(
        model
    ).values(
        rows
    )

    update_columns = {

        column.name:
        stmt.excluded[
            column.name
        ]

        for column
        in model.__table__.columns

        if column.name
        != primary_key
    }

    stmt = (
        stmt.on_conflict_do_update(
            index_elements=[
                primary_key
            ],
            set_=update_columns
        )
    )

    session.execute(
        stmt
    )


# =====================================================
# SILVER LAYER
# =====================================================

def load_departments_silver(
        session,
        etl
):

    batch_upsert(
        session,
        DepartmentsSilver,
        etl.departments_silver,
        "department_id"
    )


def load_employees_silver(
        session,
        etl
):

    batch_upsert(
        session,
        EmployeesSilver,
        etl.employees_silver,
        "employee_id"
    )


def load_attendance_silver(
        session,
        etl
):

    batch_upsert(
        session,
        AttendanceSilver,
        etl.attendance_silver,
        "attendance_id"
    )


def load_silver(etl):

    session = get_session()

    try:

        load_departments_silver(
            session,
            etl
        )

        load_employees_silver(
            session,
            etl
        )

        load_attendance_silver(
            session,
            etl
        )

        session.commit()

        logger.info(
            "Silver layer loaded successfully."
        )

    except Exception as error:

        session.rollback()

        logger.error(
            f"Silver load failed: "
            f"{error}"
        )

        raise

    finally:

        session.close()


# =====================================================
# GOLD LAYER
# =====================================================

def load_department_dim(
        session,
        etl
):

    batch_upsert(
        session,
        DepartmentDim,
        etl.department_dim,
        "department_id"
    )


def load_employee_dim(
        session,
        etl
):

    batch_upsert(
        session,
        EmployeeDim,
        etl.employee_dim,
        "employee_id"
    )


def load_attendance_fact(
        session,
        etl
):

    batch_upsert(
        session,
        AttendanceFact,
        etl.attendance_fact,
        "attendance_id"
    )


def load_employee_metrics(
        session,
        etl
):

    batch_upsert(
        session,
        EmployeeMetricsAgg,
        etl.employee_metrics,
        "employee_id"
    )


def load_department_metrics(
        session,
        etl
):

    batch_upsert(
        session,
        DepartmentMetricsAgg,
        etl.department_metrics,
        "department_id"
    )


def load_gold(etl):

    session = get_session()

    try:

        load_department_dim(
            session,
            etl
        )

        load_employee_dim(
            session,
            etl
        )

        load_attendance_fact(
            session,
            etl
        )

        load_employee_metrics(
            session,
            etl
        )

        load_department_metrics(
            session,
            etl
        )

        session.commit()

        logger.info(
            "Gold layer loaded successfully."
        )

    except Exception as error:

        session.rollback()

        logger.error(
            f"Gold load failed: "
            f"{error}"
        )

        raise

    finally:

        session.close()


# =====================================================
# MASTER LOAD
# =====================================================

def run_load(etl):

    load_silver(
        etl
    )

    load_gold(
        etl
    )

    logger.info(
        "Load phase completed."
    )