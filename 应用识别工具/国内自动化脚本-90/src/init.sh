#!/bin/bash
type=$1
user=$2
ip="172.28.247.50"
passwd="Ruijie@123"
pc_ip="172.28.247.90"
pc_passwd="ruijie12345"
path="`pwd`"
cd ..
pc_path="`pwd`/update"
cd $path


if [ "$type" == "appid" ];then

	if [ "$user" == "root" ];then

		/usr/bin/expect <<-EOF
				set timeout 3
				spawn ssh $user@$ip
				expect "assword"
				send "$passwd\n"
				expect "firewall"
				send "sudo fpcmd fp app-id cfg enable cache false\n"
				expect "firewall"
				send "sudo fpcmd fp app-id cfg enable expect false\n"
				expect "firewall"
				send "sudo fpcmd fp app-id show application > /mnt/flash/appid-rules.txt\n"
				expect "firewall"
				send "sudo scp -r /mnt/flash/appid-rules.txt root@$pc_ip:$pc_path/$type/\n"
				expect "assword"
				send "$pc_passwd\n"
				expect "firewall"
				send "sudo fp-npfctl flows-flush\n"
				expect "firewall"
				send "exit\n"
				send "exit\n"
				interact
				expect eof
				EOF
		
	elif [ "$user" == "admin" ];then
	
		/usr/bin/expect <<-EOF
				set timeout 3
				spawn ssh $user@$ip
				expect "assword"
				send "$passwd\n"
				expect "firewall"
				send "cmd appid run \'app-id cache-enable false\'\n"
				expect "firewall"
				send "cmd appid run \'app-id expect-enable false\'\n"
				expect "firewall"
				send "flush nfp flows\n"
				expect "firewall"
				send "exit\n"
				send "exit\n"
				interact
				expect eof
				EOF
		
	else	

		/usr/bin/expect <<-EOF
				set timeout 3
				spawn ssh $user@$ip
				expect "assword"
				send "$passwd\n"
				expect "firewall"
				send "sudo ls\n"
				expect "assword"
				send "$passwd\n"
				expect "firewall"
				send "sudo fpcmd fp app-id cache-enable false\n"
				expect "firewall"
				send "sudo fpcmd fp app-id expect-enable false\n"
				expect "firewall"
				send "sudo fp-npfctl flows-flush\n"
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
				set timeout 3
				spawn ssh $user@$ip
				expect "assword"
				send "$passwd\n"
				expect "firewall"
				send "sudo fpcmd fp app-id cache-enable false\n"
				expect "firewall"
				send "sudo fpcmd fp app-id expect-enable false\n"
				expect "firewall"
				send "sudo sqlite3 /tmp/ips/ips_sig.db .dump > /mnt/flash/ips-rules.txt\n"
				expect "firewall"
				send "sudo scp -r /mnt/flash/ips-rules.txt root@$pc_ip:$pc_path/$type/\n"
				expect "assword"
				send "$pc_passwd\n"
				expect "firewall"
				send "sudo fpcmd fp ips debug pkt-debug off\n"
				expect "firewall"
				send "sudo fpcmd fp ips debug post-match off\n"
				expect "firewall"
				send "sudo fpcmd fp ips debug log on\n"
				expect "firewall"
				send "sudo fpcmd log-level-set 7\n"
				expect "firewall"
				send "sudo fpcmd log-type-set all off\n"
				expect "firewall"
				send "sudo fpcmd log-type-set APP_PARSER on\n"
				expect "firewall"
				send "sudo fpcmd log-type-set IPS on\n"
				expect "firewall"
				send "sudo fp-npfctl flows-flush\n"
				expect "firewall"
				send "exit\n"
				send "exit\n"
				interact
				expect eof
				EOF
	
	elif [ "$user" == "admin" ];then

		/usr/bin/expect <<-EOF
				set timeout 3
				spawn ssh $user@$ip
				expect "assword"
				send "$passwd\n"
				expect "firewall"
				send "cmd appid run \'app-id cache-enable false\'\n"
				expect "firewall"
				send "cmd appid run \'app-id expect-enable false\'\n"
				expect "firewall"
				send "cmd ips run \"debug pkt-debug off\"\n"
				expect "firewall"
				send "cmd ips run \"debug post-match off\"\n"
				expect "firewall"
				send "cmd ips run \"debug log on\"\n"
				expect "firewall"
				send "cmd debug-support fp exec \"log-level-set 7\"\n"
				expect "firewall"
				send "cmd debug-support fp exec \"log-type-set all off\"\n"
				expect "firewall"
				send "cmd debug-support fp exec \"log-type-set APP_PARSER on\"\n"
				expect "firewall"
				send "cmd debug-support fp exec \"log-type-set IPS on\"\n"
				expect "firewall"
				send "flush nfp flows\n"
				expect "firewall"
				send "exit\n"
				send "exit\n"
				interact
				expect eof
				EOF
	
	else	

		/usr/bin/expect <<-EOF
				set timeout 3
				spawn ssh $user@$ip
				expect "assword"
				send "$passwd\n"
				expect "firewall"
				send "sudo ls\n"
				expect "assword"
				send "$passwd\n"
				expect "firewall"
				send "sudo fpcmd fp app-id cache-enable false\n"
				expect "firewall"
				send "sudo fpcmd fp app-id expect-enable false\n"
				expect "firewall"
				send "sudo fpcmd fp ips debug pkt-debug off\n"
				expect "firewall"
				send "sudo fpcmd fp ips debug post-match off\n"
				expect "firewall"
				send "sudo fpcmd fp ips debug log on\n"
				expect "firewall"
				send "sudo fpcmd log-level-set 7\n"
				expect "firewall"
				send "sudo fpcmd log-type-set all off\n"
				expect "firewall"
				send "sudo fpcmd log-type-set APP_PARSER on\n"
				expect "firewall"
				send "sudo fpcmd log-type-set IPS on\n"
				expect "firewall"
				send "sudo fp-npfctl flows-flush\n"
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
