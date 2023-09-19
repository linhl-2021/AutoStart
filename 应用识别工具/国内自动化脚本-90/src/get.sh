#!/bin/bash
type=$1
user=$2
pc_ip="172.28.247.90"
pc_passwd="ruijie12345"
Z5100_ip="172.28.247.50"
Z5100_passwd="Ruijie@123"

path=`pwd`
cd ..
pc_path="`pwd`/report/Z5100_$1"
cd $path

if [ "$type" == "appid" ];then

	if [ "$user" == "root" ];then
	
		/usr/bin/expect <<-EOF
				set timeout 10
				spawn ssh $user@$Z5100_ip
				expect "assword"
				send "$Z5100_passwd\n"
				expect "firewall"
				send "sudo fp-npfctl cookie 3 > $type.txt\n"
				expect "firewall"
				send "sudo fp-npfctl cookie 3 >> $type.txt\n"
				expect "firewall"
				send "sudo fp-npfctl cookie 3 >> $type.txt\n"
				expect "firewall"
				send "sudo scp -r $type.txt $user@$pc_ip:$pc_path/\n"
				expect "assword"
				send "$pc_passwd\n"
				expect "firewall"
				send "sudo rm -rf $type.txt\n"
				#expect "firewall"
				#send "sudo fp-npfctl flows-flush\n"
				expect "firewall"
				send "exit\n"
				send "exit\n"
				interact
				expect eof
				EOF
		
	elif [ "$user" == "admin" ];then
	
		/usr/bin/expect <<-EOF
				set timeout 10
				spawn ssh $user@$Z5100_ip
				expect "assword"
				send "$Z5100_passwd\n"
				expect "firewall"
				send "show nfp cookie pid 3\n"
				expect "firewall"
				sleep 1
				send " \n"
				#expect "firewall"
				#send "flush nfp flows\n"
				expect "firewall"
				send "exit\n"
				send "exit\n"
				interact
				expect eof
				EOF
		
	else	
	
		/usr/bin/expect <<-EOF
				set timeout 10
				spawn ssh $user@$Z5100_ip
				expect "assword"
				send "$Z5100_passwd\n"
				expect "firewall"
				send "sudo ls\n"
				expect "assword"
				send "$Z5100_passwd\n"
				expect "firewall"
				send "sudo fp-npfctl cookie 3 > $type.txt\n"
				expect "firewall"
				send "sudo fp-npfctl cookie 3 >> $type.txt\n"
				expect "firewall"
				send "sudo fp-npfctl cookie 3 >> $type.txt\n"
				expect "firewall"
				send "sudo scp -r $type.txt $user@$pc_ip:$pc_path/\n"
				expect "assword"
				send "$pc_passwd\n"
				expect "firewall"
				send "sudo rm -rf $type.txt\n"
				#expect "firewall"
				#send "sudo fp-npfctl flows-flush\n"
				expect "firewall"
				send "exit\n"
				send "exit\n"
				interact
				expect eof
				EOF
	
	fi

elif [ "$type" == "ips" ];then
	
	if [ "$user" == "root" ];then

		/usr/bin/expect <<-EOF
				set timeout 20
				spawn ssh $user@$Z5100_ip
				expect "assword"
				send "$Z5100_passwd\n"
				expect "firewall"
				#send "echo `date` > time_check\n"
				#expect "firewall"
				send "sudo journalctl |grep IPS|tail -n 300 > $type.txt\n"
				expect "firewall"
				#send "echo `date` >> time_check\n"
				#expect "firewall"
				send "sudo scp -r $type.txt $user@$pc_ip:$pc_path/\n"
				expect "assword"
				send "$pc_passwd\n"
				expect "firewall"
				send "sudo fpcmd log-level-set 7\n"
				expect "firewall"
				send "sudo rm -rf $type.txt\n"
				#expect "firewall"
				#send "sudo fp-npfctl flows-flush\n"
				expect "firewall"
				send "echo `date` >> time_check\n"
				expect "firewall"
				send "exit\n"
				send "exit\n"
				interact
				expect eof
				EOF

	elif [ "$user" == "admin" ];then

		/usr/bin/expect <<-EOF
				set timeout 10
				spawn ssh $user@$Z5100_ip
				expect "assword"
				send "$Z5100_passwd\n"
				expect "firewall"
				send "cmd debug-support fp exec \"log-level-set 7\"\n"
				expect "firewall"
				send "show log max-lines 100 | match sid\n"
				expect "firewall"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				sleep 1
				send " \n"
				expect "firewall"
				send "exit\n"
				send "exit\n"
				interact
				expect eof
				EOF
	
	else	

		/usr/bin/expect <<-EOF
				set timeout 10
				spawn ssh $user@$Z5100_ip
				expect "assword"
				send "$Z5100_passwd\n"
				expect "firewall"
				send "sudo ls\n"
				expect "assword"
				send "$Z5100_passwd\n"
				expect "firewall"
				#send "sudo journalctl -n 100 > $type.txt\n"
				send "sudo journalctl |grep IPS|tail -n 100 > $type.txt\n"
				expect "firewall"
				send "sudo scp -r $type.txt $user@$pc_ip:$pc_path/\n"
				expect "assword"
				send "$pc_passwd\n"
				expect "firewall"
				send "sudo fpcmd log-level-set 7\n"
				expect "firewall"
				send "sudo rm -rf $type.txt\n"
				#expect "firewall"
				#send "sudo fp-npfctl flows-flush\n"
				expect "firewall"
				send "exit\n"
				send "exit\n"
				interact
				expect eof
				EOF
	
fi
	
else

	break
	
fi
