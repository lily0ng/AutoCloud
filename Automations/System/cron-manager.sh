#!/bin/bash
# Cron Job Manager

set -e

add_cron_job() {
    local schedule=$1
    local command=$2
    
    (crontab -l 2>/dev/null; echo "$schedule $command") | crontab -
    echo "✅ Cron job added: $schedule $command"
}

list_cron_jobs() {
    echo "Current cron jobs:"
    crontab -l
}

remove_cron_job() {
    local pattern=$1
    crontab -l | grep -v "$pattern" | crontab -
    echo "✅ Cron job removed"
}

backup_crontab() {
    local backup_file="/var/backups/crontab_$(date +%Y%m%d).bak"
    crontab -l > "$backup_file"
    echo "✅ Crontab backed up to $backup_file"
}

case "${1:-list}" in
    add)
        add_cron_job "$2" "$3"
        ;;
    list)
        list_cron_jobs
        ;;
    remove)
        remove_cron_job "$2"
        ;;
    backup)
        backup_crontab
        ;;
esac
