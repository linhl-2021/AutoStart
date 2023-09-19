import pexpect
from log_module import logger
from config import Config

config=Config()
log_file = config.log_command_path
command=f'ssh-keygen -R 172.28.247.85'
child = pexpect.spawn(command,encoding='utf-8',timeout=5)

command=f"ssh root@172.28.247.85"
# log_file = "/home/linhl/linhl-auto-py/pycode/bak/log.txt"
# child = pexpect.spawn(command,logfile=open(log_file, "wb"),timeout=10)
child = pexpect.spawn(command,timeout=10)
output_index = child.expect([pexpect.EOF, pexpect.TIMEOUT,".*yes.*"])
child.sendline("yes")
output_index = child.expect([pexpect.EOF, pexpect.TIMEOUT,"password:"])
child.sendline("Ruijie@123")
output_index = child.expect([pexpect.EOF, pexpect.TIMEOUT,"#"])
child.sendline("exit")
for line in child:
    logger.debug(f"Index: {output_index}")
    logger.debug(child.before.decode())