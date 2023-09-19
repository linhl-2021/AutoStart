import requests

url = 'https://10.51.212.31/api/v1/feature_library/getData'
# url = 'https://10.51.212.31/api/v1/application/'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Referer': 'https://10.51.212.31/',
    'Cookie': 'LOCAL_LANG_i18n=zh; session=c922a2b3-5334-4ca7-b1c4-1c7145ce12d4; csrftoken=VxJEKcBgbY8Nlf69UZsjMm4L8naqxKL3SV3jvHxcoC3ayotvQaEXJXzpABhIOFGp; sessionid=axyk6g2pk1bborbjew0tiwu6bptfz5k9',
}
response = requests.get(url, headers=headers,verify=False)

print(response.headers)
# print(response.text)