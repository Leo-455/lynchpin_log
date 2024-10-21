#--coding:UTF-8--
import requests #api库
import json
import time
from plyer import notification #通知弹窗库
from time import sleep

url = "https://ak.hypergryph.com/lynchpin/api/meta" #lynchpin URL
active = True #初始化状态

while active == True:
    try:
        r = requests.get(url) #请求
        responce = r.json() #存储
        active = False #若请求成功则跳出循环
    except requests.exceptions.ConnectionError as e: #处理网络中断
        print("网络连接中断，正在重试. . .")
        sleep(10)
        continue #重试

number = responce["data"]["progress"] #提取百分数
t = time.strftime("%Y-%m-%d",time.localtime()) #请求当前日期

#Windows通知弹窗
notification.notify(
    title = "lynchpin",
    message = f"{t} 的lynchpin是{number}%"
    )

#提取上一次请求的日期
with open("D:\\programing\\python\\pv4\\latest_date.txt","r",encoding='utf-8') as file:
    date = file.read()

#判断是否已经存储过今日的响应，若是则不写入
if date != t:
    #存储响应结果
    with open("D:\\programing\\python\\pv4\\lynchpin.txt","a",encoding='utf-8') as file:
        file.write(f"{t} {number}%\n{responce}\n\n")
    
    #覆写今日请求日期
    with open("D:\\programing\\python\\pv4\\latest_date.txt","w",encoding='utf-8') as file:
        file.write(f"{t}")
    
    print(f"写入完成：{number}%")
else:
    print(f"今日写入已记录：{number}%")