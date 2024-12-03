#--coding:UTF-8--
import requests #api库
import json
import time
from win10toast import ToastNotifier #通知弹窗库
from time import sleep

url_1 = "https://ak.hypergryph.com/standbyherside/api/premeta" #StandByHerSide API（似乎是忘记密码提示？）
url_2 = "https://ak.hypergryph.com/lynchpin/api/meta" #lynchpin API
active = True #初始化状态

while active == True:
    try:
        r = requests.get(url_1) #请求
        responce_1 = r.json() #存储
        r = requests.get(url_2) #请求
        responce_2 = r.json() #存储
        active = False #若请求成功则跳出循环
    except requests.exceptions.ConnectionError as e: #处理网络中断
        print("网络连接中断，正在重试. . .")
        sleep(10)
        continue #重试

number = responce_2["data"]["progress"] #提取百分数
t = time.strftime("%Y-%m-%d",time.localtime()) #请求当前日期

#Windows通知弹窗
toaster = ToastNotifier()
toaster.show_toast("lynchpin",f"{t} 的lynchpin是{number}%\n{responce_1}",duration=10)

#提取上一次请求的日期
with open("latest_date.txt","r",encoding='utf-8') as file:
    date = file.read()

#判断是否已经存储过今日的响应，若是则不写入
if date != t:
    #存储响应结果
    with open("lynchpin.txt","a",encoding='utf-8') as file:
        file.write(f"{t} {number}%\n{responce_2}\n\n")
    
    #覆写今日请求日期
    with open("latest_date.txt","w",encoding='utf-8') as file:
        file.write(f"{t}")
    
    print(f"写入完成：{number}%")
else:
    print(f"今日写入已记录：{number}%")