@echo off
cd /d "C:\Users\ericw\Documents\python\TW_Climate_Forecast"

call ".venv\Scripts\activate.bat"

python GetDataset_HumanStation.py >> "%~dp0GetDataset.log" 2>&1
python GetDataset_NoHumanStation.py >> "%~dp0GetDataset.log" 2>&1

call deactivate
