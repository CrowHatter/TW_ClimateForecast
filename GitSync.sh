#!/bin/bash

# 專案路徑
PROJECT_DIR="/home/ericweng/Desktop/TW_ClimateForecast/"

cd "$PROJECT_DIR" || exit 1

# 更新專案
git pull

# 加入變動（你可用 git status 來預先檢查）
git add .

# 自動提交（可加上日期訊息）
git commit -m "Auto commit on $(date '+%Y-%m-%d %H:%M:%S')"

# 推送到 GitHub
git push

# modify http to ssh
# git remote set-url origin git@github.com:CrowHatter/TW_ClimateForecast.git

# crontab -e
# chmod +x /home/ericweng/Desktop/TW_ClimateForecast/GitSync.sh
# 30 15 * * * /home/ericweng/Desktop/TW_ClimateForecast/GitSync.sh >> /home/ericweng/Desktop/TW_ClimateForecast/logs/git_sync.log 2>&1

