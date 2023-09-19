import paramiko

def ip_check(host,username,password,port):
    # 建立SSH连接
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    i = 0
    while i<=5:
        ip = generate_ip_address()
        # print(ip)
        # ip = '200.200.11.101'
        # 执行多个命令
        command999 = "kill -9 $(ps -ef | grep root | grep pts |grep -v `echo ${SSH_TTY:5}` |grep -v bash | awk '{print $2}')"
        commands = [f'fpcmd fp ti detect 2 ip {ip}',f' fpcmd fp ti detect 1 ip {ip}']
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            result = stdout.read().decode()
            error = stderr.read().decode()
            if error:
                print(f"Error executing command {command}: {error}")
            else:
                if "bad" in result :
                    i=i+1
                    print(i)
                    print(f"Result of command {command}: {result}")
    # 关闭SSH连接
    ssh.close()
import random

def generate_ip_address():
    # 随机生成四个数字作为 IP 地址的四个部分
    a = random.randint(0, 255)
    b = random.randint(0, 255)
    c = random.randint(0, 255)
    d = random.randint(0, 255)
    # 拼接成 IP 地址
    ip_address = f'{a}.{b}.{c}.{d}'
    return ip_address


# print(generate_ip_address())
ip_check('10.51.212.30','root','ruijie@123','20')