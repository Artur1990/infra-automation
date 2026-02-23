from __future__ import annotations

import json
import re
from pathlib import Path

from pydantic import BaseModel, ValidationError, field_validator


class InstanceSpec(BaseModel):
    name: str
    os: str
    cpu: str
    ram: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]{1,30}", value):
            raise ValueError("name must start with a letter and contain letters, digits, or '-' (2-31 chars)")
        return value

    @field_validator("os")
    @classmethod
    def validate_os(cls, value: str) -> str:
        allowed = {"ubuntu", "centos"}
        if value.lower() not in allowed:
            raise ValueError("os must be Ubuntu or CentOS")
        return value.title()

    @field_validator("cpu")
    @classmethod
    def validate_cpu(cls, value: str) -> str:
        if not re.fullmatch(r"\d+vCPU", value):
            raise ValueError("cpu must match pattern like 2vCPU")
        return value

    @field_validator("ram")
    @classmethod
    def validate_ram(cls, value: str) -> str:
        if not re.fullmatch(r"\d+GB", value):
            raise ValueError("ram must match pattern like 4GB")
        return value


def validate_instance(payload: dict) -> InstanceSpec:
    return InstanceSpec.model_validate(payload)


def validate_instances_file(path: str | Path) -> tuple[bool, str]:
    config_path = Path(path)
    if not config_path.exists():
        return True, ""

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except json.JSONDecodeError as exc:
        return False, f"{config_path}: invalid JSON at line {exc.lineno}, column {exc.colno} ({exc.msg})"
    except OSError as exc:
        return False, f"{config_path}: cannot read file ({exc})"

    if not isinstance(payload, list):
        return False, f"{config_path}: pydantic validation failed (top-level JSON must be an array)"

    try:
        for idx, item in enumerate(payload, start=1):
            InstanceSpec.model_validate(item)
        return True, ""
    except ValidationError as exc:
        return False, f"{config_path}: pydantic validation failed for item #{idx} ({exc.errors()[0]['msg']})"


__all__ = ["InstanceSpec", "ValidationError", "validate_instance", "validate_instances_file"]
