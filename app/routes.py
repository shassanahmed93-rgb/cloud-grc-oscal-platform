import json
from pathlib import Path

from flask import Blueprint, render_template, send_file

from app.controls import CONTROL_CATALOG
from app.risk_engine import prioritize_findings

dashboard = Blueprint("dashboard", __name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FINDINGS_FILE = PROJECT_ROOT / "data" / "sample_findings.json"
SSP_FILE = PROJECT_ROOT / "system-security-plans" / "cloud-journal-api" / "system-security-plan.json"


def load_findings():
    with FINDINGS_FILE.open(encoding="utf-8") as file:
        return json.load(file)


@dashboard.route("/exports/oscal-ssp")
def export_oscal_ssp():
    if not SSP_FILE.is_file():
        return {"error": "OSCAL SSP file not found"}, 404

    return send_file(
        SSP_FILE,
        as_attachment=True,
        download_name="cloud-journal-api-ssp.json",
        mimetype="application/json",
    )


@dashboard.route("/")
def index():
    raw_findings = load_findings()
    findings = prioritize_findings(raw_findings)

    open_findings = [
        finding for finding in findings
        if finding["status"] == "OPEN"
    ]

    severity_counts = {
        severity: sum(
            finding["severity"] == severity
            for finding in open_findings
        )
        for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW")
    }

    risk_counts = {
        level: sum(
            finding["risk_level"] == level
            for finding in open_findings
        )
        for level in ("CRITICAL", "HIGH", "MEDIUM", "LOW")
    }

    findings_by_control = {}
    for finding in open_findings:
        control_id = finding["control_id"]
        findings_by_control.setdefault(control_id, []).append(finding)

    control_rows = []
    for control_id, control in CONTROL_CATALOG.items():
        control_rows.append({
            "id": control_id,
            **control,
            "open_findings": len(
                findings_by_control.get(control_id, [])
            ),
        })

    return render_template(
        "dashboard.html",
        findings=findings,
        open_count=len(open_findings),
        severity_counts=severity_counts,
        risk_counts=risk_counts,
        highest_risk=open_findings[:3],
        controls=findings_by_control,
        control_rows=control_rows,
    )
