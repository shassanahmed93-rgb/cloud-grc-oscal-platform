import json
from pathlib import Path

import regex
from jsonschema import FormatChecker
from jsonschema.validators import extend, validator_for

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_FILE = ROOT / "schemas" / "oscal_ssp_schema.json"
SSP_FILE = (
    ROOT
    / "system-security-plans"
    / "cloud-journal-api"
    / "system-security-plan.json"
)


def unicode_pattern(validator, pattern, instance, schema):
    if not validator.is_type(instance, "string"):
        return

    try:
        matches = regex.search(pattern, instance)
    except regex.error as exc:
        from jsonschema.exceptions import SchemaError

        raise SchemaError(
            f"Invalid Unicode regular expression {pattern!r}: {exc}"
        ) from exc

    if matches is None:
        from jsonschema.exceptions import ValidationError

        yield ValidationError(
            f"{instance!r} does not match pattern {pattern!r}"
        )


def main() -> int:
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    ssp = json.loads(SSP_FILE.read_text(encoding="utf-8"))

    base_validator = validator_for(schema)
    checker = FormatChecker()
    checker.checkers["regex"] = (
        lambda value: not isinstance(value, str)
        or _valid_unicode_regex(value),
        "must be a valid Unicode regular expression",
    )

    validator_class = extend(
        base_validator,
        validators={"pattern": unicode_pattern},
    )
    validator = validator_class(schema, format_checker=checker)

    errors = sorted(
        validator.iter_errors(ssp),
        key=lambda error: list(map(str, error.absolute_path)),
    )

    if errors:
        print(f"FAIL: SSP has {len(errors)} schema validation error(s).")
        for error in errors[:20]:
            path = "/" + "/".join(map(str, error.absolute_path))
            print(f"- {path}: {error.message}")
        return 1

    print("PASS: SSP conforms to the OSCAL 1.1.2 JSON schema.")
    return 0


def _valid_unicode_regex(value: str) -> bool:
    try:
        regex.compile(value)
        return True
    except regex.error:
        return False


if __name__ == "__main__":
    raise SystemExit(main())
