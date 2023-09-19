import json
import os
import re
import requests
import sys
import demo
import difflib
from bs4 import BeautifulSoup

def getappdate1(date,username,passworde):
    ntos_page = date
    login_api = f"{ntos_page}/api/v1/login/"
    res=demo.login_web(login_api,ntos_page,username,passworde)
    sessionid=res["session_id"]
    csrftoken=res["csrftoken"]
    cookie = f"LOCAL_LANG_i18n=en;csrftoken={csrftoken};sessionid={sessionid}"
    url = f"{ntos_page}/api/v1/application/"
    headers = {
    "cookie": cookie,
}
    response =  requests.get(url,headers=headers,verify=False)

    # print(response.text)
    str1=json.loads(response.text)
    # print(type(str1))
    list1=str1["data"]["list"]
    return list1


def has_chinese(string):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    match = pattern.search(string)
    return match is not None

def check_app_name_online(app_name):
    url = f'https://www.baidu.com/s?wd={app_name}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    h3_list = soup.find_all('h3')
    for h3 in h3_list:
        print(h3.text)  # 输出H3标签的文本内容

def check_app_name(date="https://10.51.212.212",username="admin",passworde="Ruijie@123"):
    codepath = os.path.dirname(os.path.abspath(__file__))
    path=os.path.join(codepath, "file/")
    fielname=path+"10.51.212.212-en"
    print("检测应用名规范性")
    list1=getappdate1(date,username,passworde)
    for first_list in list1:
        for sec_list in first_list["sub_class_list"]:
            if not sec_list["app_list"]:
                print(f"{sec_list['desc_name']}不存在3级菜单")
                print(f"检测{sec_list['desc_name']}规范性")
            else:
                for third_list in sec_list["app_list"]:
                    # print("1级："+first_list["desc_name"]+"==2级： "+sec_list["desc_name"]+"==3级： "+third_list["desc_name"])
                    print(f"检测{third_list['desc_name']}规范性")

def compare_file(filename,language,level):
    # print("开始对比")
    codepath = os.path.dirname(os.path.abspath(__file__))
    path=os.path.join(codepath, "file/")
    with open(f'{path}standard-{language}-{level}级.txt', 'r',encoding='utf-8') as file1:
        file1_lines = file1.readlines()
    # 读取第二个文件
    with open(f'{filename}-{level}级.txt', 'r',encoding='utf-8') as file2:
        file2_lines = file2.readlines()
    differ = difflib.Differ()
    diff = list(differ.compare(file1_lines, file2_lines))
    flag=True
    app=""
    for line in diff:
        if line.startswith('+'):
            # print(f'{language}：【新增】{line[1:].strip()}\r\n')
            app=app+f'{language}：【新增】{line[1:].strip()}'+"\r\n"
            flag=False
        elif line.startswith('-'):
            flag=False
            app=app+f'{language}：【删除】{line[1:].strip()}'+"\r\n"
            # print(f'{language}：【删除】{line[1:].strip()}\r\n')
        elif line.startswith('?'):
            pass   # 忽略差异行中的无关符号
        else:
            pass   # 两文件相同行，不进行处理
    if flag:
        return f"应用名无变动"+"\r\n"
    else:
        return  app


def getappdate(date,language,username,password):
    app1_1=""
    app2_1=""
    app3_1=""
    ntos_page = date
    login_api = f"{ntos_page}/api/v1/login/"
    # res=demo.login_web(login_api,ntos_page,username,password)
    res=demo.login_web(login_api,ntos_page)
    sessionid=res["session_id"]
    csrftoken=res["csrftoken"]
    cookie = f"LOCAL_LANG_i18n={language};csrftoken={csrftoken};sessionid={sessionid}"
    url = f"{ntos_page}/api/v1/application/"
    headers = {
    "cookie": cookie,
}
    response =  requests.get(url,headers=headers,verify=False)

    # print(response.text)
    str1=json.loads(response.text)
    list1=str1["data"]["list"]
    codepath = os.path.dirname(os.path.abspath(__file__))
    path=os.path.join(codepath, "file/")
    fielname=path+ntos_page.split("//")[1]+"-"+language
    # fielname="standard"+"-"+language
    with open(f'{fielname}-1级.txt', 'w', encoding='utf-8') as file1:
        file1.write("1级"+"\n")
        file1.close()
    with open(f'{fielname}-2级.txt', 'w', encoding='utf-8') as file2:
        file2.write("2级"+"\n")
        file2.close()
    with open(f'{fielname}-3级.txt', 'w', encoding='utf-8') as file3:
        file3.write("3级"+"\n")
        file3.close()
    # my_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for first_list in list1:
        # print(first_list["desc_name"])
        # print("1级："+first_list["desc_name"])
        if(has_chinese(first_list["desc_name"])):
            app1_1=app1_1+"存在中文: "+first_list["desc_name"]+"\r\n"
        with open(f'{fielname}-1级.txt', 'a', encoding='utf-8') as file1:
            file1.write("1级："+first_list["desc_name"]+"\n")
            file1.close()
        for sec_list in first_list["sub_class_list"]:
            if(has_chinese(sec_list["desc_name"])):
                app2_1=app2_1+"存在中文: "+sec_list["desc_name"]+"\r\n"
            with open(f'{fielname}-2级.txt', 'a', encoding='utf-8') as file2:
                file2.write("2级： "+sec_list["desc_name"]+"\n")
                file2.close()
            for third_list in sec_list["app_list"]:
                if(has_chinese(third_list["desc_name"])):
                    app3_1=app3_1+"存在中文: "+third_list["desc_name"]+"\r\n"
                with open(f'{fielname}-3级.txt', 'a', encoding='utf-8') as file3:
                    file3.write("3级： "+third_list["desc_name"]+"\n")
                    file3.close()
    if app1_1 == "":
        app1_1="不存在中文"
    if app2_1 == "":
        app2_1="不存在中文"
    if app2_1 == "":
        app2_1="不存在中文"

    app1=compare_file(fielname,language,1)
    app2=compare_file(fielname,language,2)
    app3=compare_file(fielname,language,3)
    print(f'一级菜单：\r\t{app1}\r\t{app1_1}\r二级菜单：\r\t{app2}\r\t{app2_1}\r三级菜单：\r\t{app3}\r\t{app3_1}')



if __name__ == "__main__":
    # codepath = os.path.dirname(os.path.abspath(__file__))
    # path=os.path.join(codepath, "file/")
    # fielname=path+"10.51.212.212-en"
    # getappdate("https://10.51.212.212","en","admin","Ruijie@123")
    check_app_name(date="https://10.51.212.30",username="admin",passworde="ruijie@123")
    # getappdate("https://10.51.212.212","en","admin","Ruijie@123")
#     # getappdate("https://10.51.212.212","ch","admin","Ruijie@123")
#     compare_file("10.51.212.212","en",1)
#     compare_file("10.51.212.212","en",2)
#     compare_file("10.51.212.212","en",3)
#     compare_file("10.51.212.212","ch",1)
#     compare_file("10.51.212.212","ch",2)
#     compare_file("10.51.212.212","ch",3)
