import logging
from logging.handlers import TimedRotatingFileHandler
import os
from config import Config

def setup_logging(Level,log_path):
    # 创建一个名为my_logger的日志记录器
    my_logger = logging.getLogger("my_logger")
    # my_logger.setLevel(logging.DEBUG)
    my_logger.setLevel(Level) 

    # 创建一个输出格式
    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d - %(levelname)s - %(message)s')

    # 创建一个控制台处理程序，并将其添加到日志记录器中
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    my_logger.addHandler(console_handler)

    # 创建一个文件处理程序，并将其添加到日志记录器中
    file_handler = TimedRotatingFileHandler(log_path,when='midnight', backupCount=2)
    file_handler.setFormatter(formatter)
    my_logger.addHandler(file_handler)

    return my_logger

config = Config()
codepath = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(codepath, config.log_path)
if os.path.exists(log_path):
    with open(log_path, 'w'):
        pass  # 清空文件内容
logger = setup_logging(config.Level,config.log_path)
# appid_key_fs = "1dd56c87-e54e-4151-8bc3-159c8477c79e"
# type="appid"
# logger.debug(f"文件内容为： {type}---飞书群key为： {appid_key_fs}")
    
