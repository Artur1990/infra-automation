# src/infra_simulator.py
import argparse
import json
from pathlib import Path

from src.logger import logger
from src.machine import Machine
from src.validator import validate_instance, validate_instances_file


CONFIG_PATH = Path("configs") / "instances.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Provision infrastructure instances")
    parser.add_argument(
        "--instance",
        action="append",
        nargs=4,
        metavar=("NAME", "OS", "CPU", "RAM"),
        required=True,
        help="Instance spec as: NAME OS CPU RAM. Repeat for multiple machines.",
    )
    parser.add_argument(
        "--config",
        default=str(CONFIG_PATH),
        help=f"Output config path (default: {CONFIG_PATH})",
    )
    return parser.parse_args()


def save_instances(instances: list[dict]) -> None:
    CONFIG_PATH.parent.mkdir(exist_ok=True)

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(instances, f, indent=4)

    logger.info(f"Saved {len(instances)} instance(s) to {CONFIG_PATH}")


def main():
    global CONFIG_PATH
    args = parse_args()
    CONFIG_PATH = Path(args.config)

    logger.info("Provisioning started.")

    ok, err = validate_instances_file(CONFIG_PATH)
    if not ok:
        logger.error(f"Invalid config file: {err}")
        print(f"[ERROR] Invalid config file: {err}")
        return

    instances: list[dict] = []

    for index, instance_args in enumerate(args.instance, start=1):
        name, os_name, cpu, ram = instance_args
        data = {"name": name, "os": os_name, "cpu": cpu, "ram": ram}

        ok, err = validate_instance(data)
        if not ok:
            logger.error(f"Invalid --instance #{index}: {err}")
            print(f"[ERROR] Invalid --instance #{index}: {err}")
            return

        machine = Machine(**data)
        machine.log_creation()
        instances.append(machine.to_dict())

    save_instances(instances)
    logger.info("Provisioning ended.")


if __name__ == "__main__":
    main()
