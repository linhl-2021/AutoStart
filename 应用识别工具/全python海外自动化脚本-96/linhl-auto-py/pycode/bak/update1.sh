#!/bin/bash
# pc_ip="172.28.249.86"
pc_ip="$1"
#pc_user="root"
pc_user="$2"
pc_passwd="ruijie12345"
# pc_passwd="$3"
# z3200_ip="172.28.247.83"
z3200_ip="$4"
# z3200_user="root"
z3200_user="$5"
# z3200_passwd="Ruijie@123"
z3200_passwd="$6"
# z3200_hostname="firewall"
z3200_hostname="$7"
# z3200_root_path="/root"
z3200_root_path="$8"

# path="`pwd`"
# cd ..
pc_path="${10}"
# if [ -z "$10" ] ;then
# 	pc_path="`pwd`/update"
# else
# 	pc_path="$10"
# fi
# cd $path
type="$9"
rm -rf $pc_path/$type/*.log

if [ "$type" == "appid" ];then

/usr/bin/expect <<-EOF
        set timeout 60
        spawn ssh $z3200_user@$z3200_ip
        expect "assword"
        send "$z3200_passwd\n"
        expect "$z3200_hostname"
        send "sudo rm -rf $z3200_root_path/app*.zip\n"
		expect "$z3200_hostname"
        send "scp -r $pc_user@$pc_ip:${11} ./\n"
        expect "assword"
        send "$pc_passwd\n"
		expect "$z3200_hostname"
        send "sudo cat /etc/os-release|head -n 1 > /mnt/flash/app-rules.log\n"
		expect "$z3200_hostname"
        send "sudo cat /etc/.release >> /mnt/flash/app-rules.log\n"
		expect "$z3200_hostname"
		send "sudo cat /etc/.releaseID >> /mnt/flash/app-rules.log\n"
		expect "$z3200_hostname"
        send "sudo fpcmd fp app-id show version >> /mnt/flash/app-rules.log\n"
		expect "$z3200_hostname"
		#send "sudo echo >> /mnt/flash/app-rules.log\n"
		#expect "$z3200_hostname"
		send "sudo free >> /mnt/flash/app-rules.log\n"
		expect "$z3200_hostname"
		#send "sudo journalctl -f -u fast-path|grep APP_IDY|grep -A 10000 \"Local signature database upgrading.\" >> /mnt/flash/app-rules.log &\n"
		send "sudo journalctl -f |grep fp-rte|grep APP_IDY|grep -A 10000 \"Local signature database upgrading.\" >> /mnt/flash/app-rules.log &\n"
		expect "$z3200_hostname"
        send "sudo fpcmd fp app-id debug file on\n"
		expect "$z3200_hostname"
		send "sudo md5sum $z3200_root_path/app*.zip >> /mnt/flash/app-rules.log\n"
		expect "$z3200_hostname"
        send "exit\n"
        send "exit\n"
        interact
		expect eof
		EOF
		
elif [ "$type" == "ips" ];then

/usr/bin/expect <<-EOF
        set timeout 60
        spawn ssh $z3200_user@$z3200_ip
        expect "assword"
        send "$z3200_passwd\n"
        expect "$z3200_hostname"
        send "sudo rm -rf $z3200_root_path/ips*.zip\n"
		expect "$z3200_hostname"
        send "scp -r $pc_user@$pc_ip:$2 ./\n"
        expect "assword"
        send "$pc_passwd\n"
		expect "$z3200_hostname"
		send "sudo cat /etc/os-release|head -n 1 > /mnt/flash/ips-rules.log\n"
        expect "$z3200_hostname"
        send "sudo cat /etc/.release >> /mnt/flash/ips-rules.log\n"
		expect "$z3200_hostname"
        send "sudo cat /etc/.releaseID >> /mnt/flash/ips-rules.log\n"
        expect "$z3200_hostname"
		send "sudo fpcmd fp ips show sig-info|grep \"sig version\" >> /mnt/flash/ips-rules.log\n"
        expect "$z3200_hostname"
		send "sudo free >> /mnt/flash/ips-rules.log\n"
        expect "$z3200_hostname"
		send "md5sum $z3200_root_path/ips*.zip >> /mnt/flash/ips-rules.log\n"
        expect "$z3200_hostname"
        send "sudo rm -rf $z3200_root_path/ips*.zip\n"
        send "exit\n"
        send "exit\n"
        interact
		expect eof
		EOF
		
else

break

fi


