# HR Analytics ETL Pipeline using Medallion Architecture

## Project Overview

This project implements an end-to-end HR Analytics ETL Pipeline using Medallion Architecture.

The pipeline ingests HR source CSV files, stores them in an AWS S3 Bronze Layer, validates and cleanses the data, loads trusted records into PostgreSQL Silver Layer, generates business metrics in PostgreSQL Gold Layer, and produces analytical reports and visualizations for business stakeholders.

The solution is designed to be:

* Re-runnable using UPSERT operations
* Scalable using Medallion Architecture
* Auditable through pipeline audit logging
* Extensible for future HR analytics requirements

---

# Business Scenario

A company wants to analyze workforce productivity, attendance, absenteeism, employee tenure, and attrition risk.

The HR department currently receives raw CSV files from multiple source systems and needs a reliable analytics platform.

This project provides:

* Data quality validation
* Historical auditability
* Employee performance insights
* Attrition risk monitoring
* Department-level workforce analytics

---

# Medallion Architecture

## Bronze Layer

Purpose:

Store raw source files exactly as received.

Technology:

* AWS S3

Files:

* departments.csv
* employees.csv
* attendance.csv

Characteristics:

* Immutable
* Raw data
* Supports reprocessing

---

## Silver Layer

Purpose:

Store validated and cleansed business data.

Technology:

* PostgreSQL
* SQLAlchemy ORM

Tables:

### DEPARTMENTS_SILVER

Primary Key:

* department_id

---

### EMPLOYEES_SILVER

Primary Key:

* employee_id

Foreign Key:

* department_id

---

### ATTENDANCE_SILVER

Primary Key:

* attendance_id

Foreign Key:

* employee_id

---

## Gold Layer

Purpose:

Store business-ready dimensions, facts, and aggregated metrics.

### DEPARTMENT_DIM

Primary Key:

* department_id

Columns:

* department_name
* employee_count

---

### EMPLOYEE_DIM

Primary Key:

* employee_id

Foreign Key:

* department_id

---

### ATTENDANCE_FACT

Primary Key:

* attendance_id

Foreign Keys:

* employee_id
* department_id

---

### EMPLOYEE_METRICS_AGG

Primary Key:

* employee_id

Foreign Keys:

* employee_id
* department_id

Stores:

* tenure_days
* absent_days
* absenteeism_rate
* attrition_risk
* last_updated

---

# Source Data

## departments.csv

Columns:

* department_id
* department_name

---

## employees.csv

Columns:

* employee_id
* employee_name
* department_id
* hire_date
* termination_date
* gender

---

## attendance.csv

Columns:

* attendance_id
* employee_id
* attendance_date
* hours_worked

---

# Data Quality Validation Rules

The validation layer performs the following checks:

### Departments

* Duplicate Department IDs
* Missing Department IDs

### Employees

* Duplicate Employee IDs
* Missing Employee IDs
* Missing Department IDs
* Invalid Dates
* Orphan Departments

### Attendance

* Duplicate Attendance IDs
* Missing Attendance IDs
* Invalid Attendance Dates
* Negative Hours Worked
* Orphan Employees

Invalid records are written to:

reports/invalid_records.csv

---

# Business Metrics

## Tenure Days

Formula:

termination_date - hire_date

OR

current_date - hire_date

for active employees.

---

## Absent Days

Business Rule:

hours_worked < 4

Attendance records with less than 4 working hours are considered absent days.

---

## Absenteeism Rate

Formula:

absent_days / total_working_days

---

## Attrition Risk

### HIGH

* tenure_days < 365

AND

* absenteeism_rate > 0.20

### MEDIUM

* absenteeism_rate > 0.10

### LOW

* Otherwise

---

# Audit Framework

The pipeline maintains execution audit records.

Audit Table:

AUDIT_RUN

Tracks:

* Records Processed
* Records Failed
* Execution Time
* Pipeline Status
* Error Messages
* Run Timestamp

Statuses:

* SUCCESS
* FAILED

---

# UPSERT Strategy

To support rerunnable pipelines:

All Silver and Gold layer loads use PostgreSQL UPSERT logic.

Benefits:

* No duplicate records
* Supports daily execution
* Handles late-arriving data
* Production-ready design

---

# Analytics Reports

The pipeline generates the following reports:

## Department Attendance Summary

Shows attendance trends by department.

Output:

department_attendance_report.csv

---

## Absenteeism Report

Shows absenteeism rate per employee.

Output:

absenteeism_report.csv

---

## Attrition Risk Report

Shows employees categorized by risk level.

Output:

attrition_report.csv

---

## Monthly Attendance Trend

Shows attendance volume by month.

Output:

monthly_attendance_report.csv

---

## Tenure Distribution Report

Shows employee tenure distribution.

Output:

tenure_distribution_report.csv

---

## Turnover Report

Shows departments with high attrition risk.

Output:

turnover_report.csv

---

## Productivity Report

Shows average employee working hours.

Output:

productivity_report.csv

---

# Visualizations

Charts generated automatically:

## employees_by_department.png

Shows employee count by department.

---

## absenteeism.png

Shows absenteeism rates by employee.

---

## attrition_risk.png

Shows high-risk employees by department.

---

## avg_hours_department.png

Shows average working hours by department.

---

## monthly_attendance.png

Shows attendance trends across months.

---

## turnover_risk.png

Shows departments with elevated attrition risk.

---

## productivity.png

Shows employee productivity based on average hours worked.

---

## department_kpi.png

Shows department-level absenteeism metrics.

---

## invalid_records_analysis.png

Shows distribution of data quality issues discovered during validation.

---

## data_quality_summary.png

Compares:

* Extracted Records
* Valid Records
* Invalid Records

for all datasets.

---

# Project Structure

HR_ANALYTICS_PROJECT/

config/

models/

src/

tests/

reports/

logs/

data/

requirements.txt

README.md

---

# Unit Testing

Implemented using Pytest.

Tests:

### test_tenure.py

Validates:

* Active employee tenure
* Terminated employee tenure

---

### test_absenteeism.py

Validates:

* Absenteeism calculation
* Zero-day scenarios

Run:

pytest tests/

---

# Technologies Used

Programming:

* Python

Database:

* PostgreSQL

ORM:

* SQLAlchemy

Cloud:

* AWS S3

Libraries:

* Pandas
* NumPy
* Matplotlib
* Psycopg2
* Boto3
* Pytest

---

# Running the Project

Create Tables:

python src/create_tables.py

Run Pipeline:

python src/main.py

Run Tests:

pytest tests/

---

# Team Responsibilities

Member 1

* AWS S3 Bronze Layer
* Extraction

Member 2

* Validation
* Data Quality Reporting

Member 3

* Transformations
* Business Metrics

Member 4

* Database Models
* Loading
* Audit Logging

Member 5

* Analytics
* Visualizations
* Documentation
* GitHub Management

---

# Key Learnings

* Medallion Architecture
* ETL Pipeline Design
* AWS S3 Integration
* PostgreSQL Data Warehousing
* SQLAlchemy ORM
* Data Quality Frameworks
* Audit Logging
* Business KPI Development
* Data Visualization
* Automated Reporting

---

# Future Enhancements

* Airflow Scheduling
* Incremental Loading
* Real-Time Streaming
* Power BI Dashboard
* AWS Glue Integration
* Snowflake Migration
* CI/CD Automation

---
