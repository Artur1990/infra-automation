# Infra Automation

Stage 1 skeleton for a mock infrastructure provisioning tool.

## Project structure

infra-automation/
|-- scripts/
|-- configs/
|-- logs/
|-- src/
|-- infra_simulator.py
|-- requirements.txt
|-- README.md

## Setup

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```bash
python infra_simulator.py
```

The script will:
- ask for VM definitions
- validate each input
- save valid instances to `configs/instances.json`
- write logs to `logs/provisioning.log`

## Example input format
- name: `web-1`
- os: `Ubuntu` or `CentOS`
- cpu: `2vCPU`
- ram: `4GB`
