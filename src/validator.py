# src/validator.py
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


def validate_instance(data: dict) -> tuple[bool, str]:
    try:
        validate(instance=data, schema=VM_SCHEMA)
        return True, ""
    except ValidationError as e:
        return False, e.message
