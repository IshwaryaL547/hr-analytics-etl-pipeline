"""
employee_etl.py

Main ETL Controller Class
"""


class EmployeeETL:

    def __init__(self):

        # =====================================
        # RAW DATAFRAMES
        # =====================================

        self.departments_df = None

        self.employees_df = None

        self.attendance_df = None

        # =====================================
        # INVALID RECORDS
        # =====================================

        self.invalid_records = []

        # =====================================
        # SILVER OBJECTS
        # =====================================

        self.departments_silver = []

        self.employees_silver = []

        self.attendance_silver = []

        # =====================================
        # GOLD OBJECTS
        # =====================================

        self.department_dim = []

        self.employee_dim = []

        self.attendance_fact = []

        self.employee_metrics = []

        self.department_metrics = []

        # =====================================
        # AUDIT METRICS
        # =====================================

        self.audit_metrics = {

            "records_processed": 0,

            "records_failed": 0,

            "duplicate_rows": 0
        }

        # =====================================
        # EXTRACTION COUNTERS
        # =====================================

        self.total_departments_extracted = 0

        self.total_employees_extracted = 0

        self.total_attendance_extracted = 0