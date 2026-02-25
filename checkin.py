# pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
# https://glados.cloud
import json
import os
import time
import requests
import re
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def str_before_num(s,num):
    if len(s) <= num:
        return s  # 如果字符串长度小于或等于16，返回原字符串

    first_8 = s[:num]  # 获取前8位
    # last_8 = s[-8:]  # 获取后8位
    middle = '*'  # 用一个*代替中间的字符

    return first_8 + middle

def str_after_num(s,num):
    if len(s) <= num:
        return s  # 如果字符串长度小于或等于16，返回原字符串

    # first_8 = s[:num]  # 获取前8位
    last_8 = s[-num:]  # 获取后8位
    # middle = '*'  # 用一个*代替中间的字符

    return last_8

def pad_string_to_num_chars(string,num=24):
    if len(string) == num:
        return string
    elif len(string) < num:
        # return string.ljust(num)
        return string + " " * (num - len(string))
    else:
        return string[:num]

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
    pattern2 = rf'"{keyword}":(.*?)'
    match2 = re.search(pattern2, input_str)

    if match:
        extracted_content = match.group(1)
        # print("提取的内容:", extracted_content)
        return extracted_content
    elif match2:
        extracted_content = match2.group(1)
        # print("提取的内容:", extracted_content)
        return extracted_content
    else:
        print(f"找不到关键字1 '{keyword}'")
        return keyword

def get_account(cookie,authorization):

    # 要查询的 URL
    url = 'https://glados.cloud/api/user/status'

    # 设置 User-Agent
    headers = {
        'Cookie': cookie,
        'Authorization': authorization,
        # 'referer': 'https://glados.cloud/console/checkin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',  # 替换成你自己的 User-Agent 字符串
    }

    # 发送 POST 请求，传递 payload 数据和请求头
    response = requests.get(url,headers=headers,verify=False)

    # 检查响应状态码
    if response.status_code == 200:
        # 处理响应数据
        # 请根据实际情况解析响应数据
        input_str=response.text
        keyword1="email"
        keyword2="leftDays"
        print("==========account==============")
        print(cookie)
        print(response.text)
        account=get_keywords(input_str,keyword1)
        # account = mask_middle_with_asterisks(account)
        # "leftDays":"2.0000000000000000"
        # "leftDays":0
        leftDays=get_keywords(input_str,keyword2)
        if leftDays:
            leftDays=leftDays.split('.')[0]
            leftDays=int(leftDays)
        else:
            leftDays=0
        return account,leftDays

def check_in(cookie,authorization):
    # 要查询的 URL
    url = 'https://glados.cloud/api/user/checkin'
    # url = 'https://glados.cloud/api/user/checkin'
    # url = 'https://glados.cloud/api/user/status'

    payload = {
        "token": "glados.cloud"
        }

    # 设置 User-Agent
    headers = {
        'Cookie': cookie,
        'Authorization': authorization,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',  # 替换成你自己的 User-Agent 字符串
    }
    # 发送 POST 请求，传递 payload 数据和请求头
    # response = requests.post(url,data=payload,headers=headers,verify=False)
    response = requests.post(url, json=payload, headers=headers, verify=False)

    # 检查响应状态码
    if response.status_code == 200:
        # 处理响应数据
        # 请根据实际情况解析响应数据

        print("========================")
        print(cookie)
        print(response.text)
        data = json.loads(response.text)
        if data['list']:
            first_record = data['list'][0]
            # 在这里使用 first_record 进行进一步处理或存储到变量中
            print(first_record)
        else:
            # 如果列表为空，则继续其他操作
            print("List is empty. Continuing...")
        if data['message']:
            message = data['message']
            # 在这里使用 first_record 进行进一步处理或存储到变量中
            print(message)
        else:
            # 如果列表为空，则继续其他操作
            print("message is empty. Continuing...")
        input_str=response.text
        keyword1="message"
        keyword2="business"
        keyword3="balance"

        #积分
        balance=get_keywords(input_str,keyword3)
        if balance == "balance":
            time.sleep(1)
            balance=get_keywords(input_str,keyword3)

        #签到时间
        business=get_keywords(input_str,keyword2)
        message=get_keywords(input_str,keyword1)
        business=business.replace("checkin:","")
        business=business.replace("system:","")
        balance=balance.split('.')[0]
        if balance != "balance":
            balance=int(balance)
        return message,business,balance

def create_file(content,result_filename_csv):
    with open(result_filename_csv, 'a', encoding='utf-8') as file2:
        file2.write(content)
        file2.close()

def test(src_filename,result_filename_csv):
    content="账号,积分,签到,信息,天数\n"
    content_feishu="海外vpn\n"
    num=0
    result_list = []
    with open(src_filename, 'r',encoding='utf-8') as file:
        for line in file:
            # 去除行两端的空白字符，然后检查是否为空白行
            line = line.strip()
            if line and not line.startswith("#"):
                cookie1=line.replace("\n", "").split("###")[1]
                authorization=line.replace("\n", "").split("###")[0]
                message,business,balance=check_in(cookie1,authorization)
                account,leftDays=get_account(cookie1,authorization)
                # content=content+f"{account},{balance},{business},{message}\n"
                # content_feishu=content_feishu+f"{num}、账号: {account},积分: {balance},签到: {business},信息: {message}\n"
                result_list.append({"账号": account, "积分": balance, "签到": business, "信息": message,"天数": leftDays})

    # 按balance字段的值进行排序（假设balance是一个数字）
    # sorted_result = sorted(result_list, key=lambda x: x["积分"], reverse=True)
    sorted_result = result_list
    # 打印排序后的结果
    for entry in sorted_result:
        num=num+1
        num_str = str(num).zfill(2)
        # 账号=pad_string_to_num_chars(str(entry['账号']),num=24)
        # 积分=pad_string_to_num_chars(str(entry['积分'],),num=3)
        # content_feishu=content_feishu+f"{num}、账号: {账号},积分: {积分},签到: {entry['签到']},信息: {entry['信息']},天数: {entry['天数']}\n"
        积分=str(entry['积分']).zfill(2)
        天数=str(entry['天数']).zfill(3)
        信息=str_before_num(entry['信息'],18)
        签到=str_after_num(entry['签到'],10)
        content_feishu=content_feishu+f"{num_str}、积分: {积分}，天数: {天数}，签到: {签到}，信息: {信息}，账号: {entry['账号']}\n"
        content=content+f"{entry['账号']},{entry['积分']},{entry['签到']},{entry['信息']},{entry['天数']}\n"

    print(content_feishu)
    send_message(content_feishu)
    # create_file(content,result_filename_csv)

    # send_message(content,'bcbd3669-fc22-43fd-95eb-4e2e787c3abf')

codepath = os.path.dirname(os.path.abspath(__file__))
#/home/runner/work/AutoStart/AutoStart
print(codepath)
now = datetime.now()
formatted_time = now.strftime("%Y%m%d-%H%M%S")
src_filename=f"{codepath}/cookie2.sh"
#/home/runner/work/AutoStart/AutoStart
result_filename_csv=f"{codepath}/log/{formatted_time}.csv"
test(src_filename,result_filename_csv)
