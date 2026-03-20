"""
Lead Scoring Module — Assigns quality scores to enriched leads.
"""

import logging

logger = logging.getLogger("baku.scorer")

# Scoring weights
SCORING_RULES = {
    "has_email": 3,
    "email_verified": 5,
    "email_likely_engage": 3,
    "has_phone": 4,
    "has_linkedin": 2,
    "seniority_c_suite": 5,
    "seniority_vp": 4,
    "seniority_director": 3,
    "seniority_manager": 2,
    "has_company_domain": 1,
    "has_title": 1,
    "has_intent_signals": 4,
    "has_technologies": 2,  # enterprise
    "has_funding_data": 2,  # enterprise
}

MAX_POSSIBLE_SCORE = sum(SCORING_RULES.values())


def score_leads(leads: list[dict]) -> list[dict]:
    """
    Score each lead based on data completeness and quality signals.
    Adds 'lead_score' (0-100) and 'lead_grade' (A/B/C/D) to each lead.
    """
    scored = []

    for lead in leads:
        raw_score = 0

        # Email scoring
        if lead.get("email"):
            raw_score += SCORING_RULES["has_email"]
            status = (lead.get("email_status") or "").lower()
            if status == "verified":
                raw_score += SCORING_RULES["email_verified"]
            elif status in ("likely to engage", "likely_to_engage"):
                raw_score += SCORING_RULES["email_likely_engage"]

        # Contact info
        if lead.get("phone"):
            raw_score += SCORING_RULES["has_phone"]
        if lead.get("linkedin_url"):
            raw_score += SCORING_RULES["has_linkedin"]

        # Seniority
        seniority = (lead.get("seniority") or "").lower()
        if seniority == "c_suite":
            raw_score += SCORING_RULES["seniority_c_suite"]
        elif seniority == "vp":
            raw_score += SCORING_RULES["seniority_vp"]
        elif seniority == "director":
            raw_score += SCORING_RULES["seniority_director"]
        elif seniority == "manager":
            raw_score += SCORING_RULES["seniority_manager"]

        # Basic completeness
        if lead.get("company_domain"):
            raw_score += SCORING_RULES["has_company_domain"]
        if lead.get("title"):
            raw_score += SCORING_RULES["has_title"]

        # Premium signals
        if lead.get("intent_strength"):
            raw_score += SCORING_RULES["has_intent_signals"]

        # Enterprise signals
        if lead.get("technologies"):
            raw_score += SCORING_RULES["has_technologies"]
        if lead.get("total_funding") or lead.get("latest_funding_amount"):
            raw_score += SCORING_RULES["has_funding_data"]

        # Normalize to 0-100
        normalized_score = round((raw_score / MAX_POSSIBLE_SCORE) * 100)
        grade = _score_to_grade(normalized_score)

        lead["lead_score"] = normalized_score
        lead["lead_grade"] = grade
        scored.append(lead)

    # Sort by score descending
    scored.sort(key=lambda x: x["lead_score"], reverse=True)

    # Log distribution
    grades = {"A": 0, "B": 0, "C": 0, "D": 0}
    for lead in scored:
        grades[lead["lead_grade"]] += 1
    logger.info(f"Scoring complete: {grades}")

    return scored


def _score_to_grade(score: int) -> str:
    """Convert numeric score to letter grade."""
    if score >= 75:
        return "A"
    elif score >= 50:
        return "B"
    elif score >= 25:
        return "C"
    else:
        return "D"


def filter_by_min_score(leads: list[dict], min_score: int = 0) -> list[dict]:
    """Filter out leads below a minimum score threshold."""
    filtered = [l for l in leads if l.get("lead_score", 0) >= min_score]
    removed = len(leads) - len(filtered)
    if removed > 0:
        logger.info(f"Filtered out {removed} leads below score {min_score}")
    return filtered
