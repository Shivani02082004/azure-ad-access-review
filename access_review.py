"""
Azure AD-style Access Review Simulator
----------------------------------------
Reads a user access CSV and flags accounts that would typically be caught
in a real IAM access review:

  1. STALE ACCOUNTS      - no login in 90+ days
  2. OVER-PRIVILEGED      - holds a high-privilege admin role
  3. HIGH RISK            - admin role + no MFA enabled
  4. STALE + PRIVILEGED   - the worst combination: unused admin access

Usage:
    python3 access_review.py users.csv
"""

import csv
import sys
from datetime import datetime

HIGH_PRIV_ROLES = {"Global Admin", "User Admin", "Application Admin", "Billing Admin"}
STALE_THRESHOLD_DAYS = 90


def load_users(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def days_since(date_str):
    last_login = datetime.strptime(date_str, "%Y-%m-%d")
    return (datetime.now() - last_login).days


def review(users):
    findings = []
    for u in users:
        flags = []
        idle_days = days_since(u["last_login_date"])
        is_privileged = u["role"] in HIGH_PRIV_ROLES
        has_mfa = u["mfa_enabled"].strip().lower() == "true"

        if idle_days >= STALE_THRESHOLD_DAYS:
            flags.append(f"STALE (no login in {idle_days} days)")

        if is_privileged:
            flags.append(f"OVER-PRIVILEGED ({u['role']})")

        if is_privileged and not has_mfa:
            flags.append("HIGH RISK: privileged role without MFA")

        if flags:
            findings.append({
                "user_id": u["user_id"],
                "name": u["full_name"],
                "department": u["department"],
                "role": u["role"],
                "flags": flags
            })
    return findings


def print_report(findings, total_users):
    print("=" * 60)
    print("AZURE AD ACCESS REVIEW REPORT")
    print("=" * 60)
    print(f"Total accounts reviewed: {total_users}")
    print(f"Accounts flagged: {len(findings)}\n")

    for f in findings:
        print(f"[{f['user_id']}] {f['name']} — {f['department']} — {f['role']}")
        for flag in f["flags"]:
            print(f"    -> {flag}")
        print()

    if not findings:
        print("No issues found. All accounts pass review.")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "users.csv"
    users = load_users(path)
    findings = review(users)
    print_report(findings, len(users))
