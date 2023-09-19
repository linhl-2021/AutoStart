import json
import re
import requests
import sys
import demo

def getappdate(date,language,username,password):
    ntos_page = date
    login_api = f"{ntos_page}/api/v1/login/"
    res=demo.login_web(login_api,ntos_page,username,password)
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
    fielname=ntos_page.split("//")[1]+"-"+language
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
        with open(f'{fielname}-1级.txt', 'a', encoding='utf-8') as file1:
            file1.write(first_list["desc_name"]+"\n")
            file1.close()
        for sec_list in first_list["sub_class_list"]:
            # print("1级："+first_list["desc_name"]+"==2级： "+sec_list["desc_name"])
            with open(f'{fielname}-2级.txt', 'a', encoding='utf-8') as file2:
                file2.write("1级："+first_list["desc_name"]+"==2级： "+sec_list["desc_name"]+"\n")
                file2.close()
            # print(sec_list["desc_name"])
            for third_list in sec_list["app_list"]:
                # print("1级："+first_list["desc_name"]+"==2级： "+sec_list["desc_name"]+"==3级： "+third_list["desc_name"])
                with open(f'{fielname}-3级.txt', 'a', encoding='utf-8') as file3:
                    file3.write("1级："+first_list["desc_name"]+"==2级： "+sec_list["desc_name"]+"==3级： "+third_list["desc_name"]+"\n")
                    file3.close()





if __name__ == "__main__":
    getappdate("https://10.51.212.30","en","admin","ruijie@123")
    # getappdate("https://10.51.212.30","ch","admin","Ruijie@123")