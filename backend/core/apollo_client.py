"""
Apollo API Client for BAKU Lead Generation Engine.

Standalone wrapper that uses Apollo REST API directly.
No MCP dependencies — runs anywhere with an API key.
"""

import os
import time
import logging
import requests
from typing import Optional

logger = logging.getLogger("baku.apollo")

APOLLO_BASE_URL = "https://api.apollo.io"

# Rate limiting defaults
DEFAULT_RATE_LIMIT_DELAY = 1.0  # seconds between requests
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


class ApolloClient:
    """Lightweight Apollo API client with rate limiting and retry logic."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("APOLLO_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Apollo API key required. Set APOLLO_API_KEY env var or pass api_key."
            )
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        })
        self._last_request_time = 0
        self._credits_used = 0

    def _rate_limit(self):
        """Enforce minimum delay between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < DEFAULT_RATE_LIMIT_DELAY:
            time.sleep(DEFAULT_RATE_LIMIT_DELAY - elapsed)
        self._last_request_time = time.time()

    def _request(self, method: str, endpoint: str, payload: dict = None) -> dict:
        """Make an API request with retry logic."""
        url = f"{APOLLO_BASE_URL}{endpoint}"

        # Always include API key in payload
        if payload is None:
            payload = {}
        payload["api_key"] = self.api_key

        for attempt in range(MAX_RETRIES):
            self._rate_limit()
            try:
                if method == "GET":
                    resp = self.session.get(url, params=payload, timeout=30)
                else:
                    resp = self.session.post(url, json=payload, timeout=30)

                if resp.status_code == 429:
                    # Rate limited — back off
                    wait = RETRY_DELAY * (attempt + 1)
                    logger.warning(f"Rate limited. Waiting {wait}s...")
                    time.sleep(wait)
                    continue

                resp.raise_for_status()
                return resp.json()

            except requests.exceptions.RequestException as e:
                if attempt < MAX_RETRIES - 1:
                    logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error(f"Request failed after {MAX_RETRIES} attempts: {e}")
                    raise

    # ── People Search ────────────────────────────────────────────────

    def search_people(
        self,
        person_titles: list[str] = None,
        person_seniorities: list[str] = None,
        person_locations: list[str] = None,
        organization_locations: list[str] = None,
        organization_num_employees_ranges: list[str] = None,
        q_organization_keyword_tags: list[str] = None,
        q_keywords: str = None,
        contact_email_status: list[str] = None,
        currently_using_any_of_technology_uids: list[str] = None,
        revenue_range: dict = None,
        page: int = 1,
        per_page: int = 25,
    ) -> dict:
        """
        Search Apollo's people database.
        Does NOT return emails/phones — use enrich_person for that.
        Costs: free (search only), credits on reveal.
        """
        payload = {"page": page, "per_page": per_page}

        # Add non-None filters
        filters = {
            "person_titles": person_titles,
            "person_seniorities": person_seniorities,
            "person_locations": person_locations,
            "organization_locations": organization_locations,
            "organization_num_employees_ranges": organization_num_employees_ranges,
            "q_organization_keyword_tags": q_organization_keyword_tags,
            "q_keywords": q_keywords,
            "contact_email_status": contact_email_status,
            "currently_using_any_of_technology_uids": currently_using_any_of_technology_uids,
            "revenue_range": revenue_range,
        }
        for k, v in filters.items():
            if v is not None:
                payload[k] = v

        result = self._request("POST", "/api/v1/mixed_people/search", payload)
        logger.info(
            f"People search: page {page}, "
            f"found {result.get('pagination', {}).get('total_entries', 0)} total"
        )
        return result

    # ── People Enrichment ────────────────────────────────────────────

    def enrich_person(
        self,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        domain: str = None,
        organization_name: str = None,
        linkedin_url: str = None,
        apollo_id: str = None,
        reveal_personal_emails: bool = False,
    ) -> dict:
        """
        Enrich a single person. Returns email, phone, full profile.
        Costs: ~1 credit per match.
        """
        payload = {"reveal_personal_emails": reveal_personal_emails}

        fields = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "domain": domain,
            "organization_name": organization_name,
            "linkedin_url": linkedin_url,
            "id": apollo_id,
        }
        for k, v in fields.items():
            if v is not None:
                payload[k] = v

        self._credits_used += 1
        return self._request("POST", "/api/v1/people/match", payload)

    def enrich_people_bulk(
        self,
        details: list[dict],
        reveal_personal_emails: bool = False,
    ) -> dict:
        """
        Enrich up to 10 people at once.
        Each entry in details should have: first_name, last_name, domain, etc.
        Costs: ~1 credit per match.
        """
        if len(details) > 10:
            raise ValueError("Apollo bulk enrichment supports max 10 people per call.")

        payload = {
            "details": details,
            "reveal_personal_emails": reveal_personal_emails,
        }
        self._credits_used += len(details)
        return self._request("POST", "/api/v1/people/bulk_match", payload)

    # ── Organization Search & Enrichment ─────────────────────────────

    def search_organizations(
        self,
        q_organization_keyword_tags: list[str] = None,
        organization_locations: list[str] = None,
        organization_num_employees_ranges: list[str] = None,
        currently_using_any_of_technology_uids: list[str] = None,
        revenue_range: dict = None,
        page: int = 1,
        per_page: int = 25,
    ) -> dict:
        """Search Apollo's organization database."""
        payload = {"page": page, "per_page": per_page}

        filters = {
            "q_organization_keyword_tags": q_organization_keyword_tags,
            "organization_locations": organization_locations,
            "organization_num_employees_ranges": organization_num_employees_ranges,
            "currently_using_any_of_technology_uids": currently_using_any_of_technology_uids,
            "revenue_range": revenue_range,
        }
        for k, v in filters.items():
            if v is not None:
                payload[k] = v

        return self._request("POST", "/api/v1/mixed_companies/search", payload)

    def enrich_organization(self, domain: str) -> dict:
        """Enrich a single organization by domain."""
        self._credits_used += 1
        return self._request("GET", "/api/v1/organizations/enrich", {"domain": domain})

    def enrich_organizations_bulk(self, domains: list[str]) -> dict:
        """Enrich up to 10 organizations by domain."""
        if len(domains) > 10:
            raise ValueError("Apollo bulk org enrichment supports max 10 per call.")
        self._credits_used += len(domains)
        return self._request(
            "POST", "/api/v1/organizations/bulk_enrich", {"domains": domains}
        )

    # ── Utils ────────────────────────────────────────────────────────

    @property
    def credits_used(self) -> int:
        """Track estimated credits consumed in this session."""
        return self._credits_used

    def reset_credits_counter(self):
        self._credits_used = 0
