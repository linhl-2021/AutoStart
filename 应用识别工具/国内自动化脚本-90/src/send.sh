#!/bin/bash
api_key="$3"
if [ "$api_key" == ""  ];then
        api_key="b6868d94-95bc-4128-9b28-c0447939e6bd"
fi
media_id_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=$api_key&type=file"
send_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$api_key"

function send_file(){
python3 - "$@" <<END
#!/usr/bin/python3
import requests
import os
import sys
from urllib3 import encode_multipart_formdata

args = sys.argv[1]
report = args
def post_file(media_id_url,send_url,report):
    data = {'file': open(report,'rb')}
    response = requests.post(url=media_id_url, files=data)
    json_res = response.json()
    media_id = json_res['media_id']

    data = {"msgtype": "file",
             "file": {"media_id": media_id}
            }
    result = requests.post(url=send_url,json=data)
    return(result)

post_file("$media_id_url", "$send_url", report)
print('发送完成')
END
}

#发送消息
function send_message(){
curl "$send_url" -H 'Content-Type: application/json' -d "
   {
        \"msgtype\": \"text\",
        \"text\": {
        \"content\": \"$1\"
        }
   }"
}

if [ "$1" = "message"  ];then
	send_message "$2"
else
	send_file "$2"
fi
