import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(42)

# -----------------------------
# Departments
# -----------------------------
departments = []
for i in range(1, 21):
    departments.append({
        "department_id": i if random.random() > 0.02 else random.randint(1, 5),
        "department_name": fake.job().split()[0]  # simplified dept names
    })
departments_df = pd.DataFrame(departments)
departments_df.to_csv("departments.csv", index=False)

# -----------------------------
# Employees
# -----------------------------
employees = []
for i in range(1, 1101):
    hire_date = fake.date_between(start_date="-10y", end_date="today")
    termination_date = None
    if random.random() < 0.2:  # 20% terminated
        termination_date = hire_date + timedelta(days=random.randint(365, 365*5))
        if termination_date > datetime.today().date():
            termination_date = None
    employees.append({
        "employee_id": i if random.random() > 0.03 else random.randint(1, 50),
        "employee_name": fake.name(),
        "department_id": random.randint(1, 25),  # include orphan dept IDs
        "hire_date": hire_date,
        "termination_date": termination_date,
        "gender": random.choice(["M","F", None])
    })
employees_df = pd.DataFrame(employees)
employees_df.to_csv("employees.csv", index=False)

# -----------------------------
# Attendance
# -----------------------------
attendance = []
for i in range(1, 15001):
    employee_id = random.randint(1, 1200)  # include orphans
    date = datetime.today() - timedelta(days=random.randint(0, 365))
    hours_worked = random.randint(0, 10)
    if random.random() < 0.05:
        hours_worked = None  # missing hours
    attendance.append({
        "attendance_id": i if random.random() > 0.03 else random.randint(1, 200),
        "employee_id": employee_id,
        "attendance_date": date,
        "hours_worked": hours_worked
    })
attendance_df = pd.DataFrame(attendance)
attendance_df.to_csv("attendance.csv", index=False)

print("HR sample CSV files generated successfully!")