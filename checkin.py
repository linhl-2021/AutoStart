import json
import os
import requests
import re
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def send_message(msg,key='3ea705e6-4932-4978-8faf-e0a3510ae013'):
    data = {
        "msg_type": "text",
        "content": {"text": msg}
    }
    headers = {'Content-Type': 'application/json'}
    send_url=f"https://open.feishu.cn/open-apis/bot/v2/hook/{key}"
    print("飞书url： "+send_url)
    response = requests.post(send_url, headers=headers, data=json.dumps(data))
    print(response.json())
    return response.json()

def send_file(file_url,key):
    data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "content": [
                        [
                            {
                                "tag": "a",
                                "text": "请查看测试报告",
                                "href": file_url
                            },
                            {
                                "tag": "at",
                                "user_id": "all"
                            }
                        ]
                    ]
                }
            }
        }
    }
    headers = {'Content-Type': 'application/json'}
    send_url=f"https://open.feishu.cn/open-apis/bot/v2/hook/{key}"
    response = requests.post(send_url, headers=headers, data=json.dumps(data))
    return response.json()

def get_keywords(input_str,keyword):
    # 使用正则表达式查找关键字后面的内容
    pattern = rf'"{keyword}":"(.*?)"'
    match = re.search(pattern, input_str)

    if match:
        extracted_content = match.group(1)
        # print("提取的内容:", extracted_content)
        return extracted_content
    else:
        print(f"找不到关键字 '{keyword}'")

def get_account(cookie):

    # 要查询的 URL
    url = 'https://glados.rocks/api/user/status'

    # 设置 User-Agent
    headers = {
        'Cookie': cookie,
        # 'referer': 'https://glados.rocks/console/checkin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',  # 替换成你自己的 User-Agent 字符串
    }

    # 发送 POST 请求，传递 payload 数据和请求头
    response = requests.get(url,headers=headers,verify=False)

    # 检查响应状态码
    if response.status_code == 200:
        # 处理响应数据
        # 请根据实际情况解析响应数据
        # print(response.text)
        input_str=response.text
        keyword1="email"
        account=get_keywords(input_str,keyword1)
        return account

def check_in(cookie):
    # 要查询的 URL
    url = 'https://glados.rocks/api/user/checkin'
    # url = 'https://glados.rocks/api/user/status'

    payload = {
        "token": "glados.one"
        }

    # 设置 User-Agent
    headers = {
        'Cookie': cookie,
        # 'referer': 'https://glados.rocks/console/checkin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',  # 替换成你自己的 User-Agent 字符串
    }

    # 发送 POST 请求，传递 payload 数据和请求头
    response = requests.post(url,data=payload,headers=headers,verify=False)

    # 检查响应状态码
    if response.status_code == 200:
        # 处理响应数据
        # 请根据实际情况解析响应数据
        # print(response.text)
        input_str=response.text
        keyword1="message"
        keyword2="business"
        keyword3="balance"

        #积分
        balance=get_keywords(input_str,keyword3)
        #签到时间
        business=get_keywords(input_str,keyword2)
        message=get_keywords(input_str,keyword1)
        business=business.replace("checkin:","")
        business=business.replace("system:","")
        balance=balance.split('.')[0]
        return message,business,balance

def test(src_filename,result_filename_csv):
    content="账号,积分,签到,信息\n"
    # with open(result_filename_csv, 'w', encoding='utf-8') as file1:
    #         file1.write("账号,积分,签到,信息"+"\n")
    #         file1.close()
    # 打开文件并逐行读取域名
    with open(src_filename, 'r',encoding='utf-8') as file:
        for line in file:
            # 去除行两端的空白字符，然后检查是否为空白行
            line = line.strip()
            if line and not line.startswith("#"):
                cookie1=line.replace("\n", "")
                account=get_account(cookie1)
                message,business,balance=check_in(cookie1)
                content=content+f"{account},{balance},{business},{message}\n"

    print(content) 
    send_message(content)
    # send_message(content,'bcbd3669-fc22-43fd-95eb-4e2e787c3abf')
    with open(result_filename_csv, 'a', encoding='utf-8') as file2:
        file2.write(content)
        file2.close()

codepath = os.path.dirname(os.path.abspath(__file__))
#/home/runner/work/AutoStart/AutoStart
print(codepath)
now = datetime.now()
formatted_time = now.strftime("%Y%m%d%H%M%S")
src_filename=f"{codepath}/cookie.txt"
#/home/runner/work/AutoStart/AutoStart
result_filename_csv=f"{codepath}/log/{formatted_time}.csv"
test(src_filename,result_filename_csv)
