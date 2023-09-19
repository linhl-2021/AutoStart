#!/bin/bash
echo -e "killing main.sh\n"
ps -ef|grep main.sh|grep -v grep|awk -F " " '{print $2}'|xargs kill -9


echo -e "removing log in /home/release/log/ ...\n"
rm -rf /home/release/log/*


echo -e "starting main.sh ...\n"
nohup ./main.sh >/home/release/log/main.log 2>&1 >/dev/null &



pid=`ps -ef|grep main.sh|grep -v grep|awk -F " " '{print $2}'`


if [ "$pid" != "" ];then
	echo -e "start main.sh success, pid is $pid,enjoy your time!!!\n"
else
	echo -e "start main.sh failed,please check it!!!\n"
fi
