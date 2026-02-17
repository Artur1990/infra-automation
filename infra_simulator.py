from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.logger import setup_logger
from src.machine import Machine
from src.validators import ValidationError, validate_instance


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mock infrastructure provisioning simulator")
    parser.add_argument(
        "--instance",
        action="append",
        nargs=4,
        metavar=("NAME", "OS", "CPU", "RAM"),
        required=True,
        help="Instance spec as: NAME OS CPU RAM. Repeat flag for multiple instances.",
    )
    parser.add_argument(
        "--output",
        default=str(Path("configs") / "instances.json"),
        help="Output JSON path (default: configs/instances.json)",
    )
    return parser.parse_args()


def collect_machines_from_args(instances_args, logger):
    machines = []

    for index, instance_args in enumerate(instances_args, start=1):
        name, os_name, cpu, ram = instance_args
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
            logger.error("Invalid machine #%s input: %s", index, exc)
            raise ValueError(f"Invalid --instance #{index}: {exc}") from exc

    return machines


def save_instances(machines, target_path: Path, logger) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = [machine.to_dict() for machine in machines]
    target_path.write_text(json.dumps(serialized, indent=4), encoding="utf-8")
    logger.info("Saved %s machine(s) to %s", len(machines), target_path)


def main() -> None:
    args = parse_args()
    logger = setup_logger()
    logger.info("Provisioning simulation started")

    try:
        machines = collect_machines_from_args(args.instance, logger)
        save_instances(machines, Path(args.output), logger)
        logger.info("Provisioning simulation completed")
    except Exception:
        logger.exception("Unexpected error during provisioning simulation")
        raise


if __name__ == "__main__":
    main()
