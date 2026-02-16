from __future__ import annotations

from dataclasses import dataclass

from src.logger import logger


@dataclass(slots=True)
class Machine:
    name: str
    os: str
    cpu: str
    ram: str

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "os": self.os,
            "cpu": self.cpu,
            "ram": self.ram,
        }

    def log_creation(self) -> None:
        logger.info("Provisioning %s: %s, %s, %s", self.name, self.os, self.cpu, self.ram)
