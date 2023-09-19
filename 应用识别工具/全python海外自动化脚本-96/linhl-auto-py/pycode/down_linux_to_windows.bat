chcp 65001
@echo off

setlocal

REM 远程 Linux 主机的 IP 地址和用户名
set linux_ip=10.51.213.206
set passwd=ruijie12345
set linux_user=root

REM 远程 Linux 目录
set linux_dir=/home/release/linhl/linhl-auto-py/pycode/

REM 本地 Windows 目录
set local_dir=%cd%

REM pscp 工具路径（需要提前下载和安装）
set pscp_path=C:\Program Files\PuTTY\pscp.exe

REM 循环遍历本地目录下的所有文件，并使用 pscp 工具上传到远程目录
    echo Down file
    "%pscp_path%" -r -pw %passwd% %linux_user%@%linux_ip%:%linux_dir%* %local_dir%
echo %local_dir%
@REM pause
echo Done.


