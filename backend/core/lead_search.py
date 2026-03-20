"""
Lead Search Module — Queries Apollo for raw leads based on package config.
"""

import logging
import math
from .apollo_client import ApolloClient

logger = logging.getLogger("baku.search")


def search_leads(
    client: ApolloClient,
    industry_config: dict,
    lead_count: int,
    location_filter: list[str] = None,
    title_override: list[str] = None,
    seniority_override: list[str] = None,
    employee_range_override: list[str] = None,
    technology_filter: list[str] = None,
    email_status_filter: list[str] = None,
) -> list[dict]:
    """
    Search Apollo for leads matching the industry template + overrides.

    Returns a list of raw person dicts from Apollo.
    Fetches enough pages to fill lead_count (with ~20% buffer for dedup/filtering).
    """

    titles = title_override or industry_config.get("default_titles", [])
    seniorities = seniority_override or industry_config.get("default_seniorities", [])
    employee_ranges = employee_range_override or industry_config.get("default_employee_ranges", [])
    keyword_tags = industry_config.get("apollo_keyword_tags", [])
    tech_signals = technology_filter or industry_config.get("technology_signals", [])

    # Default: only verified or likely-to-engage emails
    email_status = email_status_filter or ["verified", "likely to engage"]

    # Request 20% buffer to account for dedup and filtering
    target_count = math.ceil(lead_count * 1.2)
    per_page = min(100, target_count)
    total_pages = math.ceil(target_count / per_page)

    all_people = []
    seen_ids = set()

    logger.info(
        f"Searching for {lead_count} leads "
        f"(target: {target_count} with buffer, {total_pages} pages)"
    )

    for page in range(1, total_pages + 1):
        try:
            result = client.search_people(
                person_titles=titles if titles else None,
                person_seniorities=seniorities if seniorities else None,
                person_locations=location_filter,
                q_organization_keyword_tags=keyword_tags if keyword_tags else None,
                organization_num_employees_ranges=employee_ranges if employee_ranges else None,
                contact_email_status=email_status,
                currently_using_any_of_technology_uids=tech_signals if tech_signals else None,
                page=page,
                per_page=per_page,
            )

            people = result.get("people", [])
            if not people:
                logger.info(f"No more results at page {page}. Stopping.")
                break

            # Deduplicate by Apollo ID
            for person in people:
                pid = person.get("id")
                if pid and pid not in seen_ids:
                    seen_ids.add(pid)
                    all_people.append(person)

            logger.info(f"Page {page}: got {len(people)} people (total: {len(all_people)})")

            # Check if we have enough
            if len(all_people) >= target_count:
                break

            # Check if there are more pages
            pagination = result.get("pagination", {})
            total_available = pagination.get("total_entries", 0)
            if page * per_page >= total_available:
                logger.info(f"Exhausted results ({total_available} total). Stopping.")
                break

        except Exception as e:
            logger.error(f"Search failed at page {page}: {e}")
            break

    # Trim to requested count
    final_leads = all_people[:lead_count]
    logger.info(f"Search complete: {len(final_leads)} leads collected")
    return final_leads
