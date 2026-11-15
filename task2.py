from pathlib import Path
from typing import List, Dict, Optional
import csv
import json
import logging

from openpyxl import Workbook, load_workbook

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

CSV_FILE = Path("employees.csv")


def find_employee(name: str, employees: List[Dict]) -> Optional[Dict]:
    for employee in employees:
        if employee["name"].lower() == name.lower():
            return employee
    return None


def read_file(path: str):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        logger.error(f"File not found: {path}")

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON: {path}")

    return None


employees = []

with open(CSV_FILE, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        row["salary"] = int(row["salary"])
        employees.append(row)

print(f"Rows read: {len(employees)}")

with open("employees.json", "w", encoding="utf-8") as file:
    json.dump(employees, file, indent=4)

high_earners = [e for e in employees if e["salary"] > 50000]

with open("high_earners.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["name", "department", "salary"]
    )

    writer.writeheader()
    writer.writerows(high_earners)

print(f"High earners written: {len(high_earners)}")

wb = Workbook()
ws = wb.active

ws.append(["name", "department", "salary"])

for employee in employees:
    ws.append([
        employee["name"],
        employee["department"],
        employee["salary"]
    ])

wb.save("salary.xlsx")

wb2 = load_workbook("salary.xlsx")
ws2 = wb2.active

print(
    f"salary.xlsx created and read back: {ws2.max_row - 1} rows"
)

employee = find_employee("Rahul", employees)

print("Found Employee:", employee)

read_file("missing.txt")