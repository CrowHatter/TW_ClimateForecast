#!/bin/bash

# 專案路徑
PROJECT_DIR="/home/ericweng/Desktop/TW_ClimateForecast"
LOG_DIR="$PROJECT_DIR/logs"

# 切換進專案
cd "$PROJECT_DIR" || exit 1

# 確保 logs 存在
mkdir -p "$LOG_DIR"

# 加入 debug
echo "$(date) - Running as $(whoami)" >> "$LOG_DIR/cron.log"

# 使用 bash login shell 啟動虛擬環境並執行程式
/usr/bin/bash -c "source $PROJECT_DIR/.venv/bin/activate && python GetDataset_HumanStation.py >> $LOG_DIR/human.log 2>&1 && python GetDataset_NoHumanStation.py >> $LOG_DIR/nohuman.log 2>&1"

# chmod +x {.sh file path}
# 15 * * * * /home/ericweng/Desktop/TW_ClimateForecast/GetDataset.sh >> /home/ericweng/Desktop/TW_ClimateForecast/logs/cron.log 2>&1
