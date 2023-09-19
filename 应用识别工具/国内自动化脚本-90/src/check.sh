#!/bin/bash
#发包网口
ethcname="eth3"
ethsname="eth3"
ethcip="30.30.30.254"
ethsip="30.30.30.254"
ethcipv6="2000:30::254"
ethsipv6="2000:30::254"
ifconfig $ethcname up
ifconfig $ethsname up
ifconfig $ethcname mtu 1600 
ifconfig $ethsname mtu 1600
ifconfig $ethcname $ethcip netmask 255.255.255.0
ifconfig $ethsname $ethsip netmask 255.255.255.0
#ifconfig $ethXname inet6 del $ethcipv6/112
#ifconfig $ethYname inet6 del $ethsipv6/112
ifconfig $ethcname inet6 add $ethcipv6/112
ifconfig $ethsname inet6 add $ethsipv6/112
ethcmac="`ifconfig -a|grep -A 5  $ethcname:|grep ether|awk -F ' ' '{print $2}'`"
ethsmac="`ifconfig -a|grep -A 5  $ethsname:|grep ether|awk -F ' ' '{print $2}'`"

#获取ip段
ip1segment="192.10.1.1/16"
ip2segment="202.20.1.1/16"
ip1segmentv6="2000:2001::"
ip2segmentv6="2000:2002::"

#设备网口
z5100cip="30.30.30.1"
z5100sip="30.30.30.1"
z5100cipv6="2000:30::1"
z5100sipv6="2000:30::1"
z5100cmac="00:d0:f8:22:36:84"
z5100smac="00:d0:f8:22:36:84"

#参数
type="$1"
debug="$2"
api_key=""
api_key_fs=""

if [ -z "$3" ] ;then
	if [ "$debug" == "test" ];then
        api_key=""
	else
		if [ "$type" == "appid" ];then
			api_key="f7a44f62-d361-4db9-a6ac-556007faf234"
		elif [ "$type" == "ips" ];then
			api_key="faf4bf93-a33e-455b-9a32-c2736fbdafb0"
		else
		#	break
			exit 0
		fi
	fi	
else
	api_key="$3"
fi

if [ -z "$4" ] ;then
	if [ "$debug" == "test" ];then
        api_key_fs=""
	else
		if [ "$type" == "appid" ];then
			api_key_fs="08c71cec-15b3-4630-ab30-eafa6e6c2b10"
		elif [ "$type" == "ips" ];then
			api_key_fs="1dd56c87-e54e-4151-8bc3-159c8477c79e"
		else
			break
		fi
	fi	
else
	api_key_fs="$4"
fi

#关键路径
path="`pwd`"
cd ..
pc_path="`pwd`"
pcap_path="$pc_path/data/pcap_$type"
work_path="$pc_path/report/Z5100_$type"
work_temp="$pc_path/temp"
update_path="$pc_path/update"
cd $path

#获取自己进程id
pid="$$"

#环境初始化
mkdir -p $pcap_path
mkdir -p $work_path
mkdir -p $work_temp
cd $work_path
rm -rf *
mkdir -p all
mkdir -p rename
mkdir -p rename_other
mkdir -p bigpcap
mkdir -p bigpcap_other
mkdir -p only
mkdir -p only_other
touch result.txt
cd $work_temp
rm -rf $pid
mkdir $pid
cd $update_path
mkdir -p appid
mkdir -p ips
rm -rf $type/*.txt
content="Packet playback verification"

#原始包路径检查
cd $pcap_path
count="`ls |wc -l`"
if [ $count -eq 0 ];then
	exit 0
fi

#随机数
function rand(){
    min=$1
    max=$(($2-$min+1))
    num=$(date +%s%N)
    echo $(($num%$max+$min))
}

#随机ip
function randip(){
python3 - "$@" <<END
#!/usr/bin/python3
import random
import struct
import socket
import sys
args = sys.argv[1:]

RANDOM_IP_POOL=args
def __get_random_ip():
    str_ip = RANDOM_IP_POOL[random.randint(0,len(RANDOM_IP_POOL) - 1)]
    str_ip_addr = str_ip.split('/')[0]
    str_ip_mask = str_ip.split('/')[1]
    ip_addr = struct.unpack('>I',socket.inet_aton(str_ip_addr))[0]
    mask = 0x0
    for i in range(31, 31 - int(str_ip_mask), -1):
        mask = mask | ( 1 << i)
    ip_addr_min = ip_addr & (mask & 0xffffffff)
    ip_addr_max = ip_addr | (~mask & 0xffffffff)
    return socket.inet_ntoa(struct.pack('>I', random.randint(ip_addr_min, ip_addr_max)))
msg = __get_random_ip()
print(msg)
END
}

function result(){
cd $work_path
rm -rf test.csv
echo "大包,小包,包长,协议,id,名称,结果" >> test.csv
while read line; do
	bigpcap_name="`echo $line|awk -F '#' '{print $1}'`"
	pcap="`echo $line|awk -F '#' '{print $2}'`"
	len="`echo $line|awk -F '#' '{print $3}'`"
	protocol="`echo $line|awk -F '#' '{print $4}'`"
	sid_old="`echo $line|awk -F '#' '{print $5}'`"
	sid_new="`echo $line|awk -F '#' '{print $5}'|tr "@" "\n"`"
	name_old="`echo $line|awk -F '#' '{print $6}'`"
	name_new="`echo $line|awk -F '#' '{print $6}'|tr "@" "\n"`"
	result="`echo $line|awk -F '#' '{print $7}'`"
	echo "$bigpcap_name,$pcap,$len,$protocol,\"$sid_new\",\"$name_new\",$result" >> test.csv
done < $1
}

function test(){
cd $pcap_path
replay_count=`ls|wc -l`
if [ "$type" == "appid" ];then
	yes_count=`ls|grep "@yes."|wc -l`
	bash $path/send.sh message "Now all pcap count $replay_count,yes pcap count $yes_count" $api_key
	bash $path/send_fs.sh message "Now all pcap count $replay_count,yes pcap count $yes_count" $api_key_fs
else
	bash $path/send.sh message "Now replay pcap count $replay_count" $api_key
	bash $path/send_fs.sh message "Now replay pcap count $replay_count" $api_key_fs
fi

echo ""
bigpcap_count=`ls *|wc -l`
echo "bigpcap_count is $bigpcap_count"
no=0

for bigpcap in $(ls -rS *)
do	
	timestamp1=`expr $(date '+%s') \* 1000 + $(date '+%N') / 1000000`	
	let "no++"
	#分解报文
	cd $pcap_path
	bigpcaplen="`du -sh -b $bigpcap|awk -F ' ' '{print $1}'`"

	if [[ $bigpcap =~ "@na.pcap" ]];then

		id_test="`echo $bigpcap|awk -F '_' '{print $1}'|awk '$1=$1'`"
		other_test="`echo $bigpcap|cut -d '_' -f 2-|awk '$1=$1'`"
		name_test="`echo $bigpcap|cut -d '_' -f 2-|awk -F '@' '{print $1}'|awk '$1=$1'`"
		flag1_test="`cat $update_path/$type/*rules.txt|grep \" $id_test \"|grep \" $name_test \"`"
		if [ -z "$flag1_test" ];then
			flag2_test="`cat $update_path/$type/*rules.txt|grep \" $name_test \"`"
			if [ -z "$flag2_test" ];then
				mv $bigpcap $work_path/bigpcap_other/
			else
				index_test="`cat $update_path/$type/*rules.txt|grep \" $name_test \"|awk -F ' ' '{print $2}'`"
				mv $bigpcap $work_path/rename_other/$index_test'_'$other_test
			fi
		else
			index_test="`cat $update_path/$type/*rules.txt|grep \" $name_test \"|awk -F ' ' '{print $2}'`"
			mv $bigpcap $work_path/only_other/$index_test'_'$other_test
		fi

		timestamp2=`expr $(date '+%s') \* 1000 + $(date '+%N') / 1000000`
		usetime=`expr $timestamp2 - $timestamp1`
		echo "info: bigpcap $no $bigpcap is na no replay, len is $bigpcaplen, usetime is $usetime ms"
        	continue
	fi

	if [[ $bigpcap =~ "@err.pcap" ]];then
		
		id_test="`echo $bigpcap|awk -F '_' '{print $1}'|awk '$1=$1'`"
		other_test="`echo $bigpcap|cut -d '_' -f 2-|awk '$1=$1'`"
		name_test="`echo $bigpcap|cut -d '_' -f 2-|awk -F '@' '{print $1}'|awk '$1=$1'`"
		flag1_test="`cat $update_path/$type/*rules.txt|grep \" $id_test \"|grep \" $name_test \"`"
		if [ -z "$flag1_test" ];then
			flag2_test="`cat $update_path/$type/*rules.txt|grep \" $name_test \"`"
			if [ -z "$flag2_test" ];then
				mv $bigpcap $work_path/bigpcap_other/
			else
				index_test="`cat $update_path/$type/*rules.txt|grep \" $name_test \"|awk -F ' ' '{print $2}'`"
				mv $bigpcap $work_path/rename_other/$index_test'_'$other_test
			fi
		else
			index_test="`cat $update_path/$type/*rules.txt|grep \" $name_test \"|awk -F ' ' '{print $2}'`"
			mv $bigpcap $work_path/only_other/$index_test'_'$other_test
		fi
			
		timestamp2=`expr $(date '+%s') \* 1000 + $(date '+%N') / 1000000`
		usetime=`expr $timestamp2 - $timestamp1`
		echo "info: bigpcap $no $bigpcap is err no replay, len is $bigpcaplen, usetime is $usetime ms"
        	continue
	fi

	if [[ $bigpcap =~ "@ignore.pcap" ]];then
		
		id_test="`echo $bigpcap|awk -F '_' '{print $1}'|awk '$1=$1'`"
		other_test="`echo $bigpcap|cut -d '_' -f 2-|awk '$1=$1'`"
		name_test="`echo $bigpcap|cut -d '_' -f 2-|awk -F '@' '{print $1}'|awk '$1=$1'`"
		flag1_test="`cat $update_path/$type/*rules.txt|grep \" $id_test \"|grep \" $name_test \"`"
		if [ -z "$flag1_test" ];then
			flag2_test="`cat $update_path/$type/*rules.txt|grep \" $name_test \"`"
			if [ -z "$flag2_test" ];then
				mv $bigpcap $work_path/bigpcap_other/
			else
				index_test="`cat $update_path/$type/*rules.txt|grep \" $name_test \"|awk -F ' ' '{print $2}'`"
				mv $bigpcap $work_path/rename_other/$index_test'_'$other_test
			fi
		else
			index_test="`cat $update_path/$type/*rules.txt|grep \" $name_test \"|awk -F ' ' '{print $2}'`"
			mv $bigpcap $work_path/only_other/$index_test'_'$other_test
		fi
			
		timestamp2=`expr $(date '+%s') \* 1000 + $(date '+%N') / 1000000`
		usetime=`expr $timestamp2 - $timestamp1`
		echo "info: bigpcap $no $bigpcap is ignore no replay, len is $bigpcaplen, usetime is $usetime ms"
        	continue
	fi
	#uvx
	rm  -rf $work_path/all
	mkdir -p $work_path/all
	pkt2flow  -uo $work_path/all $bigpcap
    #ls -l $work_path/all/* > $work_temp/$bigpcap
	#对每个包进行发包，获取流表，会话包与识别到的结果进行关联
	cd $work_path/all/
	packetnumber="`ls */*.pcap|wc -l`"
	#if [ $packetnumber -eq 1 ];then
	#	echo "info1: $no $bigpcap is single package len is $bigpcaplen"
	#else
	#	echo "info1: $no $bigpcap is many package , len is $bigpcaplen , resolve packetnumber is $packetnumber"
	#fi
	for file in $(ls -S */*.pcap)
	do
		len="`du -sh -b $file|awk -F ' ' '{print $1}'`"
		if [[ $file =~ ":" ]];then
			rand1=$(rand 1 2000)
			rand2=$(rand 1 2000)
			ip1=$ip1segmentv6$rand1
			ip2=$ip2segmentv6$rand2

		else
			ip1="$(randip $ip1segment)"
			ip2="$(randip $ip2segment)"
		fi
		#发包
		cd $work_path/all/
		echo "replay: bigpcap $no $bigpcap $file $len client:$ip1 server:$ip2"
		#去除vlan，生成去除vlan后的temp.pcap
		tcprewrite --enet-vlan=del --infile=$file --outfile=$work_temp/$pid/temp.pcap
		#tcprewrite --infile=$file --outfile=$work_temp/$pid/temp.pcap
		#temp.pcap区分上下行
		if [[ $ip1 =~ ":" ]];then
			tcpprep --port --cachefile=$work_temp/$pid/temp.cach --pcap=$work_temp/$pid/temp.pcap
			tcprewrite -m 1600 -C -e [$ip1]:[$ip2] --enet_smac=$ethcmac,$ethsmac --enet_dmac=$z5100cmac,$z5100smac -c $work_temp/$pid/temp.cach -i $work_temp/$pid/temp.pcap -o $work_temp/$pid/ok.pcap
		else	
			tcpprep --auto=client --cachefile=$work_temp/$pid/temp.cach --pcap=$work_temp/$pid/temp.pcap
			#修改temp.pcap的ip、mac、checksum，生成ok.pcap	
			#tcprewrite -C -E --mtu-trunc -e $ip1:$ip2 --enet_smac=$ethcmac,$ethsmac --enet_dmac=$z5100cmac,$z5100smac -c $work_temp/$pid/temp.cach -i $work_temp/$pid/temp.pcap -o $work_temp/$pid/ok.pcap
			tcprewrite -m 1600 -C -e $ip1:$ip2 --enet_smac=$ethcmac,$ethsmac --enet_dmac=$z5100cmac,$z5100smac -c $work_temp/$pid/temp.cach -i $work_temp/$pid/temp.pcap -o $work_temp/$pid/ok.pcap
			#ok.pcap区分上下行
			#tcpprep --auto=client --cachefile=$work_temp/$pid/ok.cach --pcap=$work_temp/$pid/ok.pcap
			#发ok.pcap
			#tcpreplay -c $work_temp/$pid/ok.cach -i $ethcname -I $ethsname -l 1 -p 100 $work_temp/$pid/ok.pcap
			#echo "tcpre_qian now `date`" > /home/release/src/time_check
		fi
		tcpreplay -c $work_temp/$pid/temp.cach -i $ethcname -I $ethsname -l 1 -p 300 $work_temp/$pid/ok.pcap
       	rm -rf $work_temp/$pid/*
		#echo "tcpre_hou now `date`" >> /home/release/src/time_check
		
		#获取流表
		cd $path
		#echo "get_qian now `date`" >> /home/release/src/time_check
		bash get.sh $type root
		#echo "get_hou now `date`" >> /home/release/src/time_check

		#会话包与识别到的结果进行关联
        chmod 777 $work_path/$type.txt
        cd $work_path/all/
		pcap="`echo $file|awk -F '/' '{print $2}'|awk -F '_' '{print $1"_"$2"_"$3"_"$4}'`"
		protocol_type="`echo $file|awk -F '/' '{print $1}'`"
		if [ "$protocol_type" == "udp" ];then
			protocol="udp"
		else
			protocol="tcp"	
		fi
        srcport="`echo $file|awk -F '/' '{print $2}'|awk -F '_' '{print $2}'`"
        dstport="`echo $file|awk -F '/' '{print $2}'|awk -F '_' '{print $4}'`"
        hit="`cat $work_path/$type.txt|grep $ip1|grep $srcport|grep $ip2|grep $dstport`"
		bigpcap_sid="`echo $bigpcap|awk -F '_' '{print $1}'`"
		bigpcap_name="`echo $bigpcap`"
        if [ "$hit" != "" ];then
			if [ "$type" == "appid" ];then
				# tmp="`cat $work_path/$type.txt|grep :$srcport|grep :$dstport|awk -F ':' '{print $3}'|awk -F ' ' '{print $2}'|sort|uniq -c > $work_path/sid_tmp.txt`"
					
				tmp="`cat $work_path/$type.txt|grep /$srcport|grep /$dstport|awk -F '/' '{print $3}'|awk -F ' ' '{print $2}'|sort|uniq -c > $work_path/sid_tmp.txt`"
			elif [ "$type" == "ips" ];then
				tmp="`cat $work_path/$type.txt|grep /$srcport|grep /$dstport|grep msg|awk -F 'sid' '{print $2}'|awk -F ' ' '{print $1}'|awk -F '(' '{print $2}'|awk -F ')' '{print $1}'|sort|uniq -c > $work_path/sid_tmp.txt`"
			else
				break
			fi
			while read line; do
				id="`echo $line|awk -F ' ' '{print $2}'`"
				if [ "$type" == "appid" ];then
					if [[ $id == "0-0-0-0" ]];then
						continue
					fi
					name_tmp="`cat $update_path/$type/*rules.txt|grep " $id"|awk -F ' ' '{print $1}'`"
					elif [ "$type" == "ips" ];then
					name_tmp="`cat $update_path/$type/*rules.txt|grep $id|awk -F ",'" '{print $1"\047,"$2","$6","$7","}'|awk -F "'," '{print "【"$3"-"$4"】"$2}'`"
				else
					break
				fi
				echo $name_tmp|grep -v '^$' >> $work_path/name_tmp.txt
			done < $work_path/sid_tmp.txt
			name="`cat $work_path/name_tmp.txt|tr "\n" "@"`"
			#sid="`cat sid_tmp.txt |sed 's/^[ \t]*//g'|tr " " "_"|tr "\n" "@"`"
			sid="`cat $work_path/sid_tmp.txt|awk -F ' ' '{print $2}'|tr "\n" "@"`"
			cat $work_path/sid_tmp.txt  >> $work_path/result.txt
			rm -rf $work_path/sid_tmp.txt
			rm -rf $work_path/name_tmp.txt

			if [[ $sid =~ $bigpcap_sid ]];then
				echo "$bigpcap_name#$pcap#$len#$protocol#$sid#$name#yes" >> $work_path/log.csv
				#scp -r $work_path/all/$file $work_path/yes/$bigpcap_name@$pcap@$protocol-$sid.pcap
				if [ "$type" == "appid" ];then
					terminal="`echo $bigpcap_name |awk -F '@' '{print $2}' |tr [A-Z] [a-z]`"
					if [ "$terminal" == "android" ];then
						terminal="android"
					elif [ "$terminal" == "iphone" ];then
						terminal="iphone"
					elif [ "$terminal" == "pc" ];then
						terminal="pc"
					else
						terminal="err"	
					fi
					other="`echo $bigpcap_name |cut -d '@' -f 3-`"
					name_final="`cat $update_path/$type/*rules.txt|grep " $bigpcap_sid"|awk -F ' ' '{print $1}'`"
					#if [ $packetnumber -ne 1 ];then
						scp -r $work_path/all/$file $work_path/only/$bigpcap_sid"_"$name_final"@"$terminal"@"$other
					#fi
				else
					if [ $packetnumber -ne 1 ];then
						scp -r $work_path/all/$file $work_path/only/$bigpcap_name
					fi
				fi
				mv $work_path/all/$file $work_path/all/$file.ok
				rm -rf $work_path/bigpcap/$bigpcap
				rm -rf $work_path/$type.txt
				#mv $work_path/$type.txt $work_path/$pcap.txt
				break
			else
				scp -r $pcap_path/$bigpcap $work_path/bigpcap/
				echo "$bigpcap_name#$pcap#$len#$protocol#$sid#$name#no" >> $work_path/log.csv
				if [ "$type" == "appid" ];then
                                        terminal="`echo $bigpcap_name |awk -F '@' '{print $2}' |tr [A-Z] [a-z]`"
                                        if [ "$terminal" == "android" ];then
                                                terminal="android"
                                        elif [ "$terminal" == "iphone" ];then
                                                terminal="iphone"
                                        elif [ "$terminal" == "pc" ];then
                                                terminal="pc"
                                        else
                                                terminal="err"
                                        fi
                                        other="`echo $bigpcap_name |cut -d '@' -f 3-`"
					original_name="`echo $bigpcap_name |awk -F '@' '{print $1}'|cut -d '_' -f 2-`"
					if [[ "$original_name@" == "$name" ]];then
						rename_id="`echo $sid|sed 's/0-0-0-0//g'|sed 's/@//g'`"
						scp -r $work_path/all/$file $work_path/rename/$rename_id"_"$name$terminal"@"$other
						#mv -f $work_path/bigpcap/$bigpcap $work_path/rename/$rename_id"_"$name$terminal"@"$other
					fi
				fi
				#echo "$bigpcap_name#$pcap#$len#$protocol#$sid#$name#no" >> $work_path/log.csv
				#scp -r $work_path/all/$file $work_path/no/$bigpcap_name@$pcap@$protocol.pcap
				scp -r $pcap_path/$bigpcap $work_path/bigpcap/
				#mv $work_path/all/$file $work_path/all/$file.ok
			fi
		else
			echo "$bigpcap_name#$pcap#$len#$protocol###no" >> $work_path/log.csv
			#scp -r $work_path/all/$file $work_path/no/$bigpcap_name@$pcap@$protocol.pcap
			scp -r $pcap_path/$bigpcap $work_path/bigpcap/
			mv $work_path/all/$file $work_path/all/$file.err
		fi
		rm -rf $work_path/$type.txt
		#mv $work_path/$type.txt $work_path/$pcap.txt
	done
	cd $pcap_path
	rm -rf $bigpcap
	timestamp2=`expr $(date '+%s') \* 1000 + $(date '+%N') / 1000000`
	usetime=`expr $timestamp2 - $timestamp1`
	if [ $packetnumber -eq 1 ];then
		echo "info: bigpcap $no $bigpcap is single, package len is $bigpcaplen, usetime is $usetime ms"
	else
		echo "info: bigpcap $no $bigpcap is many package len is $bigpcaplen, resolve packetnumber is $packetnumber, usetime is $usetime ms"
	fi
done
}

function clear(){
cd $pcap_path
rm -rf *
scp -r $work_path/bigpcap/* ./
cd $work_path
rm -rf all
#rm -rf no
rm -rf bigpcap
rm -rf log.csv
#mkdir -p yes
#mkdir -p no
mkdir -p bigpcap
mkdir -p only
cd $update_path
mkdir -p appid
mkdir -p ips
rm -rf $type/*.txt
}

function finish(){
#结果文件去重排序
cd $work_path/
countall="`cat log.csv|wc -l`"
count="`cat log.csv|grep no|wc -l`"
mv log.csv log_$1.csv
if [ $countall -eq 0 -a $1 -eq 0 ];then
	cat result.txt|awk -F ' ' '{print $2}'|grep -Ev '^$|#'|sort|uniq >> final.txt
	rm -rf result.txt
	cat log*.csv|grep "#yes" > all.csv
	result all.csv
	python3 $path/csv_to_excel.py test.csv test.xlsx
	mv test.xlsx log_Z5100_$type@$(date +%Y%m%d%H%M).xlsx
	mv test.csv log_Z5100_$type@$(date +%Y%m%d%H%M).csv
	#cat log*.csv|grep ,yes > log_Z5100_$type@$(date +%Y%m%d%H%M).csv
	bash $path/send.sh message "二、$content fail !" $api_key
	bash $path/send_fs.sh message "二、$content fail !" $api_key_fs
	bash $path/send.sh file log_Z5100*.xlsx $api_key
	mkdir -p $pc_path/report/history/report_temp
	echo "二、$content fail !" >> $pc_path/report/history/report_temp/result.txt
	echo "This feature library is fail !" >> $pc_path/report/history/report_temp/result.txt
	scp -r $work_path/log_Z5100*.xlsx $pc_path/report/history/report_temp/
	#scp -r $work_path/log_Z5100*.csv $pc_path/report/history/report_temp/
	cd $pcap_path
	rm -rf *
	exit 0
fi
if [ $count -eq 0 ];then
	cat result.txt|awk -F ' ' '{print $2}'|grep -Ev '^$|#'|sort|uniq >> final.txt
	rm -rf result.txt
	cat log*.csv|grep "#yes" > all.csv
        result all.csv
	python3 $path/csv_to_excel.py test.csv test.xlsx
        mv test.xlsx log_Z5100_$type@$(date +%Y%m%d%H%M).xlsx
	mv test.csv log_Z5100_$type@$(date +%Y%m%d%H%M).csv
	#cat log*.csv|grep ,yes > log_Z5100_$type@$(date +%Y%m%d%H%M).csv
	bash $path/send.sh message "二、$content pass !" $api_key
	bash $path/send_fs.sh message "二、$content pass !" $api_key_fs
	bash $path/send.sh file log_Z5100*.xlsx $api_key
	mkdir -p $pc_path/report/history/report_temp				
	echo "二、$content pass !" >> $pc_path/report/history/report_temp/result.txt
	echo "This feature library is pass !" >> $pc_path/report/history/report_temp/result.txt
	scp -r $work_path/log_Z5100*.xlsx $pc_path/report/history/report_temp/
	#scp -r $work_path/log_Z5100*.csv $pc_path/report/history/report_temp/
	cd $pcap_path
	rm -rf *
	exit 0
fi
}

#配置设备日志
cd $path
bash init.sh $type root

if [[ -f $pc_path/update/$type/$type-rules.txt && -s $pc_path/update/$type/$type-rules.txt ]];then
	echo ok
else
	echo error
	bash init.sh $type root
fi

#第一次
test
finish 0

#中间次数
for ((i=1; i<2; i++))
do
	clear
	cd $path
	bash init.sh $type root
	test
	finish $i
done

#最后一次
clear
cd $path
bash init.sh $type root
test

#结果文件去重排序
cd $work_path/
cat result.txt|awk -F ' ' '{print $2}'|grep -Ev '^$|#'|sort|uniq >> final.txt
rm -rf result.txt
rm -rf all
mv log.csv log-end.csv
count="`cat log-end.csv|grep no|wc -l`"
if [ $count -eq 0 ];then
	cat log*.csv|grep "#yes" > all.csv
        result all.csv
	python3 $path/csv_to_excel.py test.csv test.xlsx
        mv test.xlsx log_Z5100_$type@$(date +%Y%m%d%H%M).xlsx
	mv test.csv log_Z5100_$type@$(date +%Y%m%d%H%M).csv
	#cat log*.csv|grep ,yes > log_Z5100_$type@$(date +%Y%m%d%H%M).csv
	bash $path/send.sh message "二、$content pass !" $api_key
	bash $path/send_fs.sh message "二、$content pass !" $api_key_fs
	bash $path/send.sh file log_Z5100*.xlsx $api_key
	mkdir -p $pc_path/report/history/report_temp				
	echo "二、$content pass !" >> $pc_path/report/history/report_temp/result.txt
	echo "This feature library is pass !" >> $pc_path/report/history/report_temp/result.txt
	scp -r $work_path/log_Z5100*.xlsx $pc_path/report/history/report_temp/
	#scp -r $work_path/log_Z5100*.csv $pc_path/report/history/report_temp/
	cd $pcap_path
	rm -rf *
	exit 0
fi
cat log_*.csv|grep "#yes" > log.csv
cat log-end.csv >> log.csv
cat log.csv|sort|uniq > all.csv
result all.csv
python3 $path/csv_to_excel.py test.csv test.xlsx
mv test.xlsx log_Z5100_$type@$(date +%Y%m%d%H%M).xlsx
mv test.csv log_Z5100_$type@$(date +%Y%m%d%H%M).csv
rm -rf log.csv
rm -rf log-end.csv
bash $path/send.sh message "二、$content fail !" $api_key
bash $path/send_fs.sh message "二、$content fail !" $api_key_fs
bash $path/send.sh file log_Z5100*.xlsx $api_key
mkdir -p $pc_path/report/history/report_temp				
echo "二、$content fail !" >> $pc_path/report/history/report_temp/result.txt
echo "This feature library is fail !" >> $pc_path/report/history/report_temp/result.txt
scp -r $work_path/log_Z5100*.xlsx $pc_path/report/history/report_temp/
#scp -r $work_path/log_Z5100*.csv $pc_path/report/history/report_temp/
