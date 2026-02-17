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
python infra_simulator.py --instance web-1 Ubuntu 2vCPU 4GB
```

The script will:
- read VM definitions from CLI arguments
- validate each input
- save valid instances to `configs/instances.json`
- write logs to `logs/provisioning.log`

Multiple instances:

```bash
python infra_simulator.py \
  --instance web-1 Ubuntu 2vCPU 4GB \
  --instance db-1 CentOS 4vCPU 8GB
```

## Example input format
- name: `web-1`
- os: `Ubuntu` or `CentOS`
- cpu: `2vCPU`
- ram: `4GB`
