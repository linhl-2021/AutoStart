import requests
import json
import ssl
import re
import unittest
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from requests.packages import urllib3
from http.cookiejar import CookieJar,LWPCookieJar
from urllib.request import Request,urlopen,HTTPCookieProcessor,build_opener
from urllib.parse import urlencode
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()


def getpublickey(url):
    publickey =  requests.get(url+"/api/v1/public_key/?Referer="+url,verify=False)
    str1=publickey.text
    response_dict = json.loads(str1)
    response_dict2=response_dict["data"]
    return response_dict2["details"]

def rsa_data(message,public_key_str):
    #public_key_str = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8Nu3oRPUXF+plMypMk4r\nx/QbSNkc+lF0ez4jY39Sd42bWnK+5UK41aybzCA7yUzLDD0cAOELwryablMYVdEK\n4bQO/C0XcBBQylL7g1ctwh53TukbgfkMlvG4j6DSye8Sfpr8deIE1y11uBDUxfW3\nxS3nI9ul3eeMDe8ps9bk+Rhxhs3SdQP/SZUhRI92LnWXBtLBvOx+aJ5F8nMfzV4K\nnOEWlTp9vGk+ckcCw7Kg2SHkQNxOcw06GNHZzPyWOQdOcnW2icQm0vwKK7EXlL5U\nC6En6UrTfXSK8blDs17X3PD/K27ey1wnhBooQxyaHdzZYeNBSVuZfAIyGLRAHmE4\niwIDAQAB\n-----END PUBLIC KEY-----"
    # 明文
    message = message.encode('utf-8')
    # message=bytes(message,encoding='utf-8')
    # 获取公钥对象
    public_key = RSA.import_key(public_key_str)
    # 使用公钥加密明文
    cipher = PKCS1_v1_5.new(public_key)
    ciphertext = cipher.encrypt(message)
    ss=base64.b64encode(ciphertext)
    ss1=str(ss)
    print("密文0：", ss1[1:])
    return ss1[1:]
    # print("密文1：", ciphertext)
    # # 将加密结果转换为16进制字符串
    # ciphertext_hex = ciphertext.hex()
    # # 输出加密结果
    # print("密文2：", ciphertext_hex)

# publickey =  getpublickey("https://10.51.212.212")
# username=rsa_data("Ruijie@123",publickey)
def login_web(url,ntos_page,username,password):
    publickey =  getpublickey(ntos_page)
    username=rsa_data(username,publickey)
    #print(username)
    password=rsa_data(password,publickey)
    body = {
            "username":username,
            "password":password,
            "encrypt_disable":True

          }
    body = json.dumps(body)
    header = {
    "Accept":"application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }

    login_res1 = requests.post(url,
                                data=body,
                                headers=header,verify=False)
    login_res =login_res1.json()
    print("33333",login_res)
    csrftoken_string=login_res1.headers['Set-Cookie']
    print('4444',csrftoken_string)
    session_id=login_res["data"]["sessionid"]
    csrftoken = re.findall(r"csrftoken=(\w+);",csrftoken_string)[0]

    login_dict={
      "session_id":session_id,
      "csrftoken":csrftoken
    }
    print(login_dict)
    return login_dict

if __name__ == '__main__':
        unittest.main()












