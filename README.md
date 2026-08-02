# Azure AD Access Review Simulator

A Python tool that simulates a real-world Identity and Access Management (IAM) access review — the kind of periodic audit used to catch stale accounts, over-privileged roles, and security risks in an Azure Active Directory environment.

## Why I built this

In my role as a Service Desk Analyst, I manage Azure Active Directory access requests, permission changes, and access reviews daily for an enterprise environment. This project automates the core logic behind that manual review process: identifying accounts that are stale, over-privileged, or high-risk due to missing MFA.

## What it flags

| Flag | Meaning |
|---|---|
| **STALE** | No login in 90+ days |
| **OVER-PRIVILEGED** | Holds a high-privilege admin role (Global Admin, User Admin, Application Admin, Billing Admin) |
| **HIGH RISK** | Privileged role with MFA not enabled |

## How it works

1. `generate_mock_users.py` creates a sample dataset (`users.csv`) of 20 mock Azure AD-style accounts with realistic fields: role, last login date, account creation date, and MFA status.
2. `access_review.py` reads that CSV and applies review rules to flag risky accounts, then prints a formatted report.

## Usage

```bash
python3 generate_mock_users.py     # creates users.csv
python3 access_review.py users.csv # runs the review and prints findings
```

## Example output

```
[U1005] Karan Verma — Customer Service — Application Admin
    -> STALE (no login in 200 days)
    -> OVER-PRIVILEGED (Application Admin)
    -> HIGH RISK: privileged role without MFA
```

## Possible extensions

- Export findings to CSV/Excel for reporting
- Add configurable thresholds (e.g., 60 vs 90 day staleness)
- Extend to parse real AWS IAM policy JSON exports

## Tech used

Jupyter Notebook,Google Colab, `csv`, `datetime` — no external dependencies.
