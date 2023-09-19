import json
import re
import requests
import sys
sys.path.append(r'D:\\工作\\20230220应用识别用例\\应用识别工具\\')
import demo

def has_chinese(string):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    match = pattern.search(string)
    return match is not None

def getpublickey(url):
    publickey =  requests.get(url,verify=False)
    str1=publickey.text
    response_dict = json.loads(str1)
    # print(type(response_dict))
    # print(response_dict["data"])
    response_dict2=response_dict["data"]
    # print(type(response_dict2))
    # print(response_dict2["details"])
    return response_dict2["details"]

#对象配置--应用
def getappdate(date,username,passworde):
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
    # print(type(list1))
    # print(list1[0]["desc_name"])

    list2=list1[0]["sub_class_list"]
    # print(type(list2))
    # print(list2[0]["desc_name"])

    list3=list2[0]["app_list"]
    # print(type(list3))
    # print(list3[0]["desc_name"])
    # print(type(list3[0]["desc_name"]))


    # my_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for first_list in list1:
        # print(first_list["desc_name"])
        if(has_chinese(first_list["desc_name"])):
            print("1级："+first_list["desc_name"])
        for sec_list in first_list["sub_class_list"]:
            if(has_chinese(sec_list["desc_name"])):
                print("1级："+first_list["desc_name"]+"==2级： "+sec_list["desc_name"])
            # print(sec_list["desc_name"])
            for third_list in sec_list["app_list"]:
                # print("1级："+first_list["desc_name"]+"==2级： "+sec_list["desc_name"]+"==3级： "+third_list["desc_name"])
                if(has_chinese(third_list["desc_name"])):
                     print("1级："+first_list["desc_name"]+"==2级： "+sec_list["desc_name"]+"==3级： "+third_list["desc_name"])
                else:
                    continue

    return response.text

#安全监控--日志监控--安全日志
def getappdate(date,username,passworde):
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
    # print(type(list1))
    # print(list1[0]["desc_name"])

    list2=list1[0]["sub_class_list"]
    # print(type(list2))
    # print(list2[0]["desc_name"])

    list3=list2[0]["app_list"]
    # print(type(list3))
    # print(list3[0]["desc_name"])
    # print(type(list3[0]["desc_name"]))


    # my_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for first_list in list1:
        # print(first_list["desc_name"])
        if(has_chinese(first_list["desc_name"])):
            print("1级："+first_list["desc_name"])
        for sec_list in first_list["sub_class_list"]:
            if(has_chinese(sec_list["desc_name"])):
                print("1级："+first_list["desc_name"]+"==2级： "+sec_list["desc_name"])
            # print(sec_list["desc_name"])
            for third_list in sec_list["app_list"]:
                # print("1级："+first_list["desc_name"]+"==2级： "+sec_list["desc_name"]+"==3级： "+third_list["desc_name"])
                if(has_chinese(third_list["desc_name"])):
                     print("1级："+first_list["desc_name"]+"==2级： "+sec_list["desc_name"]+"==3级： "+third_list["desc_name"])
                else:
                    continue

    return response.text



# str=has_chinese("未知80端口")
# print(str)
ntos_page="https://10.51.212.31"
username="admin"
passworde="ruijie@123"
str2= getappdate(ntos_page,username,passworde)
# str1=json.loads(str2)
# print(type(str1))
# print(str2)
