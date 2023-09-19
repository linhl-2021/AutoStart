#!/bin/bash
#全局变量初始化
debug=""
key=""
key_fs=""
type=""
version=""
path="`pwd`"
cd ..
pc_path="`pwd`"
cd $path

#函数
is_empty_dir(){ 
    return `ls -A $1|wc -w`
}

work(){
	cd $path
	rm -rf $pc_path/data/pcap_${type}/*
	bash getfile.sh pcap_${type}
	sleep 3

	if [ "`ls -A $pc_path/data/pcap_${type}_temp`" == "" ];then
		bash getfile.sh pcap_${type}
		sleep 3
    fi
	
	if [ "`ls -A $pc_path/data/pcap_${type}_temp`" == "" ];then
		cp -r $pc_path/data/pcap_${type}_b/* $pc_path/data/pcap_${type}/
		#echo "i am bak"
	else
		cp -r $pc_path/data/pcap_${type}_temp/* $pc_path/data/pcap_${type}/
		#echo "i am temp"
	fi

	python3 del_space.py "$pc_path/data/pcap_${type}"
	bash check.sh ${type} ${debug} ${key} ${key_fs} > ../log/log_${type}.txt
	cat $pc_path/log/log_${type}.txt|grep info:|awk -F 'info:' '{print $2}' > $pc_path/report/history/report_temp/replay.log
}

report(){
	cd $pc_path/report/history
	time="$(date +%Y%m%d%H%M)"
	mv report_temp report_${type}_${version}_${time}
	zip -q -r report_${type}_${version}_${time}.zip report_${type}_${version}_${time}
	report="report_${type}_${version}_${time}.zip"
	curl -F "action=upload" -F "filename=@$report" -u huanglong:isFd00Wo http://172.28.249.90/test/report/$type/
	rm -rf $report
	cd $path
	bash send_fs.sh file "http://172.28.249.90/test/report/$type/report_${type}_${version}_${time}.zip" $key_fs
}

#主函数
#for ((i=0; i<1; i++))
while :
do
	sleep 10
########################################################################################################################################################
	#获取文件
	cd $pc_path
	rm -rf data/file/*
	rm -rf data/pcap_appid_temp/*
	rm -rf data/pcap_ips_temp/*
	cd $path
	bash getfile.sh file
	#根据下载的文件需求设置主要参数
	cd $pc_path
	if [ -e data/file/test ];then
		appid_key=""
		ips_key=""
		appid_key_fs=""
		ips_key_fs=""
		debug="test"
		type="`cat data/file/test`"
	elif [ -e data/file/ok ];then
		appid_key="f7a44f62-d361-4db9-a6ac-556007faf234"
		ips_key="faf4bf93-a33e-455b-9a32-c2736fbdafb0"
		appid_key_fs="08c71cec-15b3-4630-ab30-eafa6e6c2b10"
		ips_key_fs="1dd56c87-e54e-4151-8bc3-159c8477c79e"
		debug="formal"
		type="`cat data/file/ok`"
	else
		continue
	fi
	#删除http服务器上的上传文件
	cd $pc_path/data/file/
	filename="`ls *.zip`"
	curl -F "action=delete" -F "selection=$filename" -u huanglong:isFd00Wo http://172.28.249.90/test/file/
	sleep 1
	curl -F "action=delete"  -F "selection=ok" -u huanglong:isFd00Wo http://172.28.249.90/test/file/
	sleep 1
	curl -F "action=delete"  -F "selection=test" -u huanglong:isFd00Wo http://172.28.249.90/test/file/
	
	#特征库下发升级获取升级结果
	mkdir -p $pc_path/update/appid $pc_path/update/ips $pc_path/update/appid_back $pc_path/update/ips_back
	cd $pc_path/data/file/
	if [ -e app*.zip ];then
		key="$appid_key"
		key_fs="$appid_key_fs"
		type="appid"
		cd $path
		#bash update.sh appid $pc_path/data/file/app*zip
		bash test.sh appid $pc_path/data/file/app*zip
		line1="`cat $pc_path/update/appid/app-rules*.log|head -n 4|tail -n 1`"
		line2="`cat $pc_path/update/appid/app-rules*.log|tail -n 1`"			
		if [ "$line1" == "$line2" ];then
			#bash update.sh appid $pc_path/update/appid_back/app*zip
			#bash update.sh appid $pc_path/data/file/app*zip
			bash test.sh appid $pc_path/update/appid_back/app_signature_image_20220807.1404_with_lib_R3.zip
			bash test.sh appid $pc_path/data/file/app*zip
		fi	
		line1="`cat $pc_path/update/appid/app-rules*.log|head -n 4|tail -n 1`"
		line2="`cat $pc_path/update/appid/app-rules*.log|tail -n 1`"
		softwarever="`cat $pc_path/update/appid/app-rules*.log|head -n 3|tr '\n' ' '|awk -F '=' '{print $2}'`"	
		md5="`cat $pc_path/update/appid/app-rules*.log|grep "/root/app"|awk -F ' ' '{print $1}'`"
		version="`echo $line2`"
		free="`cat $pc_path/update/appid/app-rules*.log|grep "Mem:"`"	
		if [ "$line1" != "$line2" -a "$line2" != "00000000.0000" ];then	
			content="$softwarever\nThe name of the library to upgrade is $filename\nmd5 is $md5\n一、appid signature update success ! \nnow version is $version\n"
			bash send.sh message "$content$free" $key
			bash send_fs.sh message "$content" $key_fs
			bash send.sh file $pc_path/update/appid/app-rules*.log $key
			mkdir -p $pc_path/report/history/report_temp
			echo -e $content > $pc_path/report/history/report_temp/result.txt
			scp -r $pc_path/update/appid/app-rules*.log $pc_path/report/history/report_temp/
		else		
			content="$softwarever\nThe name of the library to upgrade is $filename\nmd5 is $md5\n一、appid signature update fail ! \nnow version is $version\n"
			bash send.sh message "$content$free" $key
			bash send_fs.sh message "$content" $key_fs

			bash send.sh file $pc_path/update/appid/app-rules*.log $key
			mkdir -p $pc_path/report/history/report_temp
			echo -e $content > $pc_path/report/history/report_temp/result.txt			
			scp -r $pc_path/update/appid/app-rules*.log $pc_path/report/history/report_temp/
			
			echo "This feature library is fail !" >> $pc_path/report/history/report_temp/result.txt
			report
			continue
		fi	
		work	
	elif [ -e ips*.zip ];then
		key="$ips_key"
		key_fs="$ips_key_fs"
		type="ips"
		cd $path
		#bash update.sh ips $pc_path/data/file/ips*zip
		bash test.sh ips $pc_path/data/file/ips*zip
		update_same="`cat $pc_path/update/ips/ips-rules*.log|grep -i "Same Version"`"
		if [ "$update_same" != "" ];then
			#bash update.sh ips $pc_path/update/ips_back/ips*zip
			#bash update.sh ips $pc_path/data/file/ips*zip
			bash test.sh ips $pc_path/update/ips_back/ips*zip
			bash test.sh ips $pc_path/data/file/ips*zip
		fi
		line1="`cat $pc_path/update/ips/ips-rules*.log|head -n 4|tail -n 1`"
		line2="`cat $pc_path/update/ips/ips-rules*.log|tail -n 1`"
		softwarever="`cat $pc_path/update/ips/ips-rules*.log|head -n 3|tr '\n' ' '|awk -F '=' '{print $2}'`"
		md5="`cat $pc_path/update/ips/ips-rules*.log|grep "/root/ips"|awk -F ' ' '{print $1}'`"
		update_err="`cat $pc_path/update/ips/ips-rules*.log|grep -i err`"
		update_wrong="`cat $pc_path/update/ips/ips-rules*.log|grep -i wrong`"
		free="`cat $pc_path/update/ips/ips-rules*.log|grep "Mem:"`"
		if [ "$line1" != "$line2"  -a "$line2" != "sig version: 00000000.0000"  ];then
			if [ "$update_err" == "" -a "$update_wrong" == "" ];then
				exception="no problem"
			else
				exception="there is something wrong"
			fi
			version="`cat $pc_path/update/ips/ips-rules*.log|grep "ips signature update success" |awk -F ' ' '{print $8}'`"
			rule="`cat $pc_path/update/ips/ips-rules*.log|grep "rules successfully"|awk -F '.' '{print $2}'|awk '$1=$1'`"			
			content="$softwarever\nThe name of the library to upgrade is $filename\nmd5 is $md5\n一、ips signature update success ! \nnow version is $version\n$rule\n$exception\n"
			bash send.sh message "$content$free" $key
			bash send_fs.sh message "$content" $key_fs
			bash send.sh file $pc_path/update/ips/ips-rules*.log $key
			mkdir -p $pc_path/report/history/report_temp
			echo -e $content > $pc_path/report/history/report_temp/result.txt
			scp -r $pc_path/update/ips/ips-rules*.log $pc_path/report/history/report_temp/
			bash send.sh message "Now packet playback verification on version $version" $key
			bash send_fs.sh message "Now packet playback verification on version $version\n" $key_fs
		else			
			version="`cat  $pc_path/update/ips/ips-rules*.log|head -n 4|tail -n 1|awk -F ' ' '{print $3}'`"
			
			content="$softwarever\nThe name of the library to upgrade is $filename\nmd5 is $md5\n一、ips signature update fail ! \nnow version is $version\n"
			bash send.sh message "$content" $key
			bash send_fs.sh message "$content" $key_fs
			bash send.sh file $pc_path/update/ips/ips-rules*.log $key
			mkdir -p $pc_path/report/history/report_temp
			echo -e $content > $pc_path/report/history/report_temp/result.txt			
			scp -r $pc_path/update/ips/ips-rules*.log $pc_path/report/history/report_temp/
			
			echo "This feature library is fail !" >> $pc_path/report/history/report_temp/result.txt
			report
			continue
		fi
		work
	else
		cd $path
		content="一、Use the original feature library !"
		version="original"
		if [ "$type" == "appid" ];then
			key="$appid_key"
			key_fs="$appid_key_fs"
		elif [ "$type" == "ips" ];then
			key="$ips_key"
			key_fs="$ips_key_fs"
		else
			continue
		fi
		bash send.sh message "$content" $key
		bash send_fs.sh message "$content" $key_fs
		mkdir -p $pc_path/report/history/report_temp				
		echo "$content" > $pc_path/report/history/report_temp/result.txt
		work
	fi
	report
########################################################################################################################################################
done

