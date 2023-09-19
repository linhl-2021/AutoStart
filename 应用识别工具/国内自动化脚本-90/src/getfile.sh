#!/bin/bash
#初始化
file_url="http://172.28.249.90/test/file/"
pcap_appid_url="http://172.28.249.90/test/pcap_appid/"
pcap_ips_url="http://172.28.249.90/test/pcap_ips/"

path="`pwd`"
cd ..
file_path="`pwd`/data/file"
pcap_appid_path="`pwd`/data/pcap_appid_temp"
pcap_ips_path="`pwd`/data/pcap_ips_temp"
cd $path

mkdir -p $file_path
mkdir -p $pcap_appid_path
mkdir -p $pcap_ips_path

user="huanglong"
passwd="isFd00Wo"
format="$1"

#获取文件
for ((j=0; j<1; j++))
do	
	#curl -O -u huanglong:isFd00Wo http://172.28.249.90/ips/file/pcap_v6.zip --progress
	if [ "$format" == "file" ];then
		wget -c -r -np -nd -nH -R html,tmp --no-http-keep-alive --http-user=$user --http-password=$passwd $file_url -P $file_path
	elif [ "$format" == "pcap_appid" ];then
		wget -c -r -np -nd -nH -R index.html -R index.html.tmp --no-http-keep-alive --http-user=$user --http-password=$passwd $pcap_appid_url -P $pcap_appid_path
	elif [ "$format" == "pcap_ips" ];then
		wget -c -r -np -nd -nH -R index.html -R index.html.tmp --no-http-keep-alive --http-user=$user --http-password=$passwd $pcap_ips_url -P $pcap_ips_path
	else
		break
	fi
done

