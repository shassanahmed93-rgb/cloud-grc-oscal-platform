
from app import create_app


def test_dashboard_loads_successfully():
    app = create_app()
    app.config["TESTING"] = True

    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"Cloud GRC" in response.data
    assert b"NIST Control Catalog" in response.data
    assert b"AC-6" in response.data


def test_dashboard_shows_expected_findings():
    app = create_app()
    app.config["TESTING"] = True

    response = app.test_client().get("/")

    assert b"Open Findings" in response.data
    assert b"F-001" in response.data
    assert b"F-002" in response.data


def test_oscal_ssp_download_returns_valid_json_attachment():
    import json

    app = create_app()
    app.config["TESTING"] = True

    response = app.test_client().get("/exports/oscal-ssp")

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert "attachment" in response.headers.get("Content-Disposition", "")
    assert "cloud-journal-api-ssp.json" in response.headers.get(
        "Content-Disposition", ""
    )

    payload = json.loads(response.get_data(as_text=True))
    ssp = payload["system-security-plan"]

    assert ssp["metadata"]["title"] == "Cloud GRC Portfolio Demonstration SSP"
    assert ssp["metadata"]["oscal-version"] == "1.1.2"
    assert ssp["uuid"]
