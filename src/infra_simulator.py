# src/infra_simulator.py
import json
from pathlib import Path

from src.logger import logger
from src.machine import Machine
from src.validator import validate_instance


CONFIG_PATH = Path("configs") / "instances.json"


def prompt_machine() -> dict:
    name = input("Enter machine name (or 'done' to finish): ").strip()
    if name.lower() == "done":
        return {"_done": True}

    os_name = input("Enter OS (Ubuntu/CentOS): ").strip()
    cpu = input("Enter CPU (e.g., 2vCPU): ").strip()
    ram = input("Enter RAM (e.g., 4GB): ").strip()

    return {"name": name, "os": os_name, "cpu": cpu, "ram": ram}


def save_instances(instances: list[dict]) -> None:
    CONFIG_PATH.parent.mkdir(exist_ok=True)

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(instances, f, indent=4)

    logger.info(f"Saved {len(instances)} instance(s) to {CONFIG_PATH}")


def main():
    logger.info("Provisioning started.")

    instances: list[dict] = []

    while True:
        data = prompt_machine()

        if data.get("_done"):
            break

        ok, err = validate_instance(data)
        if not ok:
            logger.error(f"Invalid input: {err}")
            print(f"[ERROR] Invalid input: {err}")
            continue

        machine = Machine(**data)
        machine.log_creation()
        instances.append(machine.to_dict())

    save_instances(instances)
    logger.info("Provisioning ended.")


if __name__ == "__main__":
    main()
