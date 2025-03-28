#!/bin/bash

LOG_PATH="/home/ericweng/Desktop/TW_ClimateForecast/logs/cron_test.log"
echo "$(date) >> cron is working!" >> "$LOG_PATH"

# chmod +x /home/ericweng/Desktop/TW_ClimateForecast/cron_test.sh
# crontab -e
# * * * * * /home/ericweng/Desktop/TW_ClimateForecast/cron_test.sh
