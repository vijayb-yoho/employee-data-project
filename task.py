from functools import wraps


# Function
def calculate_bonus(salary, rate=0.1, *extras, **options):
    bonus = salary * rate + sum(extras)

    if "cap" in options:
        bonus = min(bonus, options["cap"])

    return bonus


# Decorator
def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


# Base Class
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_details(self):
        return f"{self.name} - {self.salary}"

    @property
    def annual_salary(self):
        return self.salary * 12


# Derived Class
class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    @log_call
    def get_details(self):
        return f"{self.name} - {self.salary} - Team Size: {self.team_size}"


# Employee Data
employees = [
    ("Arun", 30000),
    ("Priya", 45000),
    ("Rahul", 60000),
    ("Divya", 75000),
    ("Karthik", 90000)
]

# Salary Categories
for name, salary in employees:
    if salary < 50000:
        category = "Low Salary"
    elif salary < 70000:
        category = "Medium Salary"
    else:
        category = "High Salary"

    print(f"{name} - {category}")

print()

# Bonus Example
bonus = calculate_bonus(60000, 0.1, 1000, 2000, cap=8000)
print("Bonus:", bonus)

print()

# Manager Example
manager = Manager("Divya", 75000, 5)
print(manager.get_details())

print()

# Annual Salary Example
print("Annual Salary:", manager.annual_salary)
