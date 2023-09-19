#!/bin/bash
api_key="$3"
if [ "$api_key" == ""  ];then
        api_key="3ca9b336-5f1a-45de-8dfd-1b377890a5f4"
fi
send_url="https://open.feishu.cn/open-apis/bot/v2/hook/$api_key"

#发送消息
function send_message(){
curl -X POST "$send_url" -H 'Content-Type: application/json' -d "
   {
        \"msg_type\":\"text\",
        \"content\":{\"text\":\"$1\"}
   }"
}

#发送消息
function send_file(){
curl -X POST "$send_url" -H 'Content-Type: application/json' -d "
   {
	\"msg_type\": \"post\",
	\"content\": {
		\"post\": {
			\"zh_cn\": {
				\"content\": [
					[
						{
							\"tag\": \"a\",
							\"text\": \"请查看测试报告\",
							\"href\": \"$1\"
						},
						{
							\"tag\": \"at\",
							\"user_id\": \"all\"
						}
					]
				]
			}
		}
	}
   }" 
}


if [ "$1" = "message"  ];then
	send_message "$2"
else
	send_file "$2"
fi
