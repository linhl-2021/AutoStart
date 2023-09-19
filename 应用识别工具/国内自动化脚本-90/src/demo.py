import requests
import rsa
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
from Crypto.Cipher import PKCS1_OAEP
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()


def getpublickey(url):
    publickey =  requests.get(url+"/api/v1/public_key/?Referer="+url,verify=False)
    str1=publickey.text
    response_dict = json.loads(str1)
    response_dict2=response_dict["data"]
    return response_dict2["details"]
    
def rsa_data(message,public_key_str):
  
    message = message.encode('utf-8')
    # 加载公钥
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(public_key_str.encode('utf-8'))
    # 使用公钥加密明文
    #cipher = PKCS1_v1_5.new(public_key)
    ciphertext = rsa.encrypt(message, pubkey)
    ss=base64.b64encode(ciphertext)
    ss1=str(ss)[1:]
    return ss1


def login_web(url: str,ntos_page):
    publickey =  getpublickey(ntos_page)
    username=rsa_data("admin",publickey)
    #print(username)
    password=rsa_data("Ruijie@123",publickey)
    #print(password)
    #print(publickey)
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
    csrftoken_string=login_res1.headers['Set-Cookie']

    session_id=login_res["data"]["sessionid"]
    csrftoken = re.findall(r"csrftoken=(\w+);",csrftoken_string)[0]

    login_dict={
      "session_id":session_id,
      "csrftoken":csrftoken
    }
    return login_dict

if __name__ == '__main__':
        unittest.main()












