from __future__ import annotations

import json
from pathlib import Path

from src.logger import setup_logger
from src.machine import Machine
from src.validators import ValidationError, validate_instance


def collect_machines(logger):
    machines = []

    while True:
        name = input("Enter machine name (or 'done' to finish): ").strip()
        if name.lower() == "done":
            break

        os_name = input("Enter OS (Ubuntu/CentOS): ").strip()
        cpu = input("Enter CPU (e.g., 2vCPU): ").strip()
        ram = input("Enter RAM (e.g., 4GB): ").strip()

        payload = {"name": name, "os": os_name, "cpu": cpu, "ram": ram}

        try:
            validated = validate_instance(payload)
            machine = Machine(
                name=validated.name,
                os=validated.os,
                cpu=validated.cpu,
                ram=validated.ram,
            )
            machines.append(machine)
            logger.info("Machine accepted: %s", machine.name)
        except ValidationError as exc:
            logger.error("Invalid machine input: %s", exc)
            print("Invalid input. Please try again.")

    return machines


def save_instances(machines, target_path: Path, logger) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = [machine.to_dict() for machine in machines]
    target_path.write_text(json.dumps(serialized, indent=4), encoding="utf-8")
    logger.info("Saved %s machine(s) to %s", len(machines), target_path)


def main() -> None:
    logger = setup_logger()
    logger.info("Provisioning simulation started")

    try:
        machines = collect_machines(logger)
        save_instances(machines, Path("configs") / "instances.json", logger)
        logger.info("Provisioning simulation completed")
    except Exception:
        logger.exception("Unexpected error during provisioning simulation")
        raise


if __name__ == "__main__":
    main()
