@echo off
REM 切換至專案資料夾
cd /d "C:\Users\ericw\Documents\python\TW_Climate_Forecast"

REM 啟動虛擬環境
call ".venv\Scripts\activate.bat"

REM 執行 Python 腳本
python GetDataset_HumanStation.py

REM
python GetDataset_NoHumanStation.py

REM 可選：停用虛擬環境（若有需要，可加入 deactivate 命令）
deactivate