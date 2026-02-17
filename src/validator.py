import json
from pathlib import Path

from jsonschema import validate
from jsonschema.exceptions import ValidationError


VM_SCHEMA = {
    "type": "object",
    "required": ["name", "os", "cpu", "ram"],
    "additionalProperties": False,
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "pattern": "^[a-zA-Z0-9-]+$"
        },
        "os": {
            "type": "string",
            "enum": ["Ubuntu", "CentOS"]
        },
        "cpu": {
            "type": "string",
            "pattern": "^[0-9]+vCPU$"
        },
        "ram": {
            "type": "string",
            "pattern": "^[0-9]+GB$"
        }
    }
}


INSTANCES_SCHEMA = {
    "type": "array",
    "items": VM_SCHEMA,
}


def validate_instance(data: dict) -> tuple[bool, str]:
    try:
        validate(instance=data, schema=VM_SCHEMA)
        return True, ""
    except ValidationError as e:
        return False, e.message


def validate_instances_file(path: str | Path) -> tuple[bool, str]:
    config_path = Path(path)

    if not config_path.exists():
        return True, ""

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"{config_path}: invalid JSON at line {e.lineno}, column {e.colno} ({e.msg})"
    except OSError as e:
        return False, f"{config_path}: cannot read file ({e})"

    try:
        validate(instance=payload, schema=INSTANCES_SCHEMA)
        return True, ""
    except ValidationError as e:
        return False, f"{config_path}: schema validation failed ({e.message})"
