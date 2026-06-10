"""
main.py

HR Analytics ETL Pipeline
"""

import time

from src.employee_etl import (
    EmployeeETL
)

from src.create_tables import (
    create_all_tables
)

from src.extract import (
    run_extraction
)

from src.validate import (
    run_validation
)

from src.transform import (
    run_transform
)

from src.enrich import (
    run_enrichment
)

from src.load import (
    run_load
)

from src.audit import (
    run_audit_success,
    run_audit_failure
)

from src.analytics import (
    generate_reports
)

from src.logger import (
    logger
)

from src.visualizations import (
    generate_all_charts
)
from src.invalid_records_visualization import (
    visualize_invalid_records,
    data_quality_summary

)

def main():

    start_time = time.time()

    etl = EmployeeETL()

    try:

        logger.info(
            "Pipeline Started"
        )

        create_all_tables()

        run_extraction(
            etl
        )

        run_validation(
            etl
        )

        run_transform(
            etl
        )

        run_enrichment(
            etl
        )

        run_load(
            etl
        )

        generate_reports()

        generate_all_charts()

        visualize_invalid_records()

        data_quality_summary()

        execution_time = (
            time.time()
            - start_time
        )

        run_audit_success(
            etl,
            execution_time
        )

        logger.info(
            "Pipeline Completed"
        )

    except Exception as error:

        execution_time = (
            time.time()
            - start_time
        )

        logger.error(
            f"Pipeline Failed: "
            f"{error}"
        )

        run_audit_failure(
            etl,
            execution_time,
            str(error)
        )

        raise


if __name__ == "__main__":

    main()