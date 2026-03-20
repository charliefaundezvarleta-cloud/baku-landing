"""
Lead Export Module — Exports leads to CSV and JSON formats.
"""

import csv
import json
import os
import logging
from datetime import datetime

logger = logging.getLogger("baku.export")

DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def export_csv(
    leads: list[dict],
    package_name: str,
    output_dir: str = None,
    fields: list[str] = None,
) -> str:
    """
    Export leads to a CSV file.
    Returns the file path.
    """
    output_dir = output_dir or DEFAULT_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = package_name.lower().replace(" ", "_")
    filename = f"baku_leads_{slug}_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)

    if not leads:
        logger.warning("No leads to export.")
        return ""

    # Use specified fields or all fields from first lead
    if fields:
        headers = fields
    else:
        headers = list(leads[0].keys())

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for lead in leads:
            writer.writerow(lead)

    logger.info(f"Exported {len(leads)} leads to {filepath}")
    return filepath


def export_json(
    leads: list[dict],
    package_name: str,
    output_dir: str = None,
    metadata: dict = None,
) -> str:
    """
    Export leads to a JSON file with metadata.
    Returns the file path.
    """
    output_dir = output_dir or DEFAULT_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = package_name.lower().replace(" ", "_")
    filename = f"baku_leads_{slug}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    output = {
        "metadata": {
            "package": package_name,
            "generated_at": datetime.now().isoformat(),
            "total_leads": len(leads),
            "score_distribution": _score_distribution(leads),
            **(metadata or {}),
        },
        "leads": leads,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)

    logger.info(f"Exported {len(leads)} leads to {filepath}")
    return filepath


def generate_summary(leads: list[dict], package_name: str) -> dict:
    """Generate a summary report for the package."""
    if not leads:
        return {"package": package_name, "total": 0}

    grades = {"A": 0, "B": 0, "C": 0, "D": 0}
    has_email = 0
    has_phone = 0
    has_linkedin = 0
    verified_emails = 0
    companies = set()
    countries = set()

    for lead in leads:
        grades[lead.get("lead_grade", "D")] += 1
        if lead.get("email"):
            has_email += 1
        if lead.get("email_status") == "verified":
            verified_emails += 1
        if lead.get("phone"):
            has_phone += 1
        if lead.get("linkedin_url"):
            has_linkedin += 1
        if lead.get("company"):
            companies.add(lead["company"])
        if lead.get("country"):
            countries.add(lead["country"])

    total = len(leads)
    avg_score = round(sum(l.get("lead_score", 0) for l in leads) / total, 1)

    return {
        "package": package_name,
        "total_leads": total,
        "average_score": avg_score,
        "grade_distribution": grades,
        "email_coverage": f"{has_email}/{total} ({round(has_email/total*100)}%)",
        "verified_emails": f"{verified_emails}/{total} ({round(verified_emails/total*100)}%)",
        "phone_coverage": f"{has_phone}/{total} ({round(has_phone/total*100)}%)",
        "linkedin_coverage": f"{has_linkedin}/{total} ({round(has_linkedin/total*100)}%)",
        "unique_companies": len(companies),
        "countries": sorted(countries),
    }


def _score_distribution(leads: list[dict]) -> dict:
    grades = {"A": 0, "B": 0, "C": 0, "D": 0}
    for lead in leads:
        grade = lead.get("lead_grade", "D")
        grades[grade] = grades.get(grade, 0) + 1
    return grades
