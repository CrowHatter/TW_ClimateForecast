# DatasetDownload 使用說明

本分支負責自動下載中央氣象署公開的 XML 氣象資料，並儲存至本地資料夾，供後續模型訓練使用。

---

## 快速使用

1. **建立授權設定檔 `config.json`**  
   內容如下，請填入你的授權碼：

   ```json
   {
       "AUTH": "你的授權碼"
   }
   ```

2. **執行下載**

   - 手動下載：
     ```bash
     python GetDataset.py
     ```

   - 自動排程（Windows）使用 `GetDataset.bat` 搭配工作排程器。

---

## 輸出資料位置

成功下載的 XML 檔會存於：

成功下載的 XML 檔會存於：

```text
ClimateDataset/
└── xml/
    ├── O-A0001-001_2024-03-25_08-00.xml
    └── ...
```

---

## 備註

- 已存在檔案會自動略過
- 預設排除資源 ID `O-A0059-001`
- 需先安裝 `requests` 模組

```
pip install requests
```



