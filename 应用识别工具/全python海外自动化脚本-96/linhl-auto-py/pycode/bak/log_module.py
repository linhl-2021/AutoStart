import logging

def setup_logging():
    # 创建一个名为my_logger的日志记录器
    my_logger = logging.getLogger("my_logger")
    # my_logger.setLevel(logging.DEBUG)
    my_logger.setLevel("DEBUG") 

    # 创建一个输出格式
    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d - %(levelname)s - %(message)s')

    # 创建一个控制台处理程序，并将其添加到日志记录器中
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    my_logger.addHandler(console_handler)

    # 创建一个文件处理程序，并将其添加到日志记录器中
    file_handler = logging.FileHandler('my_log_file.log')
    file_handler.setFormatter(formatter)
    my_logger.addHandler(file_handler)

    return my_logger
    
logger = setup_logging()
