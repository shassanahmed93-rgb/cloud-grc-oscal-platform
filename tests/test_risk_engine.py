import pytest

from app.risk_engine import (
    calculate_risk,
    enrich_finding,
    prioritize_findings,
)


@pytest.mark.parametrize(
    ("likelihood", "impact", "score", "level"),
    [
        (1, 1, 1, "LOW"),
        (2, 2, 4, "LOW"),
        (1, 5, 5, "MEDIUM"),
        (3, 3, 9, "MEDIUM"),
        (2, 5, 10, "HIGH"),
        (4, 4, 16, "HIGH"),
        (5, 4, 20, "CRITICAL"),
        (5, 5, 25, "CRITICAL"),
    ],
)
def test_calculate_risk(likelihood, impact, score, level):
    assert calculate_risk(likelihood, impact) == {
        "score": score,
        "level": level,
    }


@pytest.mark.parametrize(
    ("likelihood", "impact"),
    [
        (0, 3),
        (6, 3),
        (3, 0),
        (3, 6),
        (True, 3),
        (3, 2.5),
    ],
)
def test_invalid_risk_inputs_are_rejected(likelihood, impact):
    expected_exception = (
        TypeError
        if isinstance(likelihood, (bool, float))
        or isinstance(impact, (bool, float))
        else ValueError
    )
    with pytest.raises(expected_exception):
        calculate_risk(likelihood, impact)


def test_enrich_finding_adds_risk_fields():
    finding = {
        "id": "F-TEST",
        "severity": "HIGH",
        "likelihood": 4,
        "impact": 4,
    }

    result = enrich_finding(finding)

    assert result["risk_score"] == 16
    assert result["risk_level"] == "HIGH"
    assert "risk_score" not in finding


def test_prioritize_findings_orders_highest_score_first():
    findings = [
        {"id": "F-LOW", "severity": "LOW", "likelihood": 1, "impact": 2},
        {"id": "F-CRITICAL", "severity": "HIGH", "likelihood": 5, "impact": 5},
        {"id": "F-MEDIUM", "severity": "MEDIUM", "likelihood": 3, "impact": 3},
    ]

    result = prioritize_findings(findings)

    assert [item["id"] for item in result] == [
        "F-CRITICAL",
        "F-MEDIUM",
        "F-LOW",
    ]
