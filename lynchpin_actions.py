# --coding:UTF-8--
import json
import time
import sys

import requests

url = "https://ak.hypergryph.com/lynchpin/api/meta"  # lynchpin API
success = False

for i in range(5):
    try:
        print(f"进行第{i}次请求. . .")
        r = requests.get(url, timeout=30)
        responce = r.json()
        print("请求成功")
        success = True
        break
    except requests.exceptions.ConnectionError:
        time.sleep(5)
        print("网络连接中断，正在重试. . .")

if success is False:
    print("请求失败")
    sys.exit(1)

number = responce["data"]["progress"]  # 提取百分数

utc_time = time.time()
bjt = time.gmtime(utc_time + 8 * 3600)
t = time.strftime("%Y-%m-%d", bjt)

# 提取上一次请求的日期
with open("lynchpin.json", 'r', encoding='utf-8') as f:
    json_data = json.load(f)
    date = json_data["update_time"]

# 判断是否已经存储过今日的响应，若是则不写入
if date != t:
    json_data["update_time"] = t
    json_data["data"][f"{t}"] = {"progress": number, "original_msg": responce}
    with open("lynchpin.json", 'w', encoding='utf-8') as file:
        json.dump(json_data, file)

    print(f"写入完成：{number}%")
else:
    print(f"今日写入已记录过：{number}%")
    sys.exit(0)
