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
- prompt for VM definitions interactively
- validate each input
- save valid instances to `configs/instances.json`
- write logs to `logs/provisioning.log`
- optionally run `scripts/setup_nginx.sh` to install/configure Nginx

Run with CLI arguments (optional mode):

```bash
python infra_simulator.py \
  --instance web-1 Ubuntu 2vCPU 4GB \
  --instance db-1 CentOS 4vCPU 8GB
```

Run provisioning + Nginx setup:

```bash
python infra_simulator.py \
  --instance web-1 Ubuntu 2vCPU 4GB \
  --setup-nginx
```

Note: `--setup-nginx` expects a Linux host with `bash` and either `apt-get` or `yum`.

## Example input format
- name: `web-1`
- os: `Ubuntu` or `CentOS`
- cpu: `2vCPU`
- ram: `4GB`
