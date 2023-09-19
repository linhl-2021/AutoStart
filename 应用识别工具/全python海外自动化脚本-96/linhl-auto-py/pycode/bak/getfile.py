import configparser
import os
import subprocess
import urllib.request
import base64
from log_module import logger


def getfile(format,user,passwd,file_url,
            pcap_appid_url,pcap_ips_url,file_path,pcap_appid_path,pcap_ips_path):
    # 初始化
    # 设置下载参数
    #创建目录
    os.makedirs(file_path, exist_ok=True)
    os.makedirs(pcap_appid_path, exist_ok=True)
    os.makedirs(pcap_ips_path, exist_ok=True)
    command=""
    if format == "file":
        command = command = [
        "wget","-c","-r","-np","-nd","-nH","-R","html,tmp","--no-http-keep-alive",
        "--http-user={0}".format(user),"--http-password={0}".format(passwd),file_url,
        "-P",file_path
        ]
    elif format == "appid":
        command = command = [
        "wget","-c","-r","-np","-nd","-nH","-R","html,tmp","--no-http-keep-alive",
        "--http-user={0}".format(user),"--http-password={0}".format(passwd),pcap_appid_url,
        "-P",pcap_appid_path
        ]
    elif format == "ips":
        command = command = [
        "wget","-c","-r","-np","-nd","-nH","-R","html,tmp","--no-http-keep-alive",
        "--http-user={0}".format(user),"--http-password={0}".format(passwd),pcap_ips_url,
        "-P",pcap_ips_path
        ]
    else:
        logger.debug("文件内容错误")     
        return  command 

    # 执行命令
    subprocess.run(command)
        

def printpwd():
    codepath = os.path.dirname(os.path.abspath(__file__))
    frontpath=os.path.dirname(codepath)
    print(frontpath)

#py文件所在目录
codepath = os.path.dirname(os.path.abspath(__file__))
#py文件的上一级目录
frontpath=os.path.dirname(codepath)
config = configparser.ConfigParser()
config.read(codepath+'/config.ini')
#用户
user = config.get('hfs', 'user')
passwd = config.get('hfs', 'passwd')
#hfs路径
file_url = config.get('hfs', 'file_url')
pcap_appid_url = config.get('hfs', 'pcap_appid_url')
pcap_ips_url = config.get('hfs', 'pcap_ips_url')
#下载的文件存放路径
file_path = os.path.join(frontpath, "data", "file")
pcap_appid_path = os.path.join(frontpath, "data", "pcap_appid_temp")
pcap_ips_path = os.path.join(frontpath, "data", "pcap_ips_temp")

# getfile("file",user,passwd,file_url,
#             pcap_appid_url,pcap_ips_url,file_path,pcap_appid_path,pcap_ips_path)
