#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DatasetDeleteByDateTime.py

此程式允許使用者持續輸入日期時間關鍵字 (例如：2025-03-26T21:10)
直到按下 Ctrl+C 結束程式。
程式會遞迴搜尋 "ClimateDataset/csv" 資料夾（含各 County 子資料夾）中的所有 CSV 檔案，
將每筆記錄中 DateTime 欄位包含該關鍵字的資料刪除，
若該 CSV 檔案刪除後無任何記錄，則連同檔案一起刪除。
"""

import os
import csv

def delete_records_by_datetime(search_str, base_folder="ClimateDataset/csv"):
    total_files_processed = 0
    total_rows_removed = 0
    total_files_deleted = 0

    # 遞迴處理所有 CSV 檔案
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".csv"):
                csv_path = os.path.join(root, file)
                total_files_processed += 1
                try:
                    with open(csv_path, "r", newline="", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        rows = list(reader)
                        if not rows or not reader.fieldnames:
                            continue
                        fieldnames = reader.fieldnames
                except Exception as e:
                    print(f"讀取 {csv_path} 發生錯誤: {e}")
                    continue

                # 篩選出不含關鍵字的記錄
                new_rows = [row for row in rows if search_str not in row.get("DateTime", "")]
                removed_count = len(rows) - len(new_rows)
                total_rows_removed += removed_count

                if removed_count > 0:
                    if new_rows:
                        try:
                            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                                writer = csv.DictWriter(f, fieldnames=fieldnames)
                                writer.writeheader()
                                writer.writerows(new_rows)
                            print(f"更新 {csv_path}，移除 {removed_count} 筆記錄")
                        except Exception as e:
                            print(f"寫入 {csv_path} 時發生錯誤: {e}")
                    else:
                        try:
                            os.remove(csv_path)
                            total_files_deleted += 1
                            print(f"刪除 {csv_path}，所有記錄皆被移除")
                        except Exception as e:
                            print(f"刪除 {csv_path} 時發生錯誤: {e}")
    print(f"\n完成：處理 {total_files_processed} 個檔案，移除 {total_rows_removed} 筆記錄，刪除 {total_files_deleted} 個檔案\n")

def main():
    print("請持續輸入要刪除的日期時間關鍵字 (例如：2025-03-26T21:10)，按 Ctrl+C 結束：")
    try:
        while True:
            # 讀取使用者輸入（每行一個關鍵字）
            search_str = input().strip()
            if not search_str:
                continue  # 忽略空行
            delete_records_by_datetime(search_str)
    except KeyboardInterrupt:
        print("\n偵測到 Ctrl+C，程式結束。")

if __name__ == "__main__":
    main()
