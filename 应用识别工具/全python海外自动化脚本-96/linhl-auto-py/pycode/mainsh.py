import configparser
import os
import requests
import subprocess
import time
from dealfile import dealfile, delhttpfile, ftp_del_file, ftp_get_file, getfile, pcap_check, shell_command, updatefeature
from log_module import logger
from config import Config

#py文件所在目录
codepath = os.path.dirname(os.path.abspath(__file__))
#py文件的上一级目录
frontpath=os.path.dirname(codepath)




if True:
    # time.sleep(10)
    config = Config()
    dealfile(frontpath)
    data_file_path = os.path.join(frontpath, "data", "file/")
    shell_command(f"mkdir -p {data_file_path}")
    
    logger.debug("开始下载文件")
    ftp_get_file("file",config,frontpath)
    
    # 根据下载的文件需求设置主要参数
    os.chdir(frontpath)
    if os.path.exists("data/file/test"):
        appid_key = ""
        ips_key = ""
        appid_key_fs = config.feishu_appid_key_fs
        ips_key_fs = config.feishu_ips_key_fs
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
        appid_key_fs = "08c71cec-15b3-4630-ab30-eafa6e6c2b10"
        logger.debug("不存在文件test，ok")
        exit(0)
    logger.debug(f"文件内容为： {type}---飞书群key为： {appid_key_fs}")
    if  type:
        ftp_get_file(type,config,frontpath)

    #删除文件
    ftp_del_file(frontpath,config)    
    # break
    # 特征库下发升级获取升级结果
    updatefeature(config,frontpath)
    if type:
        pcap_check(type,config,frontpath)
    
    #
    
    
    
