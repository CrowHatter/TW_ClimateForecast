#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本程式會自動抓取可取得的氣象 XML 資料：
1. 從 config.json 讀取授權碼 (AUTH)，以避免將授權碼硬編碼在原始碼中。
2. 呼叫 getDataId API 取得資源 ID 列表。
3. 按順序挑選可用的資源 ID，使用 getMetadata API 取得 XML 下載連結。
4. 下載每筆尚未下載的 XML 檔案，存放於 ClimateDataset/xml 資料夾中。

請先確保已安裝 requests 模組 (pip install requests)
"""

import os
import json
import requests

def load_config(config_file="config.json"):
    """從資源檔讀取授權碼"""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"{config_file} 不存在，請建立此檔案以儲存授權碼")
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    if "AUTH" not in config:
        raise KeyError("config.json 中找不到 'AUTH' 鍵")
    return config["AUTH"]

# 從 config.json 中讀取授權碼
AUTH = load_config()

# API URL 基本設定
BASE_ID_URL = f"https://opendata.cwa.gov.tw/historyapi/v1/getDataId/?Authorization={AUTH}"
BASE_METADATA_URL = "https://opendata.cwa.gov.tw/historyapi/v1/getMetadata/{}?Authorization={}"

# XML 資料儲存路徑：ClimateDataset/xml
DATA_FOLDER = os.path.join("ClimateDataset", "xml")
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def get_resource_ids():
    """呼叫 API 取得資源 ID 列表"""
    try:
        resp = requests.get(BASE_ID_URL)
        resp.raise_for_status()
        ids = resp.json()  # 例如 ["O-A0001-001", "O-A0059-001"]
        # 排除"O-A0059-001"
        ids.remove("O-A0059-001")
        return ids
    except Exception as e:
        print("無法取得資源 ID 列表:", e)
        return []

def get_metadata(resource_id):
    """利用指定資源 ID 取得 metadata (包含 XML 下載連結)"""
    url = BASE_METADATA_URL.format(resource_id, AUTH)
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        meta = resp.json()
        if meta.get("dataset", {}).get("success") != "true":
            print(f"資源 {resource_id} metadata 回傳失敗")
            return None
        return meta
    except Exception as e:
        print(f"取得 {resource_id} metadata 失敗:", e)
        return None

def safe_filename(resource_id, datetime_str):
    """
    根據 resource_id 與 DateTime 產生安全檔案名稱，
    將 ":" 與 "+" 等字元替換掉，並以 .xml 為副檔名
    """
    safe_dt = datetime_str.replace("T", "_").replace(":", "-").replace("+", "")
    return f"{resource_id}_{safe_dt}.xml"

def download_xml(url, file_path):
    """從指定 ProductURL 下載 XML 並儲存到 file_path"""
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(resp.content)
        print(f"下載並儲存檔案: {file_path}")
    except Exception as e:
        print(f"下載 {url} 失敗:", e)

def process_resource(resource_id):
    """處理單一資源 ID，抓取 metadata 並下載尚未存在的 XML 檔案"""
    meta = get_metadata(resource_id)
    if not meta:
        return False
    time_list = meta.get("dataset", {}).get("resources", {}).get("resource", {}).get("data", {}).get("time", [])
    if not time_list:
        print(f"資源 {resource_id} 無任何時間資料")
        return False

    for record in time_list:
        date_time = record.get("DateTime")
        product_url = record.get("ProductURL")
        if not date_time or not product_url:
            continue
        filename = safe_filename(resource_id, date_time)
        file_path = os.path.join(DATA_FOLDER, filename)
        if os.path.exists(file_path):
            print(f"檔案 {filename} 已存在，跳過下載")
            continue
        download_xml(product_url, file_path)
    return True

def main():
    resource_ids = get_resource_ids()
    if not resource_ids:
        print("無任何資源 ID 可用")
        return

    for resource_id in resource_ids:
        print(f"處理資源 {resource_id} ...")
        success = process_resource(resource_id)
        if success:
            # 如只處理第一個成功資源，可在此處加上 break
            pass

if __name__ == "__main__":
    main()
