#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="${LOG_FILE:-logs/provisioning.log}"

log() {
  local level="$1"
  local msg="$2"
  local ts
  ts="$(date '+%Y-%m-%d %H:%M:%S')"
  echo "${ts} - ${level} - ${msg}" | tee -a "$LOG_FILE"
}

run_cmd() {
  if command -v sudo >/dev/null 2>&1; then
    sudo "$@"
  else
    "$@"
  fi
}

install_with_apt() {
  log "INFO" "Using apt package manager"
  run_cmd apt-get update -y
  run_cmd apt-get install -y nginx
}

install_with_yum() {
  log "INFO" "Using yum package manager"
  run_cmd yum install -y epel-release
  run_cmd yum install -y nginx
}

main() {
  mkdir -p "$(dirname "$LOG_FILE")"
  log "INFO" "Nginx setup script started"

  if command -v nginx >/dev/null 2>&1; then
    log "INFO" "Nginx is already installed"
  else
    if command -v apt-get >/dev/null 2>&1; then
      install_with_apt
    elif command -v yum >/dev/null 2>&1; then
      install_with_yum
    else
      log "ERROR" "No supported package manager found (apt-get/yum)"
      exit 1
    fi
  fi

  if command -v systemctl >/dev/null 2>&1; then
    run_cmd systemctl enable --now nginx
    log "INFO" "Nginx service enabled and started"
  else
    log "ERROR" "systemctl is not available; cannot manage nginx service"
    exit 1
  fi

  log "INFO" "Nginx setup script completed successfully"
}

main "$@"
