"""
test_absenteeism.py
"""

from src.enrich import (
    calculate_absenteeism_rate
)


def test_absenteeism_rate():

    absent_days = 10

    total_days = 100

    result = (
        calculate_absenteeism_rate(
            absent_days,
            total_days
        )
    )

    assert result == 0.10


def test_zero_days():

    result = (
        calculate_absenteeism_rate(
            5,
            0
        )
    )

    assert result == 0