#!/bin/bash
pc_ip="172.28.247.90"
pc_user="root"
pc_passwd="ruijie12345"
z5100_ip="172.28.247.50"
z5100_user="root"
z5100_passwd="Ruijie@123"
z5100_hostname="firewall"
z5100_root_path="/root"

path="`pwd`"
cd ..
if [ -z "$3" ] ;then
	pc_path="`pwd`/update"
else
	pc_path="$3"
fi
cd $path

rm -rf $pc_path/$type/*.log

type="$1"
if [ "$type" == "appid" ];then

/usr/bin/expect <<-EOF
        set timeout 60
        spawn ssh $z5100_user@$z5100_ip
        expect "assword"
        send "$z5100_passwd\n"
        expect "$z5100_hostname"
        send "sudo rm -rf $z5100_root_path/app*.zip\n"
		expect "$z5100_hostname"
        send "scp -r $pc_user@$pc_ip:$2 ./\n"
        expect "assword"
        send "$pc_passwd\n"
		expect "$z5100_hostname"
        send "sudo cat /etc/os-release|head -n 1 > /mnt/flash/app-rules.log\n"
		expect "$z5100_hostname"
        send "sudo cat /etc/.release >> /mnt/flash/app-rules.log\n"
		expect "$z5100_hostname"
		send "sudo cat /etc/.releaseID >> /mnt/flash/app-rules.log\n"
		expect "$z5100_hostname"
        send "sudo fpcmd fp app-id show version >> /mnt/flash/app-rules.log\n"
		#expect "$z5100_hostname"
		#send "sudo echo >> /mnt/flash/app-rules.log\n"
		expect "$z5100_hostname"
		send "sudo free >> /mnt/flash/app-rules.log\n"
		expect "$z5100_hostname"
		#send "sudo journalctl -f -u fast-path|grep APP_IDY|grep -A 10000 \"Local signature database upgrading.\" >> /mnt/flash/app-rules.log &\n"
		send "sudo journalctl -f|grep fp-rte|grep APP_IDY|grep -A 10000 \"Local signature database upgrading.\" >> /mnt/flash/app-rules.log &\n"	
	expect "$z5100_hostname"
        send "sudo fpcmd fp app-id debug file on\n"
		expect "$z5100_hostname"
		send "sudo md5sum $z5100_root_path/app*.zip >> /mnt/flash/app-rules.log\n"
		expect "$z5100_hostname"
        send "sudo fpcmd fp app-id sig-update file_path $z5100_root_path/app*.zip\n"
        expect "$z5100_hostname"
        sleep 80
		send "killall journalctl\n"
		expect "$z5100_hostname"
		sleep 5
		send "sudo free >> /mnt/flash/app-rules.log\n"
		expect "$z5100_hostname"
        send "sudo fpcmd fp app-id show version >> /mnt/flash/app-rules.log\n"
		expect "$z5100_hostname"
		#send "sudo echo >> /mnt/flash/app-rules.log\n"
		#expect "$z5100_hostname"
		send "sudo scp -r /mnt/flash/app-rules.log $pc_user@$pc_ip:$pc_path/$type/\n"
        expect "assword"
        send "$pc_passwd\n"
        expect "$z5100_hostname"
        send "sudo rm -rf $z5100_root_path/app*.zip\n"
        send "exit\n"
        send "exit\n"
        interact
		expect eof
		EOF
		
elif [ "$type" == "ips" ];then

/usr/bin/expect <<-EOF
        set timeout 60
        spawn ssh $z5100_user@$z5100_ip
        expect "assword"
        send "$z5100_passwd\n"
        expect "$z5100_hostname"
        send "sudo rm -rf $z5100_root_path/ips*.zip\n"
		expect "$z5100_hostname"
        send "scp -r $pc_user@$pc_ip:$2 ./\n"
        expect "assword"
        send "$pc_passwd\n"
		expect "$z5100_hostname"
		send "sudo cat /etc/os-release|head -n 1 > /mnt/flash/ips-rules.log\n"
        expect "$z5100_hostname"
        send "sudo cat /etc/.release >> /mnt/flash/ips-rules.log\n"
		expect "$z5100_hostname"
        send "sudo cat /etc/.releaseID >> /mnt/flash/ips-rules.log\n"
        expect "$z5100_hostname"
		send "sudo fpcmd fp ips show sig-info|grep \"sig version\" >> /mnt/flash/ips-rules.log\n"
        expect "$z5100_hostname"
		send "sudo free >> /mnt/flash/ips-rules.log\n"
        expect "$z5100_hostname"
		send "md5sum $z5100_root_path/ips*.zip >> /mnt/flash/ips-rules.log\n"
        expect "$z5100_hostname"
        send "sudo fpcmd fp ips sig-update $z5100_root_path/ips*.zip\n"
        expect "$z5100_hostname"
        sleep 80
		send "sudo cat /mnt/flash/ips/log/ips-rules.log >>/mnt/flash/ips-rules.log\n"
        expect "$z5100_hostname"
		send "sudo free >> /mnt/flash/ips-rules.log\n"
		expect "$z5100_hostname"
		send "sudo fpcmd fp ips show sig-info|grep \"sig version\" >> /mnt/flash/ips-rules.log\n"
		expect "$z5100_hostname"
        send "sudo scp -r /mnt/flash/ips-rules.log $pc_user@$pc_ip:$pc_path/$type/\n"
        expect "assword"
        send "$pc_passwd\n"
        expect "$z5100_hostname"
        send "sudo rm -rf $z5100_root_path/ips*.zip\n"
        send "exit\n"
        send "exit\n"
        interact
		expect eof
		EOF
		
else

break

fi


