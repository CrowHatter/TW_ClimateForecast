# LSTM氣象預測專題

本專題旨在使用深度學習技術中的長短期記憶模型（LSTM）來進行天氣資料的預測。透過資料前處理、模型訓練與評估，建立一個能夠預測未來氣象變化的系統，期望提升氣象預測的準確度與應用價值。

---

## 專題目標

- 蒐集並處理氣象時間序列資料
- 建立並訓練基於 LSTM 的預測模型
- 預測目標可包括(暫定)：溫度、濕度、降雨機率等關鍵氣象指標
- 評估模型預測結果之準確性
- 架設簡易 GUI 介面展示預測結果（如進度允許）
- 根據新進資料動套更新模型（如進度允許）

---

## 專案流程

### 1. 資料前處理
- 使用氣象資料開放平台與他人先前紀錄之資料
  - https://opendata.cwa.gov.tw/dataset/observation/O-A0001-001 (自動氣象站資料-無人自動站氣象資料)
  - https://opendata.cwa.gov.tw/dataset/observation/O-A0003-001 (現在天氣觀測報告-有人氣象站資料)
  - https://github.com/Raingel/historical_weather (臺灣歷史氣象觀測資料庫)
- 處理缺失值與異常值
- 將非數值欄位轉換為數值型態
- 進行 Z-score 正規化
- 轉換為適合 LSTM 的時間序列格式

### 2. 模型訓練
- 使用 PyTorch 架構並以 CUDA 加速訓練 LSTM 模型
- 輸入為過去數天的氣象資料
- 輸出為各縣市下一時間點的氣溫曲線或降雨機率
- 模型可儲存為 `.pt` 或 `.joblib`

### 3. 模型預測與評估
- 匯入測試集進行預測
- 使用 MAE、RMSE、R² 等指標評估準確度
- 比較不同模型（如傳統迴歸、GRU等）

### 4. 視覺化與展示
- 使用 Matplotlib、Seaborn 畫出實際與預測結果
- 整合 GUI 介面展示（預計使用Flask簡單展示）

---

## 使用技術

- Python 3.x
- PyTorch + CUDA
- NumPy / Pandas
- Scikit-learn
- Matplotlib / Seaborn
- Jupyter Notebook
- Flask

---

## 專題進度（截至目前）

- [x] 完成資料收集(自動氣象站資料-無人自動站氣象資料)
- [x] 完成資料收集(現在天氣觀測報告-有人氣象站資料)
- [ ] 資料清洗
- [ ] 資料正規化（Z-score）與時間序列轉換
- [ ] 使用 PyTorch 架設初步 LSTM 模型
- [ ] 優化模型架構與參數調整
- [ ] 預測結果評估與視覺化
- [ ] GUI整合與預測輸出展示

---

## 未來展望

- 支援多變數輸入與多步預測
- 整合氣象開放資料API，實現即時資料預測與展示

---
## 引用資料
Ou, J.-H., Kuo, C.-H., Wu, Y.-F., Lin, G.-C., Lee, M.-H., Chen, R.-K., Chou, H.-P., Wu, H.-Y., Chu, S.-C., Lai, Q.-J., Tsai, Y.-C., Lin, C.-C., Kuo, C.-C., Liao, C.-T., Chen, Y.-N., Chu, Y.-W., Chen, C.-Y., 2023. Application-oriented deep learning model for early warning of rice blast in Taiwan. Ecological Informatics 73, 101950. https://doi.org/10.1016/j.ecoinf.2022.101950
