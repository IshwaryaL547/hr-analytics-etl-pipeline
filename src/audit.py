"""
audit.py

Pipeline auditing.
"""

from models.hr_models import (
    AuditRun
)

from src.db_connection import (
    get_session
)

from src.logger import (
    logger
)


def create_audit_record(
        pipeline_step,
        records_processed,
        records_failed,
        run_status,
        execution_time,
        error_message=None
):
    """
    Create audit record.
    """

    session = get_session()

    try:

        audit_record = AuditRun(

            pipeline_step=(
                pipeline_step
            ),

            records_processed=(
                records_processed
            ),

            records_failed=(
                records_failed
            ),

            run_status=(
                run_status
            ),

            execution_time_seconds=(
                execution_time
            ),

            error_message=(
                error_message
            )
        )

        session.add(
            audit_record
        )

        session.commit()

        logger.info(
            f"Audit record inserted: "
            f"{run_status}"
        )

    except Exception as error:

        logger.error(
            f"Audit insert failed: "
            f"{error}"
        )

    finally:

        session.close()


def run_audit_success(
        etl,
        execution_time
):
    """
    Log successful pipeline run.
    """

    total_processed = (

        etl.total_departments_extracted +

        etl.total_employees_extracted +

        etl.total_attendance_extracted
    )

    total_failed = (
        etl.audit_metrics[
            "records_failed"
        ]
    )

    create_audit_record(

        pipeline_step=(
            "FULL_ETL_RUN"
        ),

        records_processed=(
            total_processed
        ),

        records_failed=(
            total_failed
        ),

        run_status="SUCCESS",

        execution_time=(
            execution_time
        )
    )


def run_audit_failure(
        etl,
        execution_time,
        error_message
):
    """
    Log failed pipeline run.
    """

    total_processed = (

        etl.total_departments_extracted +

        etl.total_employees_extracted +

        etl.total_attendance_extracted
    )

    total_failed = (
        etl.audit_metrics[
            "records_failed"
        ]
    )

    create_audit_record(

        pipeline_step=(
            "FULL_ETL_RUN"
        ),

        records_processed=(
            total_processed
        ),

        records_failed=(
            total_failed
        ),

        run_status="FAILED",

        execution_time=(
            execution_time
        ),

        error_message=(
            error_message
        )
    )