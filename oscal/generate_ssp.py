
import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "oscal" / "ssp.json"


def new_uuid():
    return str(uuid.uuid4())


def build_ssp():
    now = datetime.now(UTC).isoformat().replace("+00:00", "Z")

    return {
        "system-security-plan": {
            "uuid": new_uuid(),
            "metadata": {
                "title": "Cloud GRC Portfolio Demonstration SSP",
                "published": now,
                "last-modified": now,
                "version": "0.1.0",
                "oscal-version": "1.1.2",
                "roles": [
                    {
                        "id": "system-owner",
                        "title": "System Owner",
                    },
                    {
                        "id": "security-assessor",
                        "title": "Security Assessor",
                    },
                ],
                "parties": [
                    {
                        "uuid": new_uuid(),
                        "type": "organization",
                        "name": "Fictional Portfolio Organization",
                    }
                ],
            },
            "import-profile": {
                "href": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_MODERATE-baseline_profile.json"
            },
            "system-characteristics": {
                "system-ids": [
                    {
                        "identifier-type": "https://ietf.org/rfc/rfc4122",
                        "id": new_uuid(),
                    }
                ],
                "system-name": "Portfolio Cloud Journal API",
                "description": (
                    "A portfolio demonstration system used to document "
                    "security controls and illustrative assessment evidence."
                ),"system-information": {
    "information-types": [
        {
            "uuid": new_uuid(),
            "title": "Journal API operational data",
            "description": (
                "Illustrative information type for API requests "
                "and journal records. Actual data classification "
                "must be verified."
            ),
        }
    ],
},
                "security-sensitivity-level": "moderate",
                "status": {
                    "state": "other",
                    "remarks": (
                        "Demonstration SSP. This document does not establish "
                        "authorization or compliance."
                    ),
                },
                "authorization-boundary": {
                    "description": (
                        "Illustrative boundary for a cloud-hosted API, "
                        "its application components, and supporting data store."
                    ),
                },
                "network-architecture": {
                    "description": (
                        "Illustrative cloud architecture. Actual deployed "
                        "resources and network paths must be verified."
                    ),
                },
                "data-flow": {
                    "description": (
                        "Users send API requests to the application. "
                        "The application processes requests and accesses "
                        "persistent storage. Actual data flows require verification."
                    ),
                },
            },
            "system-implementation": {
                "users": [
                    {
                        "uuid": new_uuid(),
                        "title": "API User",
                        "description": (
                            "A hypothetical user who sends requests to the API."
                        ),
                        "role-ids": ["system-owner"],
                    }
                ],
                "components": [
                    {
                        "uuid": new_uuid(),
                        "type": "software",
                        "title": "Journal API",
                        "description": (
                            "Python API application. Deployment configuration "
                            "must be verified against the live environment."
                        ),
                        "status": {"state": "operational"},
                    },
                    {
                        "uuid": new_uuid(),
                        "type": "service",
                        "title": "Persistent Data Store",
                        "description": (
                            "Illustrative database component. The actual "
                            "database engine and hosting configuration must be verified."
                        ),
                        "status": {"state": "other"},
                    },
                ],
            },
            "control-implementation": {
                "description": (
                    "Initial control documentation. The statements below "
                    "are assessment placeholders, not evidence of compliance."
                ),
                "implemented-requirements": [
                    {
                        "uuid": new_uuid(),
                        "control-id": control_id,
                        "remarks": "Assessment status: not assessed. " + statement,
                    }
                    for control_id, statement in [
                        (
                            "ac-6",
                            "Review access permissions and verify least privilege.",
                        ),
                        (
                            "au-2",
                            "Identify required audit events and verify logging coverage.",
                        ),
                        (
                            "ca-7",
                            "Define continuous monitoring responsibilities and evidence.",
                        ),
                        (
                            "cm-6",
                            "Document and verify security configuration settings.",
                        ),
                        (
                            "sc-8",
                            "Verify protections for information in transit.",
                        ),
                    ]
                ],
            },
        }
    }


def main():
    ssp = build_ssp()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(ssp, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Generated: {OUTPUT_FILE}")
    print("Assessment status: not assessed")
    print("This demonstration is not a compliance determination.")


if __name__ == "__main__":
    main()
