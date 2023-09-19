#!/bin/bash
pc_ip="172.28.249.86"
pc_user="root"
pc_passwd="ruijie12345"
# z3200_ip="172.28.247.83"
z3200_ip="172.28.247.83"
z3200_user="root"
z3200_passwd="Ruijie@123"
z3200_hostname="firewall"
z3200_root_path="/root"

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
        spawn ssh $z3200_user@$z3200_ip
        expect "assword"
        send "$z3200_passwd\n"
        expect "$z3200_hostname"
		send "killall journalctl\n"
		expect "$z3200_hostname"
		sleep 5
		send "sudo free >> /mnt/flash/app-rules.log\n"
		expect "$z3200_hostname"
		# send "sudo fpcmd fp app-id sig-version >> /mnt/flash/app-rules.log\n"
        send "sudo fpcmd fp app-id show version >> /mnt/flash/app-rules.log\n"
		expect "$z3200_hostname"
		#send "sudo echo >> /mnt/flash/app-rules.log\n"
		#expect "$z3200_hostname"
		send "sudo scp -r /mnt/flash/app-rules.log $pc_user@$pc_ip:$pc_path/$type/\n"
        expect "assword"
        send "$pc_passwd\n"
        expect "$z3200_hostname"
        send "sudo rm -rf $z3200_root_path/app*.zip\n"
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
		send "sudo cat /mnt/flash/ips/log/ips-rules.log >>/mnt/flash/ips-rules.log\n"
        expect "$z3200_hostname"
		send "sudo free >> /mnt/flash/ips-rules.log\n"
		expect "$z3200_hostname"
		send "sudo fpcmd fp ips show sig-info|grep \"sig version\" >> /mnt/flash/ips-rules.log\n"
		expect "$z3200_hostname"
        send "sudo scp -r /mnt/flash/ips-rules.log $pc_user@$pc_ip:$pc_path/$type/\n"
        expect "assword"
        send "$pc_passwd\n"
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


