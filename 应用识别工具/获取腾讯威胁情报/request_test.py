import json
import requests

url = 'https://tix.qq.com/?ADTAG=cloud_tencent'
# url = 'https://10.51.212.31/api/v1/application/'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}
data = {
  "Action": "DescribeSearchHot"
}


response = requests.post(url, headers=headers,data=data,verify=False)

response.encoding = "utf-8"
print(response.text)
str1=json.loads(response.text)
print(str1)
# print(response.text)