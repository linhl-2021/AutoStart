import configparser
import os
import subprocess
import urllib.request
from hdfs import InsecureClient
import paramiko
import pexpect
import requests
import base64
from log_module import logger


codepath = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(codepath+'/config.ini')

def getconfig():

    z5100Xmac = config.get('Z5100', 'z5100Xmac')
    z5100Ymac = config.get('Z5100', 'z5100Ymac')
    z5100ethX = config.get('Z5100', 'z5100ethX')
    z5100ethY = config.get('Z5100', 'z5100ethY')
    file_url = config.get('hfs', 'file_url')
    pcap_appid_url = config.get('hfs', 'pcap_appid_url')
    pcap_ips_url = config.get('hfs', 'pcap_ips_url')

    # username = config.get('DATABASE', 'username')
    # password = config.get('DATABASE', 'password')
    # database = config.get('DATABASE', 'database')
    print(z5100Xmac)
    print(z5100Ymac)
    print(z5100ethX)
    print(z5100ethY)
    print(file_url)
    print(pcap_appid_url)
    print(pcap_ips_url)

def printpwd():
    file_path = os.path.abspath(__file__)
    print(file_path)

def downfile():
    codepath = os.getcwd()
    print("codepath: "+codepath)
    os.chdir("..")
    frontpath = os.getcwd()
    file_path = os.path.join(frontpath, "data", "file")
    pcap_appid_path = os.path.join(frontpath, "data", "pcap_appid_temp")
    pcap_ips_path = os.path.join(frontpath, "data", "pcap_ips_temp")
    os.makedirs(file_path, exist_ok=True)
    os.makedirs(pcap_appid_path, exist_ok=True)
    os.makedirs(pcap_ips_path, exist_ok=True)
    # 设置下载参数
    file_url = config.get('hfs', 'file_url')
    user = config.get('hfs', 'user')
    passwd = config.get('hfs', 'passwd')
    user = "username"
    passwd = "password"
    headers = {
        "User-Agent": "Mozilla/5.0", 
        "Authorization": f"Basic {base64.b64encode(f'{user}:{passwd}'.encode()).decode()}"
    }
    url = urllib.request.Request(file_url, headers=headers)
    urllib.request.urlretrieve(url=url, filename=os.path.join(file_path, "filename"), reporthook=None, data=None)
    # getconfig()
    # test2("file")

#===================================

def sshcommand():
    hostname = config.get('firewalld', 'firewalldip')
    username = config.get('firewalld', 'firewallduser')
    password = config.get('firewalld', 'firewalldpasswd')
    linuxip = config.get('linux', 'linuxip')
    linuxuser = config.get('linux', 'linuxuser')
    linuxpasswd = config.get('linux', 'linuxpasswd')
    logger.info(hostname)
    logger.info(username)
    logger.info(password)
    firewalldrootpath = config.get('firewalld', 'firewalldrootpath')

    # 连接到远程Linux系统
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, 22,username, password)

    # 执行第一个shell命令
    # stdin, stdout, stderr = client.exec_command('ls -l')
    # result = stdout.read().decode('utf-8')
    # logger.info(result)
    # 检查结果中是否包含关键字
    # if 'firewall' in result:
    #     # 如果包含，则执行第二个shell命令
    #     stdin, stdout, stderr = client.exec_command('sudo rm -rf /root/app*.zip')
    path='/home/linhl/linhl-auto-py/pycode/test.py'
    # 然后执行第三个shell命令
    commad1='sudo rm -rf '+firewalldrootpath+'/app*.zip'


    # 获取系统信息并写入日志文件
    log_file_path = '/mnt/flash/app-rules.log'
    info_command1 = 'sudo cat /etc/os-release|head -n 1'
    info_command2 = 'sudo cat /etc/.release'
    info_command3 = 'sudo cat /etc/.releaseID'
    info_command4 = 'sudo fpcmd fp app-id show version'
    get_info_command = f'{info_command1} > {log_file_path}; {info_command2} >> {log_file_path}; {info_command3} >> {log_file_path}'
    stdin, stdout, stderr = client.exec_command(get_info_command)
    logger.info(stdout.channel.recv_exit_status())

    # result = stdout.read().decode('utf-8')
    logger.info(stdout1.channel.recv_exit_status())
    logger.info(stdout2.channel.recv_exit_status())
    logger.info(stdout3.channel.recv_exit_status())
    logger.info(stdout4.channel.recv_exit_status())
    logger.info(result)

    # 关闭SSH连接
    client.close()
    
def sshcommandtest():
    hostname = config.get('firewalld', 'firewalldip')
    username = config.get('firewalld', 'firewallduser')
    password = config.get('firewalld', 'firewalldpasswd')
    linuxip = config.get('linux', 'linuxip')
    linuxuser = config.get('linux', 'linuxuser')
    linuxpasswd = config.get('linux', 'linuxpasswd')
    logger.info(hostname)
    logger.info(username)
    logger.info(password)
    firewalldrootpath = config.get('firewalld', 'firewalldrootpath')

    # 连接到远程Linux系统
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, 22,username, password)

    # 执行第一个shell命令
    stdin, stdout, stderr = client.exec_command('ls -l')
    result = stdout.read().decode('utf-8')
    logger.info(result)
    get_info_command = f'{"sudo fpcmd fp app-id debug file on"} '
    stdin, stdout, stderr = client.exec_command(get_info_command)
    result = stdout.read().decode('utf-8')
    logger.info(stdout.channel.recv_exit_status())
    logger.info(result)

def scpcommand():
    child = pexpect.spawn('scp -r test.py root@172.28.247.85:/root',encoding='utf-8',timeout=5)
    child.expect('password:')
    child.sendline('Ruijie@123')
    child.expect(pexpect.EOF)
scpcommand()