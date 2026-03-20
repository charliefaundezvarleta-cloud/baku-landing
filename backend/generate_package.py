#!/usr/bin/env python3
"""
BAKU Lead Package Generator — Main Entry Point.

Usage:
    python generate_package.py --package starter_saas
    python generate_package.py --package growth_tech --location "United States"
    python generate_package.py --package enterprise_pack --min-score 50
    python generate_package.py --custom --industry saas --count 100 --tier premium

Environment:
    APOLLO_API_KEY  — Your Apollo.io API key (required)

Designed to run standalone — no MCP, no Vercel, no framework dependencies.
Just Python + requests + Apollo API key.
"""

import argparse
import json
import logging
import os
import sys

# Add parent dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.apollo_client import ApolloClient
from core.lead_search import search_leads
from core.lead_enrich import enrich_leads
from core.lead_scorer import score_leads, filter_by_min_score
from core.lead_export import export_csv, export_json, generate_summary

# ── Config ───────────────────────────────────────────────────────────

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def load_config(name: str) -> dict:
    path = os.path.join(CONFIG_DIR, f"{name}.json")
    with open(path, "r") as f:
        return json.load(f)


# ── Main Pipeline ────────────────────────────────────────────────────

def generate_package(
    package_id: str = None,
    industry: str = None,
    lead_count: int = None,
    tier: str = None,
    location: list[str] = None,
    min_score: int = 0,
    output_format: str = "both",
    dry_run: bool = False,
) -> dict:
    """
    Generate a lead package end-to-end.

    Can run from a predefined package (--package) or custom params.
    Returns a summary dict with file paths and stats.
    """

    packages_config = load_config("packages")
    industries_config = load_config("industries")

    # ── Resolve package config ──────────────────────────────────────

    if package_id:
        pkg = packages_config["packages"].get(package_id)
        if not pkg:
            available = ", ".join(packages_config["packages"].keys())
            raise ValueError(f"Unknown package '{package_id}'. Available: {available}")

        package_name = pkg["name"]
        industry = pkg["industry"]
        lead_count = pkg["lead_count"]
        tier = pkg["tier"]
        enrichment_level = packages_config["tiers"][tier]["enrichment_level"]
        fields = packages_config["tiers"][tier]["fields"]
    else:
        if not industry or not lead_count or not tier:
            raise ValueError("Custom mode requires --industry, --count, and --tier")
        package_name = f"Custom {industry.title()} ({lead_count} leads)"
        enrichment_level = packages_config["tiers"][tier]["enrichment_level"]
        fields = packages_config["tiers"][tier]["fields"]

    industry_config = industries_config["industries"].get(industry)
    if not industry_config:
        available = ", ".join(industries_config["industries"].keys())
        raise ValueError(f"Unknown industry '{industry}'. Available: {available}")

    # ── Log plan ────────────────────────────────────────────────────

    logger.info("=" * 60)
    logger.info(f"BAKU Lead Package Generator")
    logger.info(f"Package: {package_name}")
    logger.info(f"Industry: {industry_config['name']}")
    logger.info(f"Lead count: {lead_count}")
    logger.info(f"Tier: {tier} (enrichment: {enrichment_level})")
    logger.info(f"Location filter: {location or 'none'}")
    logger.info(f"Min score: {min_score}")
    logger.info("=" * 60)

    if dry_run:
        logger.info("DRY RUN — no API calls will be made.")
        return {"status": "dry_run", "package": package_name}

    # ── Initialize Apollo client ────────────────────────────────────

    client = ApolloClient()
    client.reset_credits_counter()

    # ── Step 1: Search ──────────────────────────────────────────────

    logger.info("[1/4] Searching for leads...")
    raw_leads = search_leads(
        client=client,
        industry_config=industry_config,
        lead_count=lead_count,
        location_filter=location,
    )
    logger.info(f"Found {len(raw_leads)} raw leads")

    if not raw_leads:
        logger.error("No leads found. Try adjusting filters.")
        return {"status": "error", "message": "No leads found"}

    # ── Step 2: Enrich ──────────────────────────────────────────────

    logger.info(f"[2/4] Enriching leads ({enrichment_level})...")
    enriched_leads = enrich_leads(
        client=client,
        leads=raw_leads,
        enrichment_level=enrichment_level,
    )
    logger.info(f"Enriched {len(enriched_leads)} leads")

    # ── Step 3: Score ───────────────────────────────────────────────

    logger.info("[3/4] Scoring leads...")
    scored_leads = score_leads(enriched_leads)

    if min_score > 0:
        scored_leads = filter_by_min_score(scored_leads, min_score)

    # Trim to exact count requested
    scored_leads = scored_leads[:lead_count]

    # ── Step 4: Export ──────────────────────────────────────────────

    logger.info("[4/4] Exporting...")

    # Always add score fields to export
    export_fields = fields + ["lead_score", "lead_grade"]

    csv_path = ""
    json_path = ""

    if output_format in ("csv", "both"):
        csv_path = export_csv(scored_leads, package_name, OUTPUT_DIR, export_fields)

    if output_format in ("json", "both"):
        json_path = export_json(
            scored_leads,
            package_name,
            OUTPUT_DIR,
            metadata={
                "tier": tier,
                "enrichment_level": enrichment_level,
                "industry": industry,
                "location_filter": location,
                "min_score": min_score,
                "credits_used": client.credits_used,
            },
        )

    # ── Summary ─────────────────────────────────────────────────────

    summary = generate_summary(scored_leads, package_name)
    summary["credits_used"] = client.credits_used
    summary["csv_file"] = csv_path
    summary["json_file"] = json_path
    summary["status"] = "success"

    logger.info("=" * 60)
    logger.info("GENERATION COMPLETE")
    for k, v in summary.items():
        logger.info(f"  {k}: {v}")
    logger.info("=" * 60)

    return summary


# ── CLI ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="BAKU Lead Package Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --package starter_saas
  %(prog)s --package growth_tech --location "United States"
  %(prog)s --package enterprise_pack --min-score 50
  %(prog)s --custom --industry saas --count 100 --tier premium
  %(prog)s --list-packages
  %(prog)s --list-industries
        """,
    )

    # Package mode
    parser.add_argument("--package", "-p", help="Predefined package ID to generate")

    # Custom mode
    parser.add_argument("--custom", action="store_true", help="Use custom parameters")
    parser.add_argument("--industry", "-i", help="Industry template to use")
    parser.add_argument("--count", "-c", type=int, help="Number of leads to generate")
    parser.add_argument("--tier", "-t", choices=["standard", "premium", "enterprise"])

    # Filters
    parser.add_argument("--location", "-l", nargs="+", help="Location filter(s)")
    parser.add_argument("--min-score", type=int, default=0, help="Minimum lead score (0-100)")

    # Output
    parser.add_argument("--format", "-f", choices=["csv", "json", "both"], default="both")
    parser.add_argument("--dry-run", action="store_true", help="Preview without API calls")

    # Info
    parser.add_argument("--list-packages", action="store_true", help="List available packages")
    parser.add_argument("--list-industries", action="store_true", help="List available industries")

    args = parser.parse_args()

    # Info commands
    if args.list_packages:
        config = load_config("packages")
        print("\nAvailable packages:")
        print("-" * 60)
        for pid, pkg in config["packages"].items():
            print(f"  {pid:25s} {pkg['name']:20s} {pkg['lead_count']:>5} leads  ${pkg['price_usd']}")
        print()
        return

    if args.list_industries:
        config = load_config("industries")
        print("\nAvailable industries:")
        print("-" * 60)
        for iid, ind in config["industries"].items():
            tags = ", ".join(ind["apollo_keyword_tags"][:3]) or "all"
            print(f"  {iid:15s} {ind['name']:20s} tags: {tags}")
        print()
        return

    # Validate
    if not args.package and not args.custom:
        parser.error("Specify --package <id> or --custom with --industry, --count, --tier")

    # Run
    try:
        result = generate_package(
            package_id=args.package,
            industry=args.industry,
            lead_count=args.count,
            tier=args.tier,
            location=args.location,
            min_score=args.min_score,
            output_format=args.format,
            dry_run=args.dry_run,
        )

        if result.get("status") == "success":
            print(f"\nPackage generated successfully!")
            print(f"  Leads: {result['total_leads']}")
            print(f"  Avg score: {result['average_score']}")
            print(f"  Credits used: {result['credits_used']}")
            if result.get("csv_file"):
                print(f"  CSV: {result['csv_file']}")
            if result.get("json_file"):
                print(f"  JSON: {result['json_file']}")

    except Exception as e:
        logger.error(f"Failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger("baku")
    main()
else:
    logger = logging.getLogger("baku")
