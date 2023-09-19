import configparser
import os
import requests
import subprocess
import time
from dealfile import dealfile, delhttpfile, getfile, updatefeature
from log_module import logger
from config import Config

#py文件所在目录
codepath = os.path.dirname(os.path.abspath(__file__))
#py文件的上一级目录
frontpath=os.path.dirname(codepath)
# config = configparser.ConfigParser()
# config.read(codepath+'/config.ini')
# #用户
# user = config.get('hfs', 'user')
# passwd = config.get('hfs', 'passwd')
# #hfs路径
# file_url = config.get('hfs', 'file_url')
# pcap_appid_url = config.get('hfs', 'pcap_appid_url')
# pcap_ips_url = config.get('hfs', 'pcap_ips_url')
#下载的文件存放路径
file_path = os.path.join(frontpath, "data", "file")
pcap_appid_path = os.path.join(frontpath, "data", "pcap_appid_temp")
pcap_ips_path = os.path.join(frontpath, "data", "pcap_ips_temp")
# #飞书机器人key
# appid_key_fs = config.get('feishu', 'appid_key_fs')
# ips_key_fs = config.get('feishu', 'file_url')
# linuxip = config.get('linux', 'linuxip')
# linuxuser = config.get('linux', 'linuxuser')
# linuxpasswd = config.get('linux', 'linuxpasswd')
# firewalldip = config.get('firewalld', 'firewalldip')
# firewallduser = config.get('firewalld', 'firewallduser')
# firewalldpasswd = config.get('firewalld', 'firewalldpasswd')
# firewalldhostname = config.get('firewalld', 'firewalldhostname')
# firewalldrootpath = config.get('firewalld', 'firewalldrootpath')
config = Config()

while True:
    time.sleep(10)
    dealfile(codepath,frontpath)
    getfile("file",config.hfs_user,config.hfs_passwd,config.hfs_file_url,config.hfs_pcap_appid_url,config.hfs_pcap_ips_url,
            config.file_path,config.pcap_appid_path,config.pcap_ips_path)

    # 根据下载的文件需求设置主要参数
    os.chdir(frontpath)
    if os.path.exists("data/file/test"):
        appid_key = ""
        ips_key = ""
        appid_key_fs = ""
        ips_key_fs = ""
        debug = "test"
        with open("data/file/test") as f:
            type = f.read()
    elif os.path.exists("data/file/ok"):
        appid_key = "f7a44f62-d361-4db9-a6ac-556007faf234"
        ips_key = "faf4bf93-a33e-455b-9a32-c2736fbdafb0"
        appid_key_fs = "08c71cec-15b3-4630-ab30-eafa6e6c2b10"
        ips_key_fs = "1dd56c87-e54e-4151-8bc3-159c8477c79e"
        debug = "formal"
        with open("data/file/ok") as f:
            type = f.read()
    else:
        continue
    logger.debug("文件内容为： "+type+"---飞书群key为： "+appid_key_fs)

    #删除文件
    delhttpfile(frontpath,file_url)    

    # 特征库下发升级获取升级结果
    updatefeature(linuxip,linuxuser,linuxpasswd,firewalldip,firewallduser,firewalldpasswd,firewalldhostname
            ,firewalldrootpath,frontpath)

    
