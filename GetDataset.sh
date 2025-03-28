#!/bin/bash

# 設定你的專案目錄
PROJECT_DIR="/home/ericweng/Desktop/TW_ClimateForecast"  # ← 這裡改成你的實際目錄

# 進入專案目錄
cd "$PROJECT_DIR" || exit

# 啟用虛擬環境
source .venv/bin/activate

# 執行腳本並將輸出記錄到 log（可省略 >> 部分不記 log）
python GetDataset_HumanStation.py >> logs/human.log 2>&1
python GetDataset_NoHumanStation.py >> logs/nohuman.log 2>&1

# 離開虛擬環境
deactivate

# crontab -e
# 15 * * * * /home/ericweng/Desktop/TW_ClimateForecast/run_weather_scripts.sh