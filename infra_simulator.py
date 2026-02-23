from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from src.logger import setup_logger
from src.machine import Machine
from src.validators import ValidationError, validate_instance, validate_instances_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mock infrastructure provisioning simulator")
    parser.add_argument(
        "--instance",
        action="append",
        nargs=4,
        metavar=("NAME", "OS", "CPU", "RAM"),
        help="Instance spec as: NAME OS CPU RAM. Repeat flag for multiple instances.",
    )
    parser.add_argument(
        "--output",
        default=str(Path("configs") / "instances.json"),
        help="Output JSON path (default: configs/instances.json)",
    )
    parser.add_argument(
        "--setup-nginx",
        action="store_true",
        help="Run scripts/setup_nginx.sh after provisioning",
    )
    parser.add_argument(
        "--setup-script",
        default=str(Path("scripts") / "setup_nginx.sh"),
        help="Path to setup script (default: scripts/setup_nginx.sh)",
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


def prompt_instances(logger):
    machines = []
    logger.info("Interactive mode enabled")

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
            logger.error("Invalid interactive input: %s", exc)
            print(f"[ERROR] Invalid input: {exc}")

    return machines


def save_instances(machines, target_path: Path, logger) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = [machine.to_dict() for machine in machines]
    target_path.write_text(json.dumps(serialized, indent=4), encoding="utf-8")
    logger.info("Saved %s machine(s) to %s", len(machines), target_path)


def run_setup_script(script_path: Path, logger) -> None:
    logger.info("Running setup script: %s", script_path)
    if not script_path.exists():
        raise FileNotFoundError(f"Setup script not found: {script_path}")

    try:
        result = subprocess.run(
            ["bash", str(script_path)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        if exc.stdout:
            for line in exc.stdout.splitlines():
                logger.error("[setup_nginx] %s", line)
        if exc.stderr:
            for line in exc.stderr.splitlines():
                logger.error("[setup_nginx] %s", line)
        raise RuntimeError(f"Setup script failed with exit code {exc.returncode}") from exc

    if result.stdout:
        for line in result.stdout.splitlines():
            logger.info("[setup_nginx] %s", line)
    if result.stderr:
        for line in result.stderr.splitlines():
            logger.warning("[setup_nginx] %s", line)


def main() -> None:
    args = parse_args()
    logger = setup_logger()
    logger.info("Provisioning simulation started")

    try:
        ok, err = validate_instances_file(args.output)
        if not ok:
            logger.error("Invalid output config file: %s", err)
            raise ValueError(f"Invalid output config file: {err}")

        if args.instance:
            machines = collect_machines_from_args(args.instance, logger)
        else:
            machines = prompt_instances(logger)
        save_instances(machines, Path(args.output), logger)
        if args.setup_nginx:
            run_setup_script(Path(args.setup_script), logger)
        logger.info("Provisioning simulation completed")
    except Exception:
        logger.exception("Unexpected error during provisioning simulation")
        raise


if __name__ == "__main__":
    main()
