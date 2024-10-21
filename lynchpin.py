#--coding:UTF-8--
import requests #api库
import json
import time
from plyer import notification #通知弹窗库
from time import sleep

url = "https://ak.hypergryph.com/lynchpin/api/meta"
r = requests.get(url)
responce = r.json()
number = responce["data"]["progress"]

t = time.strftime("%Y-%m-%d",time.localtime())

print (number)
#Windows通知弹窗
notification.notify(
    title = "lynchpin",
    message = f"{t} 的lynchpin是{number}%"
    )

with open("D:\\programing\\python\\pv4\\lynchpin.txt","a",encoding='utf-8') as file:
    file.write(f"{t} {number}%\n")