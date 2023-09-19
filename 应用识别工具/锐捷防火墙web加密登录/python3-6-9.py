import base64
import json
import requests
import rsa

def test1(public_key_str):
    # public_key_str = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtbQ302xHzPfmFF12XFXE\n4561+rVsJDxKEBBJGMWBn1ftkId8Gggt9eVpEzXB/mhL251u9XjCF9tQkK2GPStg\nKWAACA4smQSctZtU6o1128smR204iXbdeXqZiMcGS086EdW2AIxywsDY/I95amzb\nEa1zHkZtfHy0lRJ9SOomhNn3GDO2/6DUKMo3OCmOSk+Y74k3cHRHoeg9WEw2CuSE\nCGsSKQtvjRLkL9rJeU9P8X/lwNKWeatPITdqEnsDhPg88V7MC1Birqjp7XOcprdH\nlJgDZ+6Tf2d9itbmyZJ9+8EFeirmfa3EFGL8y5mn+3ZJH1MemtytQK2zEwlz09S9\nLQIDAQAB\n-----END PUBLIC KEY-----"
    # 明文
    message1="admin"
    message1 = message1.encode('utf-8')
    message2="ruijie@123"
    message2 = message2.encode('utf-8')


    # 加载公钥
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(public_key_str.encode('utf-8'))

    # 使用公钥加密明文
    ciphertext1 = rsa.encrypt(message1, pubkey)
    ss=base64.b64encode(ciphertext1)
    ss1=str(ss)[1:]
    print("明文消息：", message1)
    print("加密后的消息：", ss1)

    ciphertext2 = rsa.encrypt(message2, pubkey)
    ss=base64.b64encode(ciphertext2)
    ss1=str(ss)[1:]
    print("明文消息：", message2)
    print("加密后的消息：", ss1)

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

if __name__ == '__main__':
    # test1()
    url="https://172.28.247.85"
    ss=getpublickey(url)    
    print(ss)
    test1(ss)