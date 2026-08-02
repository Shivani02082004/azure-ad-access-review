"""
Generates a mock Azure AD-style user access CSV for the access review tool.
Run this first to create users.csv, then run access_review.py on it.
"""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

roles = ["Standard User", "Helpdesk Operator", "Global Admin", "User Admin",
         "Security Reader", "Application Admin", "Billing Admin"]

departments = ["Claims", "Underwriting", "IT", "Finance", "HR", "Customer Service"]

names = ["Aarav Shah", "Priya Nair", "Rohan Mehta", "Ananya Iyer", "Karan Verma",
         "Sneha Rao", "Vikram Joshi", "Divya Pillai", "Arjun Kapoor", "Meera Menon",
         "Sai Reddy", "Nikhil Desai", "Pooja Bhatt", "Rahul Malhotra", "Ishita Sen",
         "Aditya Kulkarni", "Kavya Pandey", "Varun Chopra", "Riya Sharma", "Manav Gupta"]

today = datetime.now()

with open("users.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["user_id", "full_name", "department", "role",
                      "last_login_date", "account_created_date", "mfa_enabled"])

    for i, name in enumerate(names, start=1):
        role = random.choice(roles)
        dept = random.choice(departments)
        # Make some accounts deliberately stale / risky for the tool to catch
        days_since_login = random.choice([2, 5, 10, 45, 95, 120, 200, 400])
        last_login = today - timedelta(days=days_since_login)
        created = last_login - timedelta(days=random.randint(200, 900))
        mfa = random.choice([True, True, True, False])  # some without MFA on purpose

        writer.writerow([
            f"U{1000+i}",
            name,
            dept,
            role,
            last_login.strftime("%Y-%m-%d"),
            created.strftime("%Y-%m-%d"),
            mfa
        ])

print("users.csv generated with", len(names), "mock users.")
