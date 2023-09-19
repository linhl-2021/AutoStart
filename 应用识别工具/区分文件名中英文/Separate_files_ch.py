import datetime
import os
import re
import shutil

def has_chinese(string):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    match = pattern.search(string)
    return match is not None

def list_directory(sourcedir):
    Chinese=sourcedir+"\\Chinese"
    English=sourcedir+"\\English"
    if not os.path.exists(Chinese):
        os.makedirs(Chinese)
    if not os.path.exists(English):
        os.makedirs(English)

    for file_name in os.listdir(sourcedir):
        if ("Chinese" not in file_name) and "English" not in file_name and "-bak-" not in file_name:
            print(file_name)
            basename_last, extension = os.path.splitext(file_name)
            basename=basename_last.replace('安卓', '')
            basename=basename.replace('加识别', '')
            basename=basename.replace('识别为雅虎网', '')
            basename=basename.replace('苹果', '')
            basename=basename.replace('网页', '')
            basename=basename.replace('邮箱', '')
            basename=basename.replace('语音', '')
            basename=basename.replace('客户端', '')
            basename=basename.replace('识别不了', '')
            basename=basename.replace('识别', '')
            basename=basename.replace('浏览器', '')
            basename=basename.replace('改名为', '')
            basename=basename.replace('噗浪', '')
            print(basename,"========="+extension)
            if has_chinese(basename):
                shutil.copy2(os.path.join(sourcedir,basename_last+extension), os.path.join(Chinese, basename_last+extension))
            else:
                shutil.copy2(os.path.join(sourcedir,basename_last+extension), os.path.join(English, basename_last+extension))
            # 获取当前时间
            now = datetime.datetime.now()
            # 格式化时间为字符串：年月日时分秒
            timestamp = now.strftime("%Y%m%d")
    for file_name in os.listdir(sourcedir):
        if ("Chinese" not in file_name) and "English" not in file_name and "-bak-" not in file_name:
            print(file_name,"========="+extension)
            bakdir=sourcedir+"\\"+timestamp+"-bak-"
            if  not os.path.exists(bakdir):
                os.makedirs(bakdir)
            shutil.move(os.path.join(sourcedir,file_name), os.path.join(bakdir, file_name))
    

if __name__ == '__main__':
    list_directory('D:\\工作\\20230220应用识别用例\\海外激活\\pacp\\all\\20230330')
