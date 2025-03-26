#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本程式會呼叫 O-A0003-001 API 取得氣象資料，
資料來源依據 config.json 中的授權碼 (AUTH)。
取得之資料會依據 GeoInfo 中的 CountyName 建立資料夾，
並依據 StationId 與 ObsTime 的月份 (格式 YYYYMM) 生成 CSV 檔案，
CSV 檔案內包含欄位：StationName、StationId、DateTime、Weather、VisibilityDescription、
SunshineDuration、WindDirection、WindSpeed、AirTemperature、RelativeHumidity、AirPressure、UVIndex。
"""

import os
import json
import csv
import requests
from datetime import datetime

def load_config(config_file="config.json"):
    """從 config.json 讀取授權碼"""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"{config_file} 不存在，請建立此檔案以儲存授權碼")
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    if "AUTH" not in config:
        raise KeyError("config.json 中找不到 'AUTH' 鍵")
    return config["AUTH"]

def fetch_weather_data(auth):
    """呼叫 O-A0003-001 API 取得氣象資料"""
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization={auth}"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        if data.get("success") != "true":
            print("API 回傳失敗")
            return None
        return data
    except Exception as e:
        print("取得 API 資料失敗:", e)
        return None

def ensure_folder(path):
    """若資料夾不存在則建立"""
    if not os.path.exists(path):
        os.makedirs(path)

def process_records(data):
    """處理 API 資料中的各筆 Station 資料，並依據 CountyName 與 StationId 儲存至 CSV"""
    records = data.get("records", {}).get("Station", [])
    if not records:
        print("無氣象資料可供處理")
        return

    # 欲儲存之欄位
    fieldnames = [
        "StationName", "StationId", "DateTime", "Weather",
        "VisibilityDescription", "SunshineDuration", "WindDirection",
        "WindSpeed", "AirTemperature", "RelativeHumidity", "AirPressure", "UVIndex"
    ]
    
    base_folder = os.path.join("ClimateDataset", "csv")
    ensure_folder(base_folder)

    for rec in records:
        try:
            station_name = rec.get("StationName", "")
            station_id = rec.get("StationId", "")
            obs_time_str = rec.get("ObsTime", {}).get("DateTime", "")
            if not obs_time_str:
                print(f"缺少 ObsTime 資料，跳過 {station_id}")
                continue

            # 解析日期並取得月份 (格式: YYYYMM)
            dt = datetime.strptime(obs_time_str, "%Y-%m-%dT%H:%M:%S%z")
            month_key = dt.strftime("%Y%m")
            
            # 取得氣象資料欄位
            weather_elem = rec.get("WeatherElement", {})
            weather = weather_elem.get("Weather", "")
            visibility = weather_elem.get("VisibilityDescription", "")
            sunshine = weather_elem.get("SunshineDuration", "")
            wind_dir = weather_elem.get("WindDirection", "")
            wind_speed = weather_elem.get("WindSpeed", "")
            air_temp = weather_elem.get("AirTemperature", "")
            rel_humidity = weather_elem.get("RelativeHumidity", "")
            air_pressure = weather_elem.get("AirPressure", "")
            uv_index = weather_elem.get("UVIndex", "")
            
            # 依據 CountyName 建立資料夾
            county = rec.get("GeoInfo", {}).get("CountyName", "Unknown")
            county_folder = os.path.join(base_folder, county)
            ensure_folder(county_folder)
            
            # CSV 檔名: StationId_{month_key}.csv
            csv_filename = f"{station_id}_{month_key}.csv"
            csv_path = os.path.join(county_folder, csv_filename)
            
            # 檢查檔案是否存在，以決定是否需寫入 header
            file_exists = os.path.exists(csv_path)
            with open(csv_path, "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow({
                    "StationName": station_name,
                    "StationId": station_id,
                    "DateTime": obs_time_str,
                    "Weather": weather,
                    "VisibilityDescription": visibility,
                    "SunshineDuration": sunshine,
                    "WindDirection": wind_dir,
                    "WindSpeed": wind_speed,
                    "AirTemperature": air_temp,
                    "RelativeHumidity": rel_humidity,
                    "AirPressure": air_pressure,
                    "UVIndex": uv_index
                })
            print(f"儲存 {csv_path}")
        except Exception as e:
            print(f"處理 StationId {rec.get('StationId', '')} 時發生錯誤:", e)

def main():
    try:
        auth = load_config()
    except Exception as e:
        print("讀取 config.json 發生錯誤:", e)
        return

    data = fetch_weather_data(auth)
    if data is None:
        print("無法取得氣象資料")
        return

    process_records(data)

if __name__ == "__main__":
    main()
