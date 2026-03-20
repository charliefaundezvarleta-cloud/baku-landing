"""
Lead Enrichment Module — Enriches raw leads with additional data from Apollo.
"""

import logging
from .apollo_client import ApolloClient

logger = logging.getLogger("baku.enrich")

BATCH_SIZE = 10  # Apollo bulk enrichment limit


def enrich_leads(
    client: ApolloClient,
    leads: list[dict],
    enrichment_level: str = "basic",
    reveal_personal_emails: bool = False,
) -> list[dict]:
    """
    Enrich leads based on the tier's enrichment level.

    Levels:
    - basic: no enrichment call, use search data only (saves credits)
    - full: person enrichment (email, phone, LinkedIn, intent)
    - enterprise: person enrichment + org enrichment (tech, funding, headcount)
    """

    if enrichment_level == "basic":
        logger.info(f"Basic tier: skipping enrichment for {len(leads)} leads")
        return [_extract_basic(lead) for lead in leads]

    enriched = []

    if enrichment_level in ("full", "enterprise"):
        enriched = _enrich_people_batch(client, leads, reveal_personal_emails)

    if enrichment_level == "enterprise":
        enriched = _enrich_organizations(client, enriched)

    logger.info(f"Enrichment complete: {len(enriched)} leads enriched at '{enrichment_level}' level")
    return enriched


def _extract_basic(person: dict) -> dict:
    """Extract basic fields from search result (no API call needed)."""
    org = person.get("organization", {}) or {}
    return {
        "apollo_id": person.get("id"),
        "first_name": person.get("first_name", ""),
        "last_name": person.get("last_name", ""),
        "name": person.get("name", ""),
        "title": person.get("title", ""),
        "company": org.get("name", ""),
        "company_domain": org.get("primary_domain", ""),
        "country": person.get("country", ""),
        "city": person.get("city", ""),
        "state": person.get("state", ""),
        "company_size": org.get("estimated_num_employees", ""),
        "industry": org.get("industry", ""),
        "email": person.get("email", ""),
        "email_status": person.get("email_status", ""),
        "seniority": person.get("seniority", ""),
        "departments": ", ".join(person.get("departments", []) or []),
    }


def _enrich_people_batch(
    client: ApolloClient,
    leads: list[dict],
    reveal_personal_emails: bool,
) -> list[dict]:
    """Enrich people in batches of 10 using bulk enrichment."""
    enriched = []
    total_batches = (len(leads) + BATCH_SIZE - 1) // BATCH_SIZE

    for i in range(0, len(leads), BATCH_SIZE):
        batch = leads[i : i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        logger.info(f"Enriching batch {batch_num}/{total_batches} ({len(batch)} people)")

        # Build enrichment request
        details = []
        for person in batch:
            detail = {}
            if person.get("id"):
                detail["id"] = person["id"]
            if person.get("first_name"):
                detail["first_name"] = person["first_name"]
            if person.get("last_name"):
                detail["last_name"] = person["last_name"]
            org = person.get("organization", {}) or {}
            if org.get("primary_domain"):
                detail["domain"] = org["primary_domain"]
            if org.get("name"):
                detail["organization_name"] = org["name"]
            if person.get("linkedin_url"):
                detail["linkedin_url"] = person["linkedin_url"]

            details.append(detail)

        try:
            result = client.enrich_people_bulk(
                details=details,
                reveal_personal_emails=reveal_personal_emails,
            )

            matches = result.get("matches", [])
            for j, match in enumerate(matches):
                if match:
                    enriched.append(_extract_full(match))
                else:
                    # Fallback to basic data if no match
                    enriched.append(_extract_basic(batch[j]))

        except Exception as e:
            logger.error(f"Batch {batch_num} enrichment failed: {e}")
            # Fallback: use basic data for entire batch
            for person in batch:
                enriched.append(_extract_basic(person))

    return enriched


def _extract_full(person: dict) -> dict:
    """Extract full enriched fields from a person match."""
    org = person.get("organization", {}) or {}
    base = _extract_basic(person)

    # Add premium fields
    base.update({
        "email": person.get("email", base.get("email", "")),
        "email_status": person.get("email_status", ""),
        "linkedin_url": person.get("linkedin_url", ""),
        "phone": _get_phone(person),
        "company_linkedin": org.get("linkedin_url", ""),
        "company_website": org.get("website_url", ""),
        "company_founded_year": org.get("founded_year", ""),
        "headline": person.get("headline", ""),
        "photo_url": person.get("photo_url", ""),
        "intent_strength": person.get("intent_strength", ""),
        "departments": ", ".join(person.get("departments", []) or []),
    })

    return base


def _enrich_organizations(client: ApolloClient, leads: list[dict]) -> list[dict]:
    """Add org-level enrichment data for enterprise tier."""
    # Collect unique domains to enrich
    domains = list(set(
        lead["company_domain"]
        for lead in leads
        if lead.get("company_domain")
    ))

    logger.info(f"Enriching {len(domains)} unique organizations")

    org_data = {}

    # Enrich in batches of 10
    for i in range(0, len(domains), 10):
        batch = domains[i : i + 10]
        try:
            result = client.enrich_organizations_bulk(batch)
            for org in result.get("organizations", []):
                if org and org.get("primary_domain"):
                    org_data[org["primary_domain"]] = org
        except Exception as e:
            logger.error(f"Org enrichment batch failed: {e}")

    # Merge org data into leads
    for lead in leads:
        domain = lead.get("company_domain", "")
        if domain in org_data:
            org = org_data[domain]
            lead.update({
                "technologies": ", ".join(
                    t.get("name", "") for t in (org.get("current_technologies", []) or [])[:10]
                ),
                "total_funding": org.get("total_funding", ""),
                "latest_funding_round": org.get("latest_funding_round_type", ""),
                "latest_funding_amount": org.get("latest_funding_amount", ""),
                "revenue_range": org.get("estimated_annual_revenue", ""),
                "employee_count_exact": org.get("estimated_num_employees", ""),
                "company_description": org.get("short_description", ""),
            })

    return leads


def _get_phone(person: dict) -> str:
    """Extract best phone number from person data."""
    phones = person.get("phone_numbers", []) or []
    # Prefer direct dial
    for p in phones:
        if p.get("type") == "direct":
            return p.get("sanitized_number", "")
    # Fallback to mobile
    for p in phones:
        if p.get("type") == "mobile":
            return p.get("sanitized_number", "")
    # Fallback to any
    if phones:
        return phones[0].get("sanitized_number", "")
    return ""
