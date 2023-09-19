chcp 65001
@echo off

setlocal

REM 远程 Linux 主机的 IP 地址和用户名
set linux_ip=10.51.213.206
set linux_user=root

REM 远程 Linux 目录
set linux_dir=/home/release/linhl/linhl-auto-py/

REM 本地 Windows 目录
set local_dir=%cd%

REM pscp 工具路径（需要提前下载和安装）
set pscp_path=C:\Program Files\PuTTY\pscp.exe


"%pscp_path%" -r -pw ruijie12345 %local_dir% %linux_user%@%linux_ip%:"%linux_dir%"

echo %local_dir%
@REM pause
echo Done.


