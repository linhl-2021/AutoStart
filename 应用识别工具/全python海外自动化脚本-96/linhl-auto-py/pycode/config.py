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

        if self.config.getboolean('firewalld01','config'):
            firewalld='firewalld01'
            linux='linux01'
        elif self.config.getboolean('firewalld02','config'):
            firewalld='firewalld02'
            linux='linux02'
        else:
            firewalld='firewalld03'
            linux='linux03'
        # 从配置文件中获取 firewalld 节点配置信息
        self.firewalld_c_mac = self.config.get(firewalld, 'firewalld_c_mac')
        self.firewalld_s_mac = self.config.get(firewalld, 'firewalld_s_mac')
        self.firewalld_c_ip = self.config.get(firewalld, 'firewalld_c_ip')
        self.firewalld_s_ip = self.config.get(firewalld, 'firewalld_s_ip')
        self.firewalld_c_ip_V6 = self.config.get(firewalld, 'firewalld_c_ip_V6')
        self.firewalld_s_ip_V6 = self.config.get(firewalld, 'firewalld_s_ip_V6')
        self.firewalld_ip = self.config.get(firewalld, 'firewalld_ip')
        self.firewalld_web_user = self.config.get(firewalld, 'firewalld_web_user')
        self.firewalld_web_passwd = self.config.get(firewalld, 'firewalld_web_passwd')
        self.firewalld_shell_user = self.config.get(firewalld, 'firewalld_shell_user')
        self.firewalld_shell_passwd = self.config.get(firewalld, 'firewalld_shell_passwd')
        self.firewalld_hostname = self.config.get(firewalld, 'firewalld_hostname')
        self.firewalld_root_path = self.config.get(firewalld, 'firewalld_root_path')
        self.firewalld_ssh_port = self.config.getint(firewalld, 'sshport')

        # 从配置文件中获取 linux 节点配置信息
        self.linux_c_eth = self.config.get(linux, 'linux_c_eth')
        self.linux_s_eth = self.config.get(linux, 'linux_s_eth')
        self.linux_c_mac = self.config.get(linux, 'linux_c_mac')
        self.linux_s_mac = self.config.get(linux, 'linux_s_mac')
        self.linux_c_ip = self.config.get(linux, 'linux_c_ip')
        self.linux_s_ip = self.config.get(linux, 'linux_s_ip')
        self.linux_c_ip_V6 = self.config.get(linux, 'linux_c_ip_V6')
        self.linux_s_ip_V6 = self.config.get(linux, 'linux_s_ip_V6')
        self.linux_ip = self.config.get(linux, 'linux_ip')
        self.linux_user = self.config.get(linux, 'linux_user')
        self.linux_passwd = self.config.get(linux, 'linux_passwd')
        self.appid_library_back = self.config.get(linux, 'appid_library_back')
        self.ips_library_back = self.config.get(linux, 'ips_library_back')
        self.ip_c_segment = self.config.get(linux, 'ip_c_segment')
        self.ip_s_segment = self.config.get(linux, 'ip_s_segment')
        self.ip_c_segmentv6 = self.config.get(linux, 'ip_c_segmentv6')
        self.ip_s_segmentv6 = self.config.get(linux, 'ip_s_segmentv6')
        self.pcap_cyclenum = self.config.get(linux, 'cyclenum')

        # 从配置文件中获取 ftp 节点配置信息
        self.ftp_ip = self.config.get('ftp', 'ip')
        self.ftp_port = self.config.get('ftp', 'port')
        self.ftp_user = self.config.get('ftp', 'user')
        self.ftp_passwd = self.config.get('ftp', 'passwd')
        self.ftp_file_url = self.config.get('ftp', 'file_url')
        self.ftp_pcap_appid_url = self.config.get('ftp', 'pcap_appid_url')
        self.ftp_pcap_av_url = self.config.get('ftp', 'pcap_av_url')
        self.ftp_pcap_ips_url = self.config.get('ftp', 'pcap_ips_url')
        self.ftp_report = self.config.get('ftp', 'report')

        # 从配置文件中获取 feishu 节点配置信息
        self.feishu_appid_key_fs = self.config.get('feishu', 'appid_key_fs')
        self.feishu_ips_key_fs = self.config.get('feishu', 'ips_key_fs')

        # 从配置文件中获取 hfs 节点配置信息
        self.hfs_user = self.config.get('hfs', 'user')
        self.hfs_passwd = self.config.get('hfs', 'passwd')
        self.hfs_file_url = self.config.get('hfs', 'file_url')
        self.hfs_pcap_appid_url = self.config.get('hfs', 'pcap_appid_url')
        self.hfs_pcap_ips_url = self.config.get('hfs', 'pcap_ips_url')
        self.hfs_report = self.config.get('hfs', 'report')