from __future__ import annotations

import re

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


__all__ = ["InstanceSpec", "ValidationError", "validate_instance"]
