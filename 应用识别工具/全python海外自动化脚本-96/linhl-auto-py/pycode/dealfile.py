import codecs
import configparser
import datetime
import ftplib
import json
import locale
import os
import random
import re
import shutil
import socket
import struct
import subprocess
import sys
import time
import zipfile
import paramiko
import requests
from log_module import logger
import pexpect
from config import Config
from updatestatue import run_update_test
import os
import shutil
import ipaddress
import random
from urllib.parse import quote
from smb.SMBConnection import SMBConnection

def randip(ip):
    net = ipaddress.IPv4Network(ip)
    ip = str(random.choice(list(net.hosts())))
    return ip
def randipV6(ip):
    rand1 = random.randint(1, 2000)
    ip = ip+str(rand1)
    return ip

# ip = randip("100.100.0.0/16")
# ip = randipV6("2001:db8:1234::")
# logger.debug(ip)
def shell_command(command):
    try:
        # 执行命令并等待结束
        logger.debug(f"执行命令： {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True)

        # 输出命令执行的标准输出和标准错误
        logger.debug(result.stdout.decode())
        logger.debug(result.stderr.decode())

    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，则输出相关信息
        logger.debug(f'命令执行失败！错误信息：{e.stderr.decode()}')
def get_command_response(command):
    logger.debug(f"执行命令： {command}")
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    return(output.strip())

def create_dir_bytime(path):
    # 获取当前日期和时间
    now = datetime.datetime.now()
    # 将日期和时间转换为指定格式的字符串
    timestamp = now.strftime('%m%d_%H%M')

    # 构造目录路径
    directory=os.path.join(path, timestamp)

    # 创建目录
    try:
        os.mkdir(directory)
        return directory
    except OSError as e:
        return e

def str_match(str,pattern):
    match = re.search(pattern, str)
    if match:
        str = match.group(1)
    else:
        str ="000000"
    return str

def file_match(file,pattern):
    with open(file, 'r') as f:
        # 使用生成器表达式逐行搜索包含关键字的行
        matching_line = next((line for line in f if pattern in line), None)

    if matching_line:
        # 处理匹配的行
        return matching_line
    else:
        # 没有找到匹配的行
        return 'No matching line found.'

def network_init(config):
    command1=f"ifconfig {config.linux_c_eth} up"
    command2=f"ifconfig {config.linux_s_eth} up"
    command3=f"ifconfig {config.linux_c_eth} mtu 1600"
    command4=f"ifconfig {config.linux_s_eth} mtu 1600"
    command5=f"ifconfig {config.linux_c_eth} {config.linux_c_ip} netmask 255.255.255.0"
    command6=f"ifconfig {config.linux_c_eth} {config.linux_s_ip} netmask 255.255.255.0"
    command7=f"ifconfig {config.linux_c_eth} {config.linux_c_ip} netmask 255.255.255.0"
    command8=f"ifconfig {config.linux_c_eth} inet6 add {config.linux_c_ip_V6}/112"
    command9=f"ifconfig {config.linux_s_eth} inet6 add {config.linux_s_ip_V6}/112"

    commands = [command1,command2,command3,command4,command5,command6,command7,command8,command9]
    for cmd in commands:
        shell_command(cmd)

def get_flow(type,config,frontpath):
    flow_log_path=os.path.join(frontpath,"report",type)
    log_file = config.log_command_path
    command=f"ssh {config.firewalld_shell_user}@{config.firewalld_ip}"
    if type == "appid":
        if config.firewalld_shell_user == "root":
            logger.debug("应用识别执行root账号命令")
            command1=f"sudo fp-npfctl cookie 3 > {type}.txt"
            command2=f"sudo fp-npfctl cookie 3 >> {type}.txt"
            command3=f'sudo fp-npfctl cookie 3 >> {type}.txt'
            command4=f"sudo scp -r {type}.txt {config.linux_user}@{config.linux_ip}:{flow_log_path}/"
            command5=f"sudo rm -rf {type}.txt"
            command6="sudo fp-npfctl flows-flush"
            command7="exit"
            commands = [command1,command2, command3, command4, command5, 
                command6, command7]
        elif config.firewalld_shell_user == "admin":
            command1="show nfp cookie pid 3"
            command2=''
            command3="flush nfp flows"
            command4="exit"
            commands = [command1,command2, command3, command4]
        else:
            command1="sudo ls"
            command2=f"sudo fp-npfctl cookie 3 > {type}.txt"
            command3=f"sudo fp-npfctl cookie 3 > {type}.txt"
            command4=f"sudo fp-npfctl cookie 3 > {type}.txt"
            command5=f"sudo scp -r {type}.txt {config.linux_user}@{config.linux_ip}:{flow_log_path}/"
            command6=f"sudo rm -rf {type}.txt"
            command7="sudo fp-npfctl flows-flush"
            command8="exit"
            commands = [command1,command2, command3, command4, command5,command6,command7,command8]
    

    elif type == "ips":
        if config.firewalld_shell_user == "root":
            logger.debug("ips执行root账号命令")
            command1=f"echo `date` > time_check"
            command2=f"sudo journalctl |grep IPS|tail -n 300 >  {type}.txt"
            command3=f'echo `date` >> time_check'
            command4=f"sudo scp -r {type}.txt {config.linux_user}@{config.linux_ip}:{flow_log_path}/"
            command5=f"sudo fpcmd log-level-set 7"
            command6=f"sudo rm -rf {type}.txt"
            command6=f"echo `date` >> time_check"
            command7="sudo fp-npfctl flows-flush"
            command8="exit"
            commands = [command1,command2, command3, command4, command5, 
                command6,command7,command8]
        elif config.firewalld_shell_user == "admin":
            command1="cmd debug-support fp exec \"log-level-set 7\""
            command2="show log max-lines 100 | match sid"
            command3="flush nfp flows"
            command4="exit"
            commands = [command1,command2, command3, command4]
        else:
            command1="sudo ls"
            command2=f"sudo fp-npfctl cookie 3 > {type}.txt"
            command3=f"sudo fp-npfctl cookie 3 > {type}.txt"
            command4=f"sudo fp-npfctl cookie 3 > {type}.txt"
            command5=f"sudo scp -r {type}.txt {config.linux_user}@{config.linux_ip}:{flow_log_path}/"
            command6=f"sudo rm -rf {type}.txt"
            command7="sudo fp-npfctl flows-flush"
            command8="exit"
            commands = [command1,command2, command3, command4, command5,command6,command7,command8]

    

    if "DEBUG" in config.Level:
        child = pexpect.spawn(command, encoding='utf-8', logfile=open(log_file, 'a'),timeout=10)
    else:
        child = pexpect.spawn(command,encoding='utf-8',timeout=10)
    logger.debug("执行命令为： "+command)
    output_index = child.expect([".*yes/no.* ", "password:", pexpect.EOF, pexpect.TIMEOUT])
    # Check which output was matched and execute the next command accordingly
    if output_index == 0:
        logger.debug("Received 1, executing next yes")
        child.sendline("yes")
        output_index = child.expect(["password:", pexpect.EOF, pexpect.TIMEOUT])
        if output_index == 0:
            logger.debug("输入防火墙密码： "+config.firewalld_shell_passwd)
            child.sendline(config.firewalld_shell_passwd)         
            while True:
                index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                if index == 0:  # 子进程输出结束符
                    logger.debug("命令执行结束"+command)
                    break
                elif index == 1:  # 子进程输出超时
                    logger.debug("命令执行超时"+command)
                    break
                else:  # 正常输出
                    output_line = child.before.strip()
                    logger.debug(output_line)
    elif output_index == 1:
        logger.debug("输入防火墙密码： "+config.firewalld_shell_passwd)
        child.sendline(config.firewalld_shell_passwd)
        while True:
            index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
            if index == 0:  # 子进程输出结束符
                logger.debug("命令执行结束"+command)
                break
            elif index == 1:  # 子进程输出超时
                logger.debug("命令执行超时"+command)
                break
            else:  # 正常输出
                output_line = child.before.strip()
                logger.debug(output_line)
    command999 = "kill -9 $(ps -ef | grep root | grep pts |grep -v `echo ${SSH_TTY:5}` |grep -v bash | awk '{print $2}')"
    commands.insert(0,command999)
    for cmd in commands:
        if "flows-flush" in cmd:
            child.timeout = 2
        child.sendline(cmd)
        output_index = child.expect([".*yes/no.*", ".*password:",'.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT])
        if ("scp" in cmd) or ("ssh" in cmd) :
            if output_index == 0:
                logger.debug(f"Received 1, executing next {cmd}")
                child.sendline("yes")
                output_index = child.expect([".*word:", pexpect.EOF, pexpect.TIMEOUT])
                if output_index == 0:
                    logger.debug("输入Linux密码： "+config.linux_passwd)
                    child.sendline(config.linux_passwd)
                    while True:
                        index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                        if index == 0:  # 子进程输出结束符
                            logger.debug("命令执行结束"+cmd)
                            break
                        elif index == 1:  # 子进程输出超时
                            logger.debug("命令执行超时"+cmd)
                            break
                        else:  # 正常输出
                            output_line = child.before.strip()
                            logger.debug(output_line)
            elif output_index == 1:
                logger.debug("输入linux密码： "+config.linux_passwd)
                child.sendline(config.linux_passwd)
                while True:
                    index = child.expect([".*firewall.*",pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                    if index == 0:  # 子进程输出结束符
                        logger.debug("命令执行结束"+cmd)
                        break
                    elif index == 1:  # 子进程输出超时
                        logger.debug("命令执行超时"+cmd)
                        continue
                    else:  # 正常输出
                        output_line = child.before.strip()
                        logger.debug(output_line)
            elif output_index == 2:
                logger.debug(f"666666： {str(child.before.strip())}")
            else:
                logger.debug("Command failed or terminated before expected output was received")
        
        logger.debug(f'{output_index}  {cmd}') 
    child.close()


def replay_pcap(type,report_all_path,bigpcap,temp_path,no,config,frontpath):
    command4=f"tcpreplay -c {temp_path}/temp.cach -i {config.linux_c_eth} -I {config.linux_s_eth} -l 1 -p 300 {temp_path}/ok.pcap"
    for filename in os.listdir(report_all_path):
        file_path = os.path.join(report_all_path, filename)
        if os.path.isdir(file_path):
            for subfile in os.listdir(file_path):
                file_child_path = os.path.join(file_path, subfile)
                len=os.path.getsize(file_child_path)
                packet_number=os.path.getsize(file_path)
                logger.debug(file_child_path)
                command1=f"tcprewrite --enet-vlan=del --infile={file_child_path} --outfile={temp_path}/temp.pcap"
                if ":" not in subfile:
                    logger.debug("ipv4")
                    ip1=randip(config.ip_c_segment)
                    ip2=randip(config.ip_s_segment)    
                    command2=f"tcpprep --auto=client --cachefile={temp_path}/temp.cach --pcap={temp_path}/temp.pcap"   
                    command3=f"tcprewrite -m 1600 -C -e {ip1}:{ip2} --enet_smac={config.linux_c_mac},{config.linux_s_mac} \
                    --enet_dmac={config.firewalld_c_mac},{config.firewalld_s_mac} -c {temp_path}/temp.cach -i \
                    {temp_path}/temp.pcap -o {temp_path}/ok.pcap"   
                    logger.debug(f"replay: bigpcap {no} bigpcap文件名： {bigpcap} smallpcap文件路径： {file_child_path} smallpcap大小：{len}B client:{ip1} server:{ip2}")
                    shell_command(command1)
                    shell_command(command2)
                    shell_command(command3)
                    shell_command(command4)
                    
                else:
                    logger.debug("ipv6")
                    ip1=randipV6(config.ip_c_segmentv6)
                    ip2=randipV6(config.ip_s_segmentv6)
                    command2=f"tcpprep --port --cachefile={temp_path}/temp.cach --pcap={temp_path}/temp.pcap"   
                    command3=f"tcprewrite -m 1600 -C -e [{ip1}]:[{ip2}] --enet_smac={config.linux_c_mac},{config.linux_s_mac} \
                    --enet_dmac={config.firewalld_c_mac},{config.firewalld_s_mac} -c {temp_path}/temp.cach -i \
                    {temp_path}/temp.pcap -o {temp_path}/ok.pcap"   
                    logger.debug(f"replay: bigpcap {no} bigpcap文件名： {bigpcap} smallpcap文件路径： {file_child_path} smallpcap大小：{len}B client:{ip1} server:{ip2}")
                    shell_command(command1)
                    shell_command(command2)
                    shell_command(command3)
                    shell_command(command4)
                
                get_flow(type,config,frontpath)
                #/tcp_syn/192.168.22.3_54133_59.111.214.54_80_1676425630.pcap
                #192.168.22.3_54133_59.111.214.54_80_1676425630.pcap
                pcap=file_child_path.split('/')[-1]
                protocol_type=file_child_path.split('/')[-2]
                if "udp" in protocol_type:
                    protocol_type = "udp"
                else:
                    protocol_type = "tcp"
                srcport=pcap.split('_')[1]
                dstport=pcap.split('_')[3]
                bigpcap_sid=bigpcap.split('_')[0]
                #/home/release/linhl/linhl-auto-py/report/appid/appid.txt
                flow_path = os.path.join(frontpath,"report",type, f"{type}.txt")
                report_type_path=os.path.join(frontpath,"report",type)
                rule_path=os.path.join(frontpath,"update",type)   
                if os.path.exists(flow_path):
                    hitnum=0
                    sid_fir="0"
                    sid_sec="0"
                    with open(flow_path, 'r') as file:
                        for line in file:
                            if ip1 in line and ip2 in line and srcport in line and dstport in line :
                                hitnum +=1
                                logger.debug(f"命中流{line}")
                                if type=="appid":
                                    sid=re.split(r"\s+", line)[4]
                                    sid_fir=sid
                                    if sid_fir=="0-0-0-0" or sid_fir==sid_sec:
                                        continue
                                    else:
                                        sid_sec=sid
                                        command=f"cat {rule_path}/*rules.txt |grep {sid}|awk -F ' ' '{{print $1}}'"
                                        name=get_command_response(command)
                                        logger.debug(f"命中流{hitnum} 文件名： {bigpcap} 小包： {file_child_path}   协议 {protocol_type} 源端口 {srcport} 目的端口： {dstport} sid：{sid} name {name} bigpcap_sid: {bigpcap_sid}")
                                        if sid==bigpcap_sid:
                                            command=f"echo {bigpcap}#{pcap}#{len}#{protocol_type}#{sid}#{name}#yes >> {report_type_path}/log.csv"
                                            shell_command(command)
                                            terminal=bigpcap.lower().split('@')[1]
                                            if "android" in terminal or "iphone" in terminal or "pc" in terminal:
                                                terminal=terminal
                                            else:
                                                terminal="err"
                                            
                                            other=bigpcap.split('@')[2]+"@"+bigpcap.split('@')[3]
                                            command=f"cat {rule_path}/*rules.txt |grep  {bigpcap_sid}|awk -F ' ' '{{print $1}}'"
                                            name_final=get_command_response(command)
                                            if packet_number>0:
                                                command=f"scp -r {file_child_path} {report_type_path}/only{sid}_{name_final}@{terminal}@{other}"
                                                shell_command(command)
                                            logger.debug(f"terminal: {terminal} other: {other} name_final {name_final}")
                                        else:
                                            command=f"echo {bigpcap}#{pcap}#{len}#{protocol_type}#####no >> {report_type_path}/log.csv"
                                            shell_command(command)
                                        
                                        
                                elif type=="ips":
                                    sid=str_match(line,r"sid\((\d+)\)")
                                    if sid =="000000":
                                        continue
                                    #INSERT INTO signatures VALUES(4390914,'D-Link DSL-526B、DSL-2780B、DSL-2640B 路由器***dnscfg*** DNS 劫持漏洞 (ExploitDb-37237)','D-Link dsl-526b, dsl-2780b, dsl-2640b router * * * dnscfg * * * DNS hijacking vulnerability (exploitdb-37237)','server',2,'alert',1,'欺骗攻击','Spoofing Attack','中间人攻击','Man-in-the-middle Attack','HTTP',replace('D-Link DSL-526B\nD-Link DSL-2780B\nD-Link DSL-2640B','\n',char(10)),'Linux',0,0,0,'dlink');
                                    
                                    command=f"cat {rule_path}/*rules.txt | grep {sid} | awk -F \",'\" '{{print $1\"\\047,\"$2\",\"$6\",\"$7\",\"}}' | awk -F \"',\" '{{print \"【\"$3\"-\"$4\"】\"$2}}'"
                                    name=get_command_response(command)
                                    logger.debug(f"命中流{hitnum} 文件名： {bigpcap} 小包： {file_child_path}   协议 {protocol_type} 源端口 {srcport} 目的端口： {dstport} sid：{sid} name {name}")

                                else:
                                    logger(f'不支持类型： {type}')
                #/home/release/linhl/linhl-auto-py/update/appid/app-rules.txt
                    file.close()
                         
                
        else:
            command1=f"tcprewrite --enet-vlan=del --infile={file_path} --outfile={temp_path}/temp.pcap"
            len=os.path.getsize(file_path)
            if ":" not in filename:
                logger.debug("ipv4")
                ip1=randip(config.ip_c_segment)
                ip2=randip(config.ip_s_segment)  
                logger.debug(f"replay: bigpcap {no} 文件名： {bigpcap} 文件路径： {file_path} 大小：{len/1024:.2f}k client:{ip1} server:{ip2}")
                command2=f"tcpprep --auto=client --cachefile={temp_path}/temp.cach --pcap={temp_path}/temp.pcap"   
                command3=f"tcprewrite -m 1600 -C -e {ip1}:{ip2} --enet_smac={config.linux_c_eth},{config.linux_s_eth} \
                --enet_dmac={config.firewalld_c_mac},{config.firewalld_s_mac} -c {temp_path}/temp.cach -i \
                {temp_path}/temp.pcap -o {temp_path}/ok.pcap" 
                shell_command(command1)
                shell_command(command2)
                shell_command(command3)
                shell_command(command4)
                get_flow(type,config,frontpath)
            else:
                logger.debug("ipv6")
                ip1=randipV6(config.ip_c_segmentv6)
                ip2=randipV6(config.ip_s_segmentv6)
                logger.debug(f"replay: bigpcap {no} 文件名： {bigpcap} 文件路径： {file_path} 大小：{len/1024:.2f}k client:{ip1} server:{ip2}")
                command2=f"tcpprep --port --cachefile={temp_path}/temp.cach --pcap={temp_path}/temp.pcap"   
                command3=f"tcprewrite -m 1600 -C -e [{ip1}]:[{ip2}] --enet_smac={config.linux_c_eth},{config.linux_s_eth} \
                    --enet_dmac={config.firewalld_c_mac},{config.firewalld_s_mac} -c {temp_path}/temp.cach -i \
                    {temp_path}/temp.pcap -o {temp_path}/ok.pcap"   
                shell_command(command1)
                shell_command(command2)
                shell_command(command3)
                shell_command(command4)
                get_flow(type,config,frontpath)

    


def del_space(path):
    file_list = os.listdir(path)
    for filename in file_list:
        if (" " in filename ) or (" " in filename ):
            print(filename)
            basename, extension = os.path.splitext(filename)
            print(basename + "===="+extension)
            basename=basename.strip()
            basename = basename.replace(' ', '-')
            basename = basename.replace(' ', '-')
            basename = basename.replace('（', '(')
            basename = basename.replace('）', ')')
            os.rename(path+"/"+filename, path+"/"+basename+".pcap")

def report(pc_path, type, version, equipment, key_fs):
    # Change directory to the report history folder
    os.chdir(os.path.join(pc_path, 'report', 'history'))
    
    # Generate timestamp string
    time = datetime.datetime.now().strftime('%Y%m%d%H%M')
    
    # Rename temporary report file with timestamp
    temp_report = 'report_temp'
    new_report_name = f'report_{type}_{version}_{time}'
    os.rename(temp_report, new_report_name)
    
    # Zip report file with timestamp
    zip_path = f'{new_report_name}.zip'
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(new_report_name)
    
    # Upload zipped report file using Curl
    url = f'http://172.28.249.90/test/z-linhl/{equipment}/report/{type}/'
    data = {'action': 'upload'}
    files = {'filename': (zip_path, open(zip_path, 'rb'))}
    auth = ('linhuilong', 'linhuilong')
    response = requests.post(url, data=data, files=files, auth=auth)

def remove(file_path):
    try:
        # 尝试删除指定文件
        os.remove(file_path)
        logger.debug(f'成功删除文件：{file_path}')
    except OSError as e:
        # 如果出现异常，则打印错误信息
        logger.debug(f'错误：无法删除文件 {file_path}，原因是 {e}')

def send_message(msg,config):
    key=config.feishu_appid_key_fs
    data = {
        "msg_type": "text",
        "content": {"text": msg}
    }
    headers = {'Content-Type': 'application/json'}
    send_url=f"https://open.feishu.cn/open-apis/bot/v2/hook/{key}"
    logger.debug("飞书url： "+send_url)
    response = requests.post(send_url, headers=headers, data=json.dumps(data))
    logger.debug(response.json())
    return response.json()

# config=Config()
# msg="降级需要的特征库不存在，请上传到 /home/linhl/linhl-auto-py/update/appid_back/app_signature_image_20220807.1404_with_lib_R3.zip"
# send_message(msg,config)
# Define the function to send files
def send_file(file_url,key):
    data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "content": [
                        [
                            {
                                "tag": "a",
                                "text": "请查看测试报告",
                                "href": file_url
                            },
                            {
                                "tag": "at",
                                "user_id": "all"
                            }
                        ]
                    ]
                }
            }
        }
    }
    headers = {'Content-Type': 'application/json'}
    send_url=f"https://open.feishu.cn/open-apis/bot/v2/hook/{key}"
    response = requests.post(send_url, headers=headers, data=json.dumps(data))
    return response.json()

def dealfile(frontpath):
    logger.debug("frontpath路径： "+frontpath)
    #下载的文件存放路径
    temp = os.path.join(frontpath, "temp/")
    data_file_path = os.path.join(frontpath, "data", "file/")
    data_pcapAppid_path = os.path.join(frontpath, "data", "pcap_appid/")
    data_pcapAppidB_path = os.path.join(frontpath, "data", "pcap_appid_b/")
    data_pcapAppidTemp_path = os.path.join(frontpath, "data", "pcap_appid_temp/")
    data_pcapIpsPath = os.path.join(frontpath, "data", "pcap_ips/")
    data_pcapIpsB_path = os.path.join(frontpath, "data", "pcap_ips_b/")
    data_pcapIpsTemp_path = os.path.join(frontpath, "data", "pcap_ips_temp/")
    report_history_reportTemp_path = os.path.join(frontpath, "report", "history","report_temp/")
    report_appid_temp_path = os.path.join(frontpath, "report","appid","temp/")
    report_appid_all_path = os.path.join(frontpath, "report","appid","all/")
    report_appid_bigpcap_path = os.path.join(frontpath, "report","appid","bigpcap/")
    report_appid_only_path = os.path.join(frontpath, "report","appid","only/")
    report_ips_temp_path = os.path.join(frontpath, "report","ips","temp/")
    report_ips_all_path = os.path.join(frontpath, "report","ips","all/")
    report_ips_bigpcap_path = os.path.join(frontpath, "report","ips","bigpcap/")
    report_ips_only_path = os.path.join(frontpath, "report","ips","only/")
    update_appid_path = os.path.join(frontpath, "update","appid/")
    update_appidB_path = os.path.join(frontpath, "update","appid_back/")
    update_ips_path = os.path.join(frontpath, "update","ips/")
    update_ipsB_path = os.path.join(frontpath, "update","ips_back/")

    dirs_to_create=[temp,data_file_path,data_pcapAppid_path,data_pcapAppidB_path,data_pcapAppidTemp_path,
                    data_pcapIpsPath,data_pcapIpsB_path,data_pcapIpsTemp_path,report_history_reportTemp_path,
                    report_appid_temp_path,report_appid_all_path,report_appid_bigpcap_path,
                    report_appid_only_path,report_ips_temp_path,report_ips_all_path,report_ips_bigpcap_path,
                    report_ips_only_path,update_appid_path,update_appidB_path,update_ips_path,update_ipsB_path]

    # 创建所有目录，如果目录已经存在则跳过
    for dir in dirs_to_create:
        if not os.path.exists(dir):
            os.makedirs(dir)

    # 删除所有目录下的文件（但保留子目录）
    for dir in dirs_to_create:
        # logger.debug(dir)
        if "_b" not in dir and "file" not in dir :
            shutil.rmtree(dir)
            os.mkdir(dir)


def getfile(type,config,frontpath):
    #下载的文件存放路径
    file_path = os.path.join(frontpath, "data", "file")
    pcap_appid_temp_path = os.path.join(frontpath, "data", "pcap_appid_temp")
    pcap_ips_temp_path = os.path.join(frontpath, "data", "pcap_ips_temp")
    
    command=""
    if type == "file":
        command = f"wget -c -r -np -nd -nH -R html,tmp --no-http-keep-alive --http-user={config.hfs_user} \
        --http-password={config.hfs_passwd} {config.hfs_file_url} -P {file_path}"
    elif type == "appid":
        command =f"wget -c -r -np -nd -nH -R index.html -R index.html.tmp \
        --no-http-keep-alive --http-user={config.hfs_user} \
        --http-password={config.hfs_passwd} {config.hfs_pcap_appid_url} -P {pcap_appid_temp_path}"
    elif type == "ips":
        command =f"wget -c -r -np -nd -nH -R index.html -R index.html.tmp --no-http-keep-alive \
            --http-user={config.hfs_user} --http-password={config.hfs_passwd} \
                {config.hfs_pcap_ips_url} -P {pcap_ips_temp_path}"
    else:
        logger.debug("文件内容错误")     
        return  command 

    # 执行命令
    logger.debug("执行命令为："+str(command))
    shell_command(command)
#下载ftp文件
def ftp_get_file(type,config,frontpath):
    ftp = ftplib.FTP()
    ftp.connect(config.ftp_ip, int(config.ftp_port))
    ftp.login(config.ftp_user, config.ftp_passwd)
    ftp.encoding = 'gbk'
    if type == "file":
        ftp_file_path = config.ftp_file_url
        local_file_path=os.path.join(frontpath,"data","file/")
    elif type == "appid":
        ftp_file_path = config.ftp_pcap_appid_url
        local_file_path=os.path.join(frontpath,"data",f"pcap_{type}_temp/")
    elif type == "ips":
        ftp_file_path = config.ftp_pcap_ips_url
        local_file_path=os.path.join(frontpath,"data",f"pcap_{type}_temp/")
    else:
        logger.error(f"不支持类型： {type}")
        ftp_file_path=""
    ftp.cwd(ftp_file_path)
    try:
        filenames = ftp.nlst()
        logger.debug(f"下载文件为： {filenames}")
        # 遍历文件列表并下载每个文件
        for filename in filenames:
            logger.debug(filename)

            with open(local_file_path+filename, 'wb') as f:
                ftp.retrbinary('RETR %s' % filename, f.write)

    except ftplib.error_perm as e:
        if '550' in str(e):
            logger.debug('file does not exist' )
            ftp.quit()
            return
        else:
            logger.debug(e)
    shell_command(f"rm -rf {local_file_path}/descript.ion")
    ftp.quit()
#删除ftp文件
def ftp_del_file(frontpath,config):
    logger.debug("删除ftp目录文件")
    os.chdir(frontpath)
    files = os.listdir("data/file/")
    ftp = ftplib.FTP()
    ftp.connect(config.ftp_ip, int(config.ftp_port))
    ftp.login(config.ftp_user, config.ftp_passwd)
    ftp.encoding = 'gb2312'
    ftp_file_path=config.ftp_file_url
    ftp.cwd(ftp_file_path)
    for file in files:
        try:
            ftp.delete(file)
            logger.debug('%s deleted successfully' % file)
        except ftplib.error_perm as e:
            if '550' in str(e):
                logger.debug('%s does not exist' % file)
            else:
                logger.debug(e)
    ftp.quit()

def delhttpfile(frontpath,file_url):
    # 删除http服务器上的上传文件
    os.chdir(frontpath)
    files = os.listdir("data/file/")
    # logger.debug(files)
    for file in files:
        if os.path.exists(frontpath+"/data/file/"+file):
            logger.debug("删除http服务器上的上传文件： "+file_url+file)
            requests.post(file_url,
            auth=("linhuilong", "linhuilong"),
                  data={"action": "delete", "selection": file})

def updateappid_before(config,appzip):
    log_file = config.log_command_path
    filename=config.firewalld_root_path+"/"+appzip.split("/")[-1]
    logger.info("开始更新应用识别")
    command=f'ssh-keygen -R {config.firewalld_ip}'
    logger.debug("执行命令为： "+command)
    if "DEBUG" in config.Level:
        logger.debug("debug模式")
        child = pexpect.spawn(command, encoding='utf-8', logfile=open(log_file, 'w'),timeout=10)
    else:
        logger.info("info模式")
        child = pexpect.spawn(command,encoding='utf-8',timeout=10)
    while True:
        index = child.expect([pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
        if index == 0:  # 子进程输出结束符
            logger.debug("命令执行结束"+command)
            break
        elif index == 1:  # 子进程输出超时
            logger.debug("命令执行超时"+command)
            continue
        else:  # 正常输出
            output_line = child.before.strip()
            logger.debug(output_line)
    
    child.close()
    command=f"ssh {config.firewalld_shell_user}@{config.firewalld_ip}"
    if "DEBUG" in config.Level:
        child = pexpect.spawn(command, encoding='utf-8', logfile=open(log_file, 'a'),timeout=10)
    else:
        child = pexpect.spawn(command,encoding='utf-8',timeout=10)
    logger.debug("执行命令为： "+command)
    output_index = child.expect([".*yes/no.* ", "password:", pexpect.EOF, pexpect.TIMEOUT])
    # Check which output was matched and execute the next command accordingly
    if output_index == 0:
        logger.debug("Received 1, executing next yes")
        child.sendline("yes")
        output_index = child.expect(["password:", pexpect.EOF, pexpect.TIMEOUT])
        if output_index == 0:
            logger.debug("输入防火墙密码： "+config.firewalld_shell_passwd)
            child.sendline(config.firewalld_shell_passwd)         
            while True:
                index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                if index == 0:  # 子进程输出结束符
                    logger.debug("命令执行结束"+command)
                    break
                elif index == 1:  # 子进程输出超时
                    logger.debug("命令执行超时"+command)
                    break
                else:  # 正常输出
                    output_line = child.before.strip()
                    logger.debug(output_line)
    elif output_index == 1:
        logger.debug("输入防火墙密码： "+config.firewalld_shell_passwd)
        child.sendline(config.firewalld_shell_passwd)
        while True:
            index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
            if index == 0:  # 子进程输出结束符
                logger.debug("命令执行结束"+command)
                break
            elif index == 1:  # 子进程输出超时
                logger.debug("命令执行超时"+command)
                break
            else:  # 正常输出
                output_line = child.before.strip()
                logger.debug(output_line)
    logger.debug("防火墙上的文件为： "+filename)
    command2=f"sudo rm -rf {config.firewalld_root_path}/app*.zip"
    command3=f'scp -r  {config.linux_user}@{config.linux_ip}:{appzip} {config.firewalld_root_path}'
    command4="sudo cat /etc/os-release|head -n 1 > /mnt/flash/app-rules.log"
    command5="sudo cat /etc/.release >> /mnt/flash/app-rules.log"
    command6="sudo cat /etc/.releaseID >> /mnt/flash/app-rules.log"
    command7="sudo fpcmd fp app-id show version >> /mnt/flash/app-rules.log"
    command8="sudo echo >> /mnt/flash/app-rules.log"
    command9="sudo free >> /mnt/flash/app-rules.log"
    command10="sudo journalctl -f |grep fp-rte|grep APP_IDY|grep -A 10000 \"Local signature database upgrading.\" >> /mnt/flash/app-rules.log &"
    command11="sudo fpcmd fp app-id debug file on"
    command12=f"sudo md5sum {filename} >> /mnt/flash/app-rules.log"
    command13="exit"
    commands = [command2, command3, command4, command5, 
                command6, command7, command8, command9, command10,
                command11,command12,command13,command13]

    command999 = "kill -9 $(ps -ef | grep root | grep pts |grep -v `echo ${SSH_TTY:5}` |grep -v bash | awk '{print $2}')"
    commands.insert(0,command999)
    for cmd in commands:
        child.sendline(cmd)
        output_index = child.expect([".*yes/no.*", ".*password:",'.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT])
        if ("scp" in cmd) or ("ssh" in cmd):
            if output_index == 0:
                logger.debug(f"Received 1, executing next {cmd}")
                child.sendline("yes")
                output_index = child.expect([".*word:", pexpect.EOF, pexpect.TIMEOUT])
                if output_index == 0:
                    logger.debug("输入Linux密码： "+config.linux_passwd)
                    child.sendline(config.linux_passwd)
                    while True:
                        index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                        if index == 0:  # 子进程输出结束符
                            logger.debug("命令执行结束"+cmd)
                            break
                        elif index == 1:  # 子进程输出超时
                            logger.debug("命令执行超时"+cmd)
                            break
                        else:  # 正常输出
                            output_line = child.before.strip()
                            logger.debug(output_line)
            elif output_index == 1:
                logger.debug("输入linux密码： "+config.linux_passwd)
                child.sendline(config.linux_passwd)
                while True:
                    index = child.expect([".*firewall.*",pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                    if index == 0:  # 子进程输出结束符
                        logger.debug("命令执行结束"+cmd)
                        break
                    elif index == 1:  # 子进程输出超时
                        logger.debug("命令执行超时"+cmd)
                        continue
                    else:  # 正常输出
                        output_line = child.before.strip()
                        logger.debug(output_line)
            elif output_index == 2:
                logger.debug(f"666666： str(child.before.strip())")
            else:
                logger.debug("Command failed or terminated before expected output was received")
        logger.debug(f'{output_index}  {cmd}') 
    child.close()
def updateappid_end(config,update_dir):
    appid_log = "app-rules.log"
    appid_log_apth=update_dir+"appid/"
    appid_log = appid_log_apth+appid_log
    log_file = config.log_command_path
    logger.info("开始判断应用识别更新结果")
    command=f'rm -rf {update_dir}appid/*.log'
    logger.debug("执行命令为： "+command)
    if "DEBUG" in config.Level:
        logger.debug("debug模式")
        child = pexpect.spawn(command, encoding='utf-8', logfile=open(log_file, 'a'),timeout=10)
    else:
        logger.info("info模式")
        child = pexpect.spawn(command,encoding='utf-8',timeout=10)
    while True:
        index = child.expect([pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
        if index == 0:  # 子进程输出结束符
            logger.debug("命令执行结束"+command)
            break
        elif index == 1:  # 子进程输出超时
            logger.debug("命令执行超时"+command)
            continue
        else:  # 正常输出
            output_line = child.before.strip()
            logger.debug(output_line)
    
    child.close()
    command=f"ssh {config.firewalld_shell_user}@{config.firewalld_ip}"
    if "DEBUG" in config.Level:
        child = pexpect.spawn(command, encoding='utf-8', logfile=open(log_file, 'a'),timeout=10)
    else:
        child = pexpect.spawn(command,encoding='utf-8',timeout=10)
    logger.debug("执行命令为： "+command)
    output_index = child.expect([".*yes/no.* ", "password:", pexpect.EOF, pexpect.TIMEOUT])
    # Check which output was matched and execute the next command accordingly
    if output_index == 0:
        logger.debug("Received 1, executing next yes")
        child.sendline("yes")
        output_index = child.expect(["password:", pexpect.EOF, pexpect.TIMEOUT])
        if output_index == 0:
            logger.debug("输入防火墙密码： "+config.firewalld_shell_passwd)
            child.sendline(config.firewalld_shell_passwd)         
            while True:
                index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                if index == 0:  # 子进程输出结束符
                    logger.debug("命令执行结束"+command)
                    break
                elif index == 1:  # 子进程输出超时
                    logger.debug("命令执行超时"+command)
                    break
                else:  # 正常输出
                    output_line = child.before.strip()
                    logger.debug(output_line)
    elif output_index == 1:
        logger.debug("输入防火墙密码： "+config.firewalld_shell_passwd)
        child.sendline(config.firewalld_shell_passwd)
        while True:
            index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
            if index == 0:  # 子进程输出结束符
                logger.debug("命令执行结束"+command)
                break
            elif index == 1:  # 子进程输出超时
                logger.debug("命令执行超时"+command)
                break
            else:  # 正常输出
                output_line = child.before.strip()
                logger.debug(output_line)
    logger.debug("日志存放目录： "+appid_log_apth)
    command2=f"killall journalctl"
    child.sendline(command2)
    output_index = child.expect([".*yes/no.*", ".*password:",'.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT])
    logger.debug(f'{output_index}  {command2}') 
    time.sleep(5)
    command3=f'sudo free >> /mnt/flash/app-rules.log'
    # command4="sudo fpcmd fp app-id sig-version >> /mnt/flash/app-rules.log"
    command4="sudo fpcmd fp app-id show version >> /mnt/flash/app-rules.log"
    command5="sudo echo >> /mnt/flash/app-rules.log"
    command6=f"sudo scp -r /mnt/flash/app-rules.log {config.linux_user}@{config.linux_ip}:{appid_log_apth}"
    command7="exit"
    commands = [command3, command4, command5, 
                command6, command7,command7]
    command999 = "kill -9 $(ps -ef | grep root | grep pts |grep -v `echo ${SSH_TTY:5}` |grep -v bash | awk '{print $2}')"
    commands.insert(0,command999)
    for cmd in commands:
        child.sendline(cmd)
        output_index = child.expect([".*yes/no.*", ".*password:",'.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT])
        if ("scp" in cmd) or ("ssh" in cmd):
            if output_index == 0:
                logger.debug(f"Received 1, executing next {cmd}")
                child.sendline("yes")
                output_index = child.expect([".*word:", pexpect.EOF, pexpect.TIMEOUT])
                if output_index == 0:
                    logger.debug("输入Linux密码： "+config.linux_passwd)
                    child.sendline(config.linux_passwd)
                    while True:
                        index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                        if index == 0:  # 子进程输出结束符
                            logger.debug("命令执行结束"+cmd)
                            break
                        elif index == 1:  # 子进程输出超时
                            logger.debug("命令执行超时"+cmd)
                            break
                        else:  # 正常输出
                            output_line = child.before.strip()
                            logger.debug(output_line)
            elif output_index == 1:
                logger.debug("输入linux密码： "+config.linux_passwd)
                child.sendline(config.linux_passwd)
                while True:
                    index = child.expect([".*firewall.*",pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                    if index == 0:  # 子进程输出结束符
                        logger.debug("命令执行结束"+cmd)
                        break
                    elif index == 1:  # 子进程输出超时
                        logger.debug("命令执行超时"+cmd)
                        continue
                    else:  # 正常输出
                        output_line = child.before.strip()
                        logger.debug(output_line)
            elif output_index == 2:
                logger.debug(f"666666： str(child.before.strip())")
            else:
                logger.debug("Command failed or terminated before expected output was received")
        logger.debug(f'{output_index}  {cmd}') 
    child.close()
def updateapp_judge(flag,frontpath,file_name,config):
    logger.debug("判断更新结果")
    report_temp_path = frontpath+"/report/history/report_temp/"
    update_log = frontpath+"/update/appid/app-rules.log"
    with open(update_log, 'r') as f:
        lines = f.readlines()
        softwarever =lines[0].strip()+" "+lines[1].strip()+" "+lines[2].strip()
        softwarever=softwarever.replace('NAME=','')
        line4 = lines[3].strip()  # 第4行，注意Python下标从0开始
        md5 = lines[8].strip().split(" ")[0]  # 第9行，注意Python下标从0开始
        last_line = lines[-1].strip()  # 最后一行非空内容
        while not last_line:  # 如果最后一行为空，则继续往前找到非空行
            last_line = lines.pop().strip()
        logger.debug(f"更新前版本： {line4}")
        logger.debug(f"更新后版本： {last_line}")


    if line4 != last_line and last_line != "00000000.0000":
        content = f"{softwarever}\nThe name of the library to upgrade is {file_name}\nmd5 is {md5}\n一、appid signature update success ! \nnow version is {last_line}\n"
        send_message(content,config)
        with open(f"{report_temp_path}/result.txt", "w") as f:
            f.write(content)
        os.system(f"cp {update_log} {report_temp_path}")

    elif line4 == last_line :
        logger.debug("版本一致，回退备份版本ing")
        flag= True
        return flag
    else:
        content = f"{softwarever}\nThe name of the library to upgrade is {file_name}\nmd5 is {md5}\n一、appid signature update fail ! \nnow version is {last_line}\n"
        send_message(content,config)
        with open(f"{report_temp_path}/result.txt", "w") as f:
            f.write(content)
        os.system(f"cp {update_log} {report_temp_path}")

def updateips_before(config,ipszip):
    log_file = config.log_command_path
    filename=config.firewalld_root_path+"/"+ipszip.split("/")[-1]
    logger.info("开始更新ips")
    command=f'ssh-keygen -R {config.firewalld_ip}'
    logger.debug("执行命令为： "+command)
    if "DEBUG" in config.Level:
        logger.debug("debug模式")
        child = pexpect.spawn(command, encoding='utf-8', logfile=open(log_file, 'w'),timeout=10)
    else:
        logger.info("info模式")
        child = pexpect.spawn(command,encoding='utf-8',timeout=10)
    while True:
        index = child.expect([pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
        if index == 0:  # 子进程输出结束符
            logger.debug("命令执行结束"+command)
            break
        elif index == 1:  # 子进程输出超时
            logger.debug("命令执行超时"+command)
            continue
        else:  # 正常输出
            output_line = child.before.strip()
            logger.debug(output_line)
    
    child.close()
    command=f"ssh {config.firewalld_shell_user}@{config.firewalld_ip}"
    if "DEBUG" in config.Level:
        child = pexpect.spawn(command, encoding='utf-8', logfile=open(log_file, 'a'),timeout=10)
    else:
        child = pexpect.spawn(command,encoding='utf-8',timeout=10)
    logger.debug("执行命令为： "+command)
    output_index = child.expect([".*yes/no.* ", "password:", pexpect.EOF, pexpect.TIMEOUT])
    # Check which output was matched and execute the next command accordingly
    if output_index == 0:
        logger.debug("Received 1, executing next yes")
        child.sendline("yes")
        output_index = child.expect(["password:", pexpect.EOF, pexpect.TIMEOUT])
        if output_index == 0:
            logger.debug("输入防火墙密码： "+config.firewalld_shell_passwd)
            child.sendline(config.firewalld_shell_passwd)         
            while True:
                index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                if index == 0:  # 子进程输出结束符
                    logger.debug("命令执行结束"+command)
                    break
                elif index == 1:  # 子进程输出超时
                    logger.debug("命令执行超时"+command)
                    break
                else:  # 正常输出
                    output_line = child.before.strip()
                    logger.debug(output_line)
    elif output_index == 1:
        logger.debug("输入防火墙密码： "+config.firewalld_shell_passwd)
        child.sendline(config.firewalld_shell_passwd)
        while True:
            index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
            if index == 0:  # 子进程输出结束符
                logger.debug("命令执行结束"+command)
                break
            elif index == 1:  # 子进程输出超时
                logger.debug("命令执行超时"+command)
                break
            else:  # 正常输出
                output_line = child.before.strip()
                logger.debug(output_line)
    logger.debug("防火墙上的文件为： "+filename)
    command2=f"sudo rm -rf {config.firewalld_root_path}/ips*.zip"
    command3=f'scp -r  {config.linux_user}@{config.linux_ip}:{ipszip} {config.firewalld_root_path}'
    command4="sudo cat /etc/os-release|head -n 1 > /mnt/flash/ips-rules.log"
    command5="sudo cat /etc/.release >> /mnt/flash/ips-rules.log"
    command6="sudo cat /etc/.releaseID >> /mnt/flash/ips-rules.log"
    command7="sudo fpcmd fp ips show sig-info|grep \"sig version\" >> /mnt/flash/ips-rules.log"
    command8="sudo echo >> /mnt/flash/ips-rules.log"
    command9="sudo free >> /mnt/flash/ips-rules.log"
    command10=f"sudo md5sum {filename} >> /mnt/flash/ips-rules.log"
    command11="exit"
    commands = [command2, command3, command4, command5, 
                command6, command7, command8, command9, command10,command11,command11]

    command999 = "kill -9 $(ps -ef | grep root | grep pts |grep -v `echo ${SSH_TTY:5}` |grep -v bash | awk '{print $2}')"
    commands.insert(0,command999)
    for cmd in commands:
        child.sendline(cmd)
        output_index = child.expect([".*yes/no.*", ".*password:",'.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT])
        if ("scp" in cmd) or ("ssh" in cmd):
            if output_index == 0:
                logger.debug(f"Received 1, executing next {cmd}")
                child.sendline("yes")
                output_index = child.expect([".*word:", pexpect.EOF, pexpect.TIMEOUT])
                if output_index == 0:
                    logger.debug("输入Linux密码： "+config.linux_passwd)
                    child.sendline(config.linux_passwd)
                    while True:
                        index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                        if index == 0:  # 子进程输出结束符
                            logger.debug("命令执行结束"+cmd)
                            break
                        elif index == 1:  # 子进程输出超时
                            logger.debug("命令执行超时"+cmd)
                            break
                        else:  # 正常输出
                            output_line = child.before.strip()
                            logger.debug(output_line)
            elif output_index == 1:
                logger.debug("输入linux密码： "+config.linux_passwd)
                child.sendline(config.linux_passwd)
                while True:
                    index = child.expect([".*firewall.*",pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                    if index == 0:  # 子进程输出结束符
                        logger.debug("命令执行结束"+cmd)
                        break
                    elif index == 1:  # 子进程输出超时
                        logger.debug("命令执行超时"+cmd)
                        continue
                    else:  # 正常输出
                        output_line = child.before.strip()
                        logger.debug(output_line)
            elif output_index == 2:
                logger.debug(f"666666： str(child.before.strip())")
            else:
                logger.debug("Command failed or terminated before expected output was received")
        logger.debug(f'{output_index}  {cmd}') 
    child.close()
def updateips_end(config,update_dir):
    log_file = config.log_command_path
    filename=update_dir+"ips/"
    logger.info("获取ips更新结果")
    command=f'rm -rf {update_dir}ips/*.log'
    logger.debug("执行命令为： "+command)
    if "DEBUG" in config.Level:
        logger.debug("debug模式")
        child = pexpect.spawn(command, encoding='utf-8', logfile=open(log_file, 'a'),timeout=10)
    else:
        logger.info("info模式")
        child = pexpect.spawn(command,encoding='utf-8',timeout=10)
    while True:
        index = child.expect([pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
        if index == 0:  # 子进程输出结束符
            logger.debug("命令执行结束"+command)
            break
        elif index == 1:  # 子进程输出超时
            logger.debug("命令执行超时"+command)
            continue
        else:  # 正常输出
            output_line = child.before.strip()
            logger.debug(output_line)
    
    child.close()
    command=f"ssh {config.firewalld_shell_user}@{config.firewalld_ip}"
    if "DEBUG" in config.Level:
        child = pexpect.spawn(command, encoding='utf-8', logfile=open(log_file, 'a'),timeout=10)
    else:
        child = pexpect.spawn(command,encoding='utf-8',timeout=10)
    logger.debug("执行命令为： "+command)
    output_index = child.expect([".*yes/no.* ", "password:", pexpect.EOF, pexpect.TIMEOUT])
    # Check which output was matched and execute the next command accordingly
    if output_index == 0:
        logger.debug("Received 1, executing next yes")
        child.sendline("yes")
        output_index = child.expect(["password:", pexpect.EOF, pexpect.TIMEOUT])
        if output_index == 0:
            logger.debug("输入防火墙密码： "+config.firewalld_shell_passwd)
            child.sendline(config.firewalld_shell_passwd)         
            while True:
                index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                if index == 0:  # 子进程输出结束符
                    logger.debug("命令执行结束"+command)
                    break
                elif index == 1:  # 子进程输出超时
                    logger.debug("命令执行超时"+command)
                    break
                else:  # 正常输出
                    output_line = child.before.strip()
                    logger.debug(output_line)
    elif output_index == 1:
        logger.debug("输入防火墙密码： "+config.firewalld_shell_passwd)
        child.sendline(config.firewalld_shell_passwd)
        while True:
            index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
            if index == 0:  # 子进程输出结束符
                logger.debug("命令执行结束"+command)
                break
            elif index == 1:  # 子进程输出超时
                logger.debug("命令执行超时"+command)
                break
            else:  # 正常输出
                output_line = child.before.strip()
                logger.debug(output_line)
    logger.debug("日志存放目录： "+filename)
    command2=f"sudo cat /mnt/flash/ips/log/ips-rules.log >>/mnt/flash/ips-rules.log"
    # child.sendline(command2)
    # output_index = child.expect([".*yes/no.*", ".*password:",'.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT])
    # logger.debug(f'{output_index}  {command2}') 
    # time.sleep(5)
    command3=f'sudo free >> /mnt/flash/ips-rules.log'
    # command4="sudo fpcmd fp ips-id sig-version >> /mnt/flash/ips-rules.log"
    command4="sudo fpcmd fp ips show sig-info|grep \"sig version\" >> /mnt/flash/ips-rules.log"
    command5="sudo echo >> /mnt/flash/ips-rules.log"
    command6=f"sudo scp -r /mnt/flash/ips-rules.log {config.linux_user}@{config.linux_ip}:{filename}"
    command7="exit"
    commands = [command2,command3, command4, command5, 
                command6, command7,command7]

    command999 = "kill -9 $(ps -ef | grep root | grep pts |grep -v `echo ${SSH_TTY:5}` |grep -v bash | awk '{print $2}')"
    commands.insert(0,command999)
    for cmd in commands:
        child.sendline(cmd)
        output_index = child.expect([".*yes/no.*", ".*password:",'.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT])
        if ("scp" in cmd) or ("ssh" in cmd):
            if output_index == 0:
                logger.debug(f"Received 1, executing next {cmd}")
                child.sendline("yes")
                output_index = child.expect([".*word:", pexpect.EOF, pexpect.TIMEOUT])
                if output_index == 0:
                    logger.debug("输入Linux密码： "+config.linux_passwd)
                    child.sendline(config.linux_passwd)
                    while True:
                        index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                        if index == 0:  # 子进程输出结束符
                            logger.debug("命令执行结束"+cmd)
                            break
                        elif index == 1:  # 子进程输出超时
                            logger.debug("命令执行超时"+cmd)
                            break
                        else:  # 正常输出
                            output_line = child.before.strip()
                            logger.debug(output_line)
            elif output_index == 1:
                logger.debug("输入linux密码： "+config.linux_passwd)
                child.sendline(config.linux_passwd)
                while True:
                    index = child.expect([".*firewall.*",pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                    if index == 0:  # 子进程输出结束符
                        logger.debug("命令执行结束"+cmd)
                        break
                    elif index == 1:  # 子进程输出超时
                        logger.debug("命令执行超时"+cmd)
                        continue
                    else:  # 正常输出
                        output_line = child.before.strip()
                        logger.debug(output_line)
            elif output_index == 2:
                logger.debug(f"666666： str(child.before.strip())")
            else:
                logger.debug("Command failed or terminated before expected output was received")
        logger.debug(f'{output_index}  {cmd}') 
    child.close()
def updateips_judge(flag,frontpath,file_name,config):
    report_temp_path = frontpath+"/report/history/report_temp/"
    update_log = frontpath+"/update/ips/ips-rules.log"
    update_err=""
    rule=""
    update_arr_wro=""
    # free = os.popen(f"cat {update_log} | grep 'Mem:'").read()
    with open(update_log, 'r') as f:
        lines = f.readlines()
        softwarever =lines[0].strip()+" "+lines[1].strip()+" "+lines[2].strip()
        softwarever=softwarever.replace('NAME=','')
        line4 = lines[3].strip().split(':')[-1]  # 第4行，注意Python下标从0开始
        md5 = lines[8].strip().split(" ")[0]  # 第9行，注意Python下标从0开始
        for line in lines:
            # 判断当前行是否包含关键字
            if ('err' in line and "same sig version" not in line) \
            or 'wrong' in line  \
            or ('ips' in line and 'fail' in line and "success" not in line and "Same Version" not in line) \
            or (flag and 'err' in line):
                # 如果包含，则打印该行
                update_arr_wro=update_arr_wro+line
            if 'rules successfully' in line:
                # 如果包含，则打印该行
                rule=line.split('.')[-1]
        last_line = lines[-1].strip()  # 最后一行非空内容
        while not last_line:  # 如果最后一行为空，则继续往前找到非空行
            last_line = lines.pop().strip()
        version=last_line.split(':')[-1]           
        logger.debug(f"更新前版本： {line4}")
        logger.debug(f"更新后版本： {version}")

    if  not update_arr_wro:
        exception= f"no problem \n {update_arr_wro}"
    else:
        exception= f"there is something wrong: \n {update_arr_wro}"
    if line4 != version and version != "00000000.0000":
        content=f"{softwarever}\nThe name of the library to upgrade is \
        {file_name}\nmd5 is {md5}\n一、ips signature update success ! \
        \nnow version is {version}\n{rule}{exception}\n"
        send_message(content,config)
        with open(f"{report_temp_path}/result.txt", "w") as f:
            f.write(content)
        # subprocess.run(["scp", "-r", f"{pc_path}/update/ipsid/ips-rules*.log", f"{pc_path}/report/history/report_temp/"])
    elif (line4 == version) and (not update_arr_wro):
        logger.debug(f"版本一致，回退备份版本ing {line4}=={version}")
        flag= True
        return flag
    else:
        content=f"{softwarever}\nThe name of the library to upgrade is \
        {file_name}\nmd5 is {md5}\n一、ips signature update fail !  \
        \nnow version is {version}\n{rule}{exception}\n"
        send_message(content,config)
        with open(f"{report_temp_path}/result.txt", "w") as f:
            f.write(content)
        os.system(f"cp {update_log} {report_temp_path}")

def init_firewall(type,config,frontpath):
    update_type_path=f"{frontpath}/update/{type}/"
    if type == "appid" :
        if config.firewalld_shell_user == "root":
            logger.debug("应用识别执行root账号命令")
            command1="sudo fpcmd fp app-id cfg enable cache false"
            command2='sudo fpcmd fp app-id cfg enable expect false'
            command3="sudo fpcmd fp app-id show application > /mnt/flash/app-rules.txt"
            command4=f"sudo scp -r /mnt/flash/app-rules.txt root@{config.linux_ip}:{update_type_path}"
            command5="sudo fp-npfctl flows-flush"
            command6="exit"
            commands = [command1,command2, command3, command4, command5,command6]
        elif config.firewalld_shell_user == "admin":
            command1="cmd appid run \'app-id cache-enable false\'"
            command2='cmd appid run \'app-id expect-enable false\''
            command3="flush nfp flows"
            command4="exit"
            commands = [command1,command2, command3, command4]
        else:
            command1="sudo ls"
            command2='sudo fpcmd fp app-id cache-enable false'
            command3="sudo fpcmd fp app-id expect-enable false"
            command4="sudo fp-npfctl flows-flush"
            command5="exit"
            commands = [command1,command2, command3, command4, command5,command5]
    elif type == "ips" :
        if config.firewalld_shell_user == "root":
            logger.debug("ips执行root账号命令")
            command1="sudo fpcmd fp app-id cache-enable false"
            command2='sudo fpcmd fp app-id expect-enable false'
            command3="sudo sqlite3 /tmp/ips/ips_sig.db .dump > /mnt/flash/ips-rules.txt"
            command4=f"sudo scp -r /mnt/flash/ips-rules.txt root@{config.linux_ip}:{update_type_path}"
            command5="sudo fpcmd fp ips debug pkt-debug off"
            command6="sudo fpcmd fp ips debug post-match off"
            command7="sudo fpcmd fp ips debug log on"
            command8="sudo fpcmd log-level-set 7"
            command9="sudo fpcmd log-type-set all off"
            command10="sudo fpcmd log-type-set APP_PARSER on"
            command11="sudo fpcmd log-type-set IPS on"
            command12="sudo fp-npfctl flows-flush"
            command13="exit"
            commands = [command1,command2, command3, command4, command5,command6,
                        command7,command8, command9, command10, command11,command12,
                        command13]
        elif config.firewalld_shell_user == "admin":
            command1="cmd appid run \'app-id cache-enable false\'"
            command2="cmd appid run \'app-id expect-enable false\'"
            command3="cmd ips run \"debug pkt-debug off\""
            command4="cmd ips run \"debug post-match off\""
            command5="cmd ips run \"debug log on\""
            command6="cmd debug-support fp exec \"log-level-set 7\""
            command7="cmd debug-support fp exec \"log-type-set all off\""
            command8="cmd debug-support fp exec \"log-type-set APP_PARSER on\""
            command9="cmd debug-support fp exec \"log-type-set IPS on\""
            command10="flush nfp flows"
            command11="exit"
            commands = [command1,command2, command3, command4, command5,command6,
                        command7,command8, command9, command10, command11,command11]       
        else:
            command1="sudo ls"
            command2="sudo fpcmd fp app-id cache-enable false"
            command3="sudo fpcmd fp app-id expect-enable false"
            command4="sudo fpcmd fp ips debug pkt-debug off"
            command5="sudo fpcmd fp ips debug post-match off"
            command6="sudo fpcmd fp ips debug log on"
            command7="sudo fpcmd log-level-set 7"
            command8="sudo fpcmd log-type-set all off"
            command9="sudo fpcmd log-type-set APP_PARSER on"
            command10="sudo fpcmd log-type-set IPS on"
            command11="sudo fp-npfctl flows-flush"
            command12="exit"
            commands = [command1,command2, command3, command4, command5,command6,
                        command7,command8, command9, command10, command11,command11,
                        command12,command12] 

    log_file = config.log_command_path
    logger.debug("开始初始化防火墙")
    command=f'ssh-keygen -R {config.firewalld_ip}'
    logger.debug("执行命令为： "+command)
    if "DEBUG" in config.Level:
        logger.debug("debug模式")
        child = pexpect.spawn(command, encoding='utf-8', logfile=open(log_file, 'w'),timeout=10)
    else:
        logger.info("info模式")
        child = pexpect.spawn(command,encoding='utf-8',timeout=10)
    while True:
        index = child.expect([pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
        if index == 0:  # 子进程输出结束符
            logger.debug("命令执行结束"+command)
            break
        elif index == 1:  # 子进程输出超时
            logger.debug("命令执行超时"+command)
            continue
        else:  # 正常输出
            output_line = child.before.strip()
            logger.debug(output_line)
    
    child.close()
    command=f"ssh {config.firewalld_shell_user}@{config.firewalld_ip}"
    if "DEBUG" in config.Level:
        child = pexpect.spawn(command, encoding='utf-8', logfile=open(log_file, 'a'),timeout=10)
    else:
        child = pexpect.spawn(command,encoding='utf-8',timeout=10)
    logger.debug("执行命令为： "+command)
    output_index = child.expect([".*yes/no.* ", "password:", pexpect.EOF, pexpect.TIMEOUT])
    # Check which output was matched and execute the next command accordingly
    if output_index == 0:
        logger.debug("Received 1, executing next yes")
        child.sendline("yes")
        output_index = child.expect(["password:", pexpect.EOF, pexpect.TIMEOUT])
        if output_index == 0:
            logger.debug("输入防火墙密码： "+config.firewalld_shell_passwd)
            child.sendline(config.firewalld_shell_passwd)         
            while True:
                index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                if index == 0:  # 子进程输出结束符
                    logger.debug("命令执行结束"+command)
                    break
                elif index == 1:  # 子进程输出超时
                    logger.debug("命令执行超时"+command)
                    break
                else:  # 正常输出
                    output_line = child.before.strip()
                    logger.debug(output_line)
    elif output_index == 1:
        logger.debug("输入防火墙密码： "+config.firewalld_shell_passwd)
        child.sendline(config.firewalld_shell_passwd)
        while True:
            index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
            if index == 0:  # 子进程输出结束符
                logger.debug("命令执行结束"+command)
                break
            elif index == 1:  # 子进程输出超时
                logger.debug("命令执行超时"+command)
                break
            else:  # 正常输出
                output_line = child.before.strip()
                logger.debug(output_line)
    

    command999 = "kill -9 $(ps -ef | grep root | grep pts |grep -v `echo ${SSH_TTY:5}` |grep -v bash | awk '{print $2}')"
    commands.insert(0,command999)
    for cmd in commands:
        child.sendline(cmd)
        output_index = child.expect([".*yes/no.*", ".*password:",'.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT])
        if ("scp" in cmd) or ("ssh" in cmd):
            if output_index == 0:
                logger.debug(f"Received 1, executing next {cmd}")
                child.sendline("yes")
                output_index = child.expect([".*word:", pexpect.EOF, pexpect.TIMEOUT])
                if output_index == 0:
                    logger.debug("输入Linux密码： "+config.linux_passwd)
                    child.sendline(config.linux_passwd)
                    while True:
                        index = child.expect(['.*'+config.firewalld_hostname+'.*',pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                        if index == 0:  # 子进程输出结束符
                            logger.debug("命令执行结束"+cmd)
                            break
                        elif index == 1:  # 子进程输出超时
                            logger.debug("命令执行超时"+cmd)
                            break
                        else:  # 正常输出
                            output_line = child.before.strip()
                            logger.debug(output_line)
            elif output_index == 1:
                logger.debug("输入linux密码： "+config.linux_passwd)
                child.sendline(config.linux_passwd)
                while True:
                    index = child.expect([".*firewall.*",pexpect.EOF, pexpect.TIMEOUT, '\n', '\r'])
                    if index == 0:  # 子进程输出结束符
                        logger.debug("命令执行结束"+cmd)
                        break
                    elif index == 1:  # 子进程输出超时
                        logger.debug("命令执行超时"+cmd)
                        continue
                    else:  # 正常输出
                        output_line = child.before.strip()
                        logger.debug(output_line)
            elif output_index == 2:
                logger.debug(f"666666： str(child.before.strip())")
            else:
                logger.debug("Command failed or terminated before expected output was received")
        logger.debug(f"{output_index}  {cmd}") 
    child.close()

def updatefeature (config,frontpath):
    logger.debug("判断是否升级特征库")
    os.chdir(frontpath+"/data/file/")
    update_dir=frontpath+"/update/"

    # Create target directories if they don't exist
    os.makedirs(os.path.join(update_dir, "ips"), exist_ok=True)
    os.makedirs(os.path.join(update_dir, "ips_back"), exist_ok=True)
    os.makedirs(os.path.join(update_dir, "appid"), exist_ok=True)
    os.makedirs(os.path.join(update_dir, "appid_back"), exist_ok=True)

    # Check for app.zip files and perform some operations and log results
    for file_name in os.listdir("."):
        logger.debug("当前目录下文件为："+file_name)
        if "test" in file_name or "ok" in file_name:
            continue
        elif  file_name.startswith("app") and file_name.endswith(".zip"):
            type ="appid"
            key = "$appid_key"
            key_fs = "$appid_key_fs"
            appzip=os.path.join(frontpath+"/data/file/"+file_name)
            updateappid_before(config,appzip)
            run_update_test(type,appzip,config)
            updateappid_end(config,update_dir)
            flag=False
            flag=updateapp_judge(flag,frontpath,file_name,config)
            if flag :
                appzip_b=config.appid_library_back
                if not os.path.exists(appzip_b):
                    logger.error(f"降级需要的特征库不存在，请上传到 {appzip_b}")
                    message=f"降级需要的特征库不存在，请上传到 {appzip_b}"
                    send_message(message,config)
                    break
                run_update_test(type,appzip_b,config)
                updateappid_before(config,appzip)
                run_update_test(type,appzip,config)
                updateappid_end(config,update_dir)
                updateapp_judge(flag,frontpath,file_name,config)
        elif  file_name.startswith("ips") and file_name.endswith(".zip"):
            type ="ips"
            key = "$appid_key"
            key_fs = "$appid_key_fs"
            ipszip=os.path.join(frontpath+"/data/file/"+file_name)
            updateips_before(config,ipszip)
            run_update_test(type,ipszip,config)
            updateips_end(config,update_dir)
            flag=False
            flag=updateips_judge(flag,frontpath,file_name,config)
            if flag :
                ipszip_b=config.ips_library_back
                if not os.path.exists(ipszip_b):
                    logger.error(f"降级需要的特征库不存在，请上传到 {ipszip_b}")
                    message=f"降级需要的特征库不存在，请上传到 {ipszip_b}"
                    send_message(message,config)
                    break   
                run_update_test(type,ipszip_b,config)
                updateips_before(config,ipszip)
                run_update_test(type,ipszip,config)
                updateips_end(config,update_dir)
                updateips_judge(flag,frontpath,file_name,config)

def pcap_check(type,config,frontpath):
    network_init(config)
    content="Packet playback verification"
    logger.debug(f"{type},开始回放包")
    pcap_path=os.path.join(frontpath, "data", f"pcap_{type}/")
    pcap_b_path=os.path.join(frontpath, "data", f"pcap_{type}_b/")
    pcap_temp_path=os.path.join(frontpath, "data", f"pcap_{type}_temp/")
    if len(os.listdir(pcap_temp_path)) > 0:
        del_space(pcap_temp_path)
    else:
        ftp_get_file(type,config,frontpath)
    if len(os.listdir(pcap_temp_path)) > 0:
        os.system(f"cp {pcap_temp_path}/* {pcap_path}")
    elif len(os.listdir(pcap_b_path)) > 0:
        logger.debug(f"回放备份包 {pcap_b_path}")
        os.system(f"cp {pcap_b_path}/* {pcap_path}")
    else:
        logger.debug("不存在回放包")
        return
    count=len(os.listdir(pcap_path))
    logger.debug(f"待回放包数量： {count}")
    init_firewall(type,config,frontpath)
    replay_count=count
    yes_count=0
    for bigpcap in os.listdir(pcap_path):
        if "@yes." in bigpcap:
            yes_count += 1
    if type == "appid":
        content=f"Now all pcap count {replay_count},yes pcap count {yes_count}"
        send_message(content,config)
    elif type == "ips":
        content=f"Now replay pcap count {replay_count}"
        send_message(content,config)
    no=0
    temp = os.path.join(frontpath, "temp/")
    temp_path=create_dir_bytime(temp)
    logger.debug(f"创建目录： {temp_path}")

    for bigpcap in os.listdir(pcap_path):
        start_time = time.time()
        file_path=os.path.join(pcap_path, bigpcap)
        report_all_path = os.path.join(frontpath, "report",type,"all/")
        file_len=os.stat(file_path).st_size
        no += 1
        command=f"rm -rf  {report_all_path}/*"
        shell_command(command)
        cyclenum=0
        if "@yes." in bigpcap:
            command=f"pkt2flow  -uo {report_all_path} {file_path}"
            shell_command(command)
            replay_pcap(type,report_all_path,bigpcap,temp_path,no,config,frontpath)
        elif "@na.pcap" in bigpcap:
            remove(file_path)
            end_time = time.time()
            spend_time = end_time - start_time
            usetime= f'{spend_time:.3f}'
            logger.debug(f"info: bigpcap {no} {bigpcap} is na no replay, len is {file_len}, \
                         usetime is {usetime} s")
        elif "@err.pcap" in bigpcap:
            remove(file_path)
            end_time = time.time()
            spend_time = end_time - start_time
            usetime= f'{spend_time:.3f}'
            logger.debug(f"info: bigpcap {no} {bigpcap} is err no replay, len is {file_len}, \
                         usetime is {usetime} s")
        elif "@ignore.pcap" in bigpcap:
            remove(file_path)
            end_time = time.time()
            spend_time = end_time - start_time
            usetime= f'{spend_time:.3f}'
            logger.debug(f"bigpcap {no} {bigpcap} is ignore no replay, len is {file_len},usetime is {usetime} s")
        else:
            command=f"pkt2flow  -uo {report_all_path} {file_path}"
            shell_command(command)
            replay_pcap(type,report_all_path,bigpcap,temp_path,no,config,frontpath)


    #report_all_path
    



    
    

# config=Config()
# #读取配置文件信息
# #py文件所在目录
# codepath = os.path.dirname(os.path.abspath(__file__))
# # py文件的上一级目录
# frontpath=os.path.dirname(codepath)
# ftp_get_file("appid",config,frontpath)
# # dealfile(frontpath)
# type="ips"
# report_all_path=os.path.join(frontpath, "report",type,"all/")
# no=1
# filename="ll"
# temp_path="/home/linhl/linhl-auto-py/temp"
# # replay_pcap(report_all_path,filename,temp_path,no,config)
#====================#
# commad="pkt2flow  -uo /home/linhl/linhl-auto-py/report/all /home/linhl/linhl-auto-py/data/pcap_appid_b/9-3-87-0_火萤-APP@iphone@20211209@yes.pcap"
# commad="ls -l "
# commad="scp "
# shell_command(commad)
#===================#

# init_firewall(type,config,frontpath)
# dealfile(frontpath)
# getfile(format,config,frontpath)
# pcap_check(type,config,frontpath)
# appzip=frontpath+"/data/file/app_signature.zip"
# # getfile("file",user,passwd,file_url,
# #             pcap_appid_url,pcap_ips_url,file_path,pcap_appid_path,pcap_ips_path)
# # delhttpfile(frontpath,file_url)


# update_dir="/home/linhl/linhl-auto-py/update"
# updateapp_judge(update_dir,"app_signature.zip",config)
# send_message("lin6666",config)
# send_file(config.hfs_report,config.feishu_appid_key_fs)
# updateappid(config,appzip)
# run_update_test("appid",appzip,config)