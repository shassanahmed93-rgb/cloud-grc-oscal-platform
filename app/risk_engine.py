VALID_LEVELS = (
    (4, "LOW"),
    (9, "MEDIUM"),
    (16, "HIGH"),
    (25, "CRITICAL"),
)


def calculate_risk(likelihood, impact):
    """Calculate illustrative inherent risk on a 1–25 scale."""
    for name, value in (
        ("likelihood", likelihood),
        ("impact", impact),
    ):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer from 1 to 5")
        if not 1 <= value <= 5:
            raise ValueError(f"{name} must be between 1 and 5")

    score = likelihood * impact

    for maximum, level in VALID_LEVELS:
        if score <= maximum:
            return {
                "score": score,
                "level": level,
            }

    raise ValueError("Risk score is outside the supported range")


def enrich_finding(finding):
    """Return a finding with calculated risk fields."""
    result = dict(finding)
    risk = calculate_risk(
        result["likelihood"],
        result["impact"],
    )
    result["risk_score"] = risk["score"]
    result["risk_level"] = risk["level"]
    return result


def prioritize_findings(findings):
    """Sort highest risk first, then highest score."""
    enriched = [enrich_finding(finding) for finding in findings]
    return sorted(
        enriched,
        key=lambda item: (
            item["risk_score"],
            item["severity"] == "CRITICAL",
            item["severity"] == "HIGH",
        ),
        reverse=True,
    )
