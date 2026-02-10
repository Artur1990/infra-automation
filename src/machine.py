# src/machine.py
from dataclasses import dataclass
from src.logger import logger


@dataclass
class Machine:
    name: str
    os: str
    cpu: str
    ram: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "os": self.os,
            "cpu": self.cpu,
            "ram": self.ram,
        }

    def log_creation(self) -> None:
        logger.info(f"Provisioning {self.name}: {self.os}, {self.cpu}, {self.ram}")
