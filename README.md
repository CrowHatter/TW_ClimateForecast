# DatasetDownload 使用說明

本分支負責下載中央氣象署氣象資料，包含「無人自動站」與「有人觀測站」兩類型，儲存為 XML 或 CSV 檔案供後續模型使用。

---

## 快速使用

1. **建立授權設定檔 `config.json`**

   ```json
   {
       "AUTH": "你的授權碼"
   }
   ```

2. **建立虛擬環境與安裝需求**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install requests
   ```

3. **執行下載**

   - `GetDataset_NoHumanStation.py`：抓取無人自動站 XML 資料
   - `GetDataset_HumanStation.py`：抓取有人觀測站資料並存為 CSV
   - `GetDataset.bat`、`GetDataset.sh`：可排程自動執行上述腳本

---

## 資料儲存結構

```text
ClimateDataset/
├── xml/      ← 無人站 XML 檔案
└── csv/      ← 有人站資料，依縣市分類資料夾，內含月度 CSV
    ├── Taipei/
    │   └── C0A560_202403.csv
    └── Kaohsiung/
        └── C0V350_202403.csv
```

---

## 備註

- XML 資料會自動略過已下載的檔案
- 預設排除 `O-A0059-001`（已知無效 ID）
- 所有 API 連線均需授權碼，請妥善保管 `config.json`
