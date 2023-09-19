import requests
import json
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA



def getpublickey(url):
    publickey =  requests.get(url+"/api/v1/public_key/?Referer="+url,verify=False)
    str1=publickey.text
    response_dict = json.loads(str1)
    # print(type(response_dict))
    # print(response_dict["data"])
    response_dict2=response_dict["data"]
    # print(type(response_dict2))
    # print(response_dict2["details"])
    return response_dict2["details"]
def rsa_data(message,public_key_str):
  
    # public_key_str = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmo2Gf8lI6Gv/xqnMD0DF\nEFkgyjDnsE6Ala8B6T8zpP1fat87dS8BM/8gWL49bALtQDryolM0W/qZUigektTX\nIz9d+O926B6A0IZ3xhTpcickUaPaYvmi1G8HrpJ9QjNch++2932zL89TRA2ofqDc\n9+PBEawegLv2RF0MF20UErdI1RHO6Y0QMwTOSgScMKqO4zmcqFfkB2J0ieGj4Qbf\nniG6jWvsWhgrI5WjfvUZPCMCxEfjt7Y9OikUE0bHImHmqMZTbM6lQT4d+4WwteYN\nQAn4qI9rKduETvM26WXQMQRJ3xl+Zutgjy/0KFMFyPY1SMWumLUSj2CZSBFihfid\nyQIDAQAB\n-----END PUBLIC KEY-----"
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
    return ss1[1:]