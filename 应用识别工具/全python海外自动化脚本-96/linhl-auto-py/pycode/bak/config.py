import os
import configparser

class Config:
    def __init__(self):
        # 获取当前Python文件所在目录
        codepath = os.path.dirname(os.path.abspath(__file__))
        # 获取上一级目录
        frontpath=os.path.dirname(codepath)

        # 读取配置文件
        self.config = configparser.ConfigParser()
        self.config.read(codepath+'/config.ini')

        # 从配置文件中获取默认配置信息
        self.host = self.config.get('DEFAULT', 'host')
        self.port = self.config.getint('DEFAULT', 'port')


        # 从配置文件中获取 DATABASE 节点配置信息
        self.database_host = self.config.get('DATABASE', 'host')
        self.database_port = self.config.getint('DATABASE', 'port')

        # 从配置文件中获取 logger 节点配置信息
        self.Level = self.config.get('logger', 'Level')
        self.log_path = self.config.get('logger', 'log_path')
        self.log_command_path = self.config.get('logger', 'log_command_path')

        # 从配置文件中获取 firewalld 节点配置信息
        self.firewalld_Xmac = self.config.get('firewalld', 'Xmac')
        self.firewalld_Ymac = self.config.get('firewalld', 'Ymac')
        self.firewalld_ip = self.config.get('firewalld', 'firewalld_ip')
        self.firewalld_web_user = self.config.get('firewalld', 'firewalld_web_user')
        self.firewalld_web_passwd = self.config.get('firewalld', 'firewalld_web_passwd')
        self.firewalld_shell_user = self.config.get('firewalld', 'firewalld_shell_user')
        self.firewalld_shell_passwd = self.config.get('firewalld', 'firewalld_shell_passwd')
        self.firewalld_hostname = self.config.get('firewalld', 'firewalld_hostname')
        self.firewalld_root_path = self.config.get('firewalld', 'firewalld_root_path')
        self.firewalld_ssh_port = self.config.getint('firewalld', 'sshport')

        # 从配置文件中获取 linux 节点配置信息
        self.linux_ethX = self.config.get('linux', 'ethX')
        self.linux_ethY = self.config.get('linux', 'ethY')
        self.linux_ip = self.config.get('linux', 'linux_ip')
        self.linux_user = self.config.get('linux', 'linux_user')
        self.linux_passwd = self.config.get('linux', 'linux_passwd')

        # 从配置文件中获取 hfs 节点配置信息
        self.hfs_user = self.config.get('hfs', 'user')
        self.hfs_passwd = self.config.get('hfs', 'passwd')
        self.hfs_file_url = self.config.get('hfs', 'file_url')
        self.hfs_pcap_appid_url = self.config.get('hfs', 'pcap_appid_url')
        self.hfs_pcap_ips_url = self.config.get('hfs', 'pcap_ips_url')

        # 从配置文件中获取 feishu 节点配置信息
        self.feishu_appid_key_fs = self.config.get('feishu', 'appid_key_fs')
        self.feishu_ips_key_fs = self.config.get('feishu', 'ips_key_fs')