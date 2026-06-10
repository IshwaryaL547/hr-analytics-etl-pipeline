"""
hr_models.py

SQLAlchemy ORM Models

Silver Layer
Gold Layer
Audit Layer
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    Index
)

from sqlalchemy.orm import (
    declarative_base,
    relationship
)

Base = declarative_base()

# =====================================================
# SILVER LAYER
# =====================================================


class DepartmentsSilver(Base):

    __tablename__ = "departments_silver"

    department_id = Column(
        Integer,
        primary_key=True
    )

    department_name = Column(
        String(255),
        nullable=False
    )

    employees = relationship(
        "EmployeesSilver",
        back_populates="department"
    )


class EmployeesSilver(Base):

    __tablename__ = "employees_silver"

    employee_id = Column(
        Integer,
        primary_key=True
    )

    employee_name = Column(
        String(255),
        nullable=False
    )

    department_id = Column(
        Integer,
        ForeignKey(
            "departments_silver.department_id"
        ),
        nullable=False
    )

    hire_date = Column(
        Date,
        nullable=False
    )

    termination_date = Column(
        Date,
        nullable=True
    )

    gender = Column(
        String(20),
        nullable=True
    )

    department = relationship(
        "DepartmentsSilver",
        back_populates="employees"
    )

    attendance = relationship(
        "AttendanceSilver",
        back_populates="employee"
    )

    __table_args__ = (
        Index(
            "idx_emp_silver_dept",
            "department_id"
        ),
    )


class AttendanceSilver(Base):

    __tablename__ = "attendance_silver"

    attendance_id = Column(
        Integer,
        primary_key=True
    )

    employee_id = Column(
        Integer,
        ForeignKey(
            "employees_silver.employee_id"
        ),
        nullable=False
    )

    attendance_date = Column(
        DateTime,
        nullable=False
    )

    hours_worked = Column(
        Float,
        nullable=False
    )

    employee = relationship(
        "EmployeesSilver",
        back_populates="attendance"
    )

    __table_args__ = (
        Index(
            "idx_att_silver_emp",
            "employee_id"
        ),
        Index(
            "idx_att_silver_date",
            "attendance_date"
        )
    )


# =====================================================
# GOLD LAYER
# =====================================================


class DepartmentDim(Base):

    __tablename__ = "department_dim"

    department_id = Column(
        Integer,
        primary_key=True
    )

    department_name = Column(
        String(255),
        nullable=False
    )

    employee_count = Column(
        Integer,
        nullable=False
    )


class EmployeeDim(Base):

    __tablename__ = "employee_dim"

    employee_id = Column(
        Integer,
        primary_key=True
    )

    employee_name = Column(
        String(255),
        nullable=False
    )

    department_id = Column(
        Integer,
        ForeignKey(
            "department_dim.department_id"
        ),
        nullable=False
    )

    hire_date = Column(
        Date,
        nullable=False
    )

    termination_date = Column(
        Date,
        nullable=True
    )

    gender = Column(
        String(20)
    )

    __table_args__ = (
        Index(
            "idx_emp_dim_dept",
            "department_id"
        ),
    )


class AttendanceFact(Base):

    __tablename__ = "attendance_fact"

    attendance_id = Column(
        Integer,
        primary_key=True
    )

    employee_id = Column(
        Integer,
        ForeignKey(
            "employee_dim.employee_id"
        ),
        nullable=False
    )

    department_id = Column(
        Integer,
        ForeignKey(
            "department_dim.department_id"
        ),
        nullable=False
    )

    attendance_date = Column(
        DateTime,
        nullable=False
    )

    hours_worked = Column(
        Float,
        nullable=False
    )

    __table_args__ = (
        Index(
            "idx_fact_emp",
            "employee_id"
        ),
        Index(
            "idx_fact_dept",
            "department_id"
        ),
        Index(
            "idx_fact_date",
            "attendance_date"
        )
    )


class EmployeeMetricsAgg(Base):

    __tablename__ = "employee_metrics_agg"

    employee_id = Column(
        Integer,
        ForeignKey(
            "employee_dim.employee_id"
        ),
        primary_key=True
    )

    department_id = Column(
        Integer,
        ForeignKey(
            "department_dim.department_id"
        ),
        nullable=False
    )

    tenure_days = Column(
        Integer,
        nullable=False
    )

    absent_days = Column(
        Integer,
        nullable=False
    )

    total_working_days = Column(
        Integer,
        nullable=False
    )

    absenteeism_rate = Column(
        Float,
        nullable=False
    )

    attrition_risk = Column(
        String(20),
        nullable=False
    )

    last_updated = Column(
        DateTime,
        default=datetime.utcnow
    )


class DepartmentMetricsAgg(Base):

    __tablename__ = "department_metrics_agg"

    department_id = Column(
        Integer,
        ForeignKey(
            "department_dim.department_id"
        ),
        primary_key=True
    )

    employee_count = Column(
        Integer,
        nullable=False
    )

    avg_tenure_days = Column(
        Float,
        nullable=False
    )

    avg_absenteeism_rate = Column(
        Float,
        nullable=False
    )

    high_risk_count = Column(
        Integer,
        nullable=False
    )

    last_updated = Column(
        DateTime,
        default=datetime.utcnow
    )


# =====================================================
# AUDIT TABLE
# =====================================================


class AuditRun(Base):

    __tablename__ = "audit_run"

    run_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    pipeline_step = Column(
        String(100),
        nullable=False
    )

    records_processed = Column(
        Integer,
        nullable=False
    )

    records_failed = Column(
        Integer,
        nullable=False
    )

    run_status = Column(
        String(20),
        nullable=False
    )

    execution_time_seconds = Column(
        Float,
        nullable=False
    )

    error_message = Column(
        String(1000),
        nullable=True
    )

    run_timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )