#!/bin/bash

# 設定你的專案路徑
PROJECT_DIR="/home/ericweng/Desktop/TW_ClimateForecast"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"
LOG_DIR="$PROJECT_DIR/logs"

# 確保 logs 資料夾存在
mkdir -p "$LOG_DIR"

# 使用虛擬環境中的 Python 執行兩個腳本，並將輸出記錄到 log
"$VENV_PYTHON" "$PROJECT_DIR/GetDataset_HumanStation.py" >> "$LOG_DIR/human.log" 2>&1
"$VENV_PYTHON" "$PROJECT_DIR/GetDataset_NoHumanStation.py" >> "$LOG_DIR/nohuman.log" 2>&1

# crontab -e
# 15 * * * * /home/ericweng/Desktop/TW_ClimateForecast/GetDataset.sh >> /home/ericweng/Desktop/TW_ClimateForecast/logs/cron.log 2>&1
