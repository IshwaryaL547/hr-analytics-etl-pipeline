"""
test_tenure.py
"""

from datetime import date

from src.enrich import (
    calculate_tenure_days
)


def test_active_employee_tenure():

    hire_date = date(
        2020,
        1,
        1
    )

    tenure = calculate_tenure_days(
        hire_date,
        None
    )

    assert tenure > 0


def test_terminated_employee_tenure():

    hire_date = date(
        2020,
        1,
        1
    )

    termination_date = date(
        2021,
        1,
        1
    )

    tenure = calculate_tenure_days(
        hire_date,
        termination_date
    )

    assert tenure == 366