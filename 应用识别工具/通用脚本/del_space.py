import os
import shutil

# 获取当前目录下所有文件的列表
path="D:\\工作\\20230220应用识别用例\\海外激活\\pacp\\all\\English\\7-EN\\loubao"
pathchange="D:\\工作\\20230220应用识别用例\\海外激活\\pacp\\all\\English\\7-EN\\loubao\\change"
for file_name in os.listdir(pathchange):
    file_path = os.path.join(pathchange, file_name)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"已删除文件：{file_path}")
    except Exception as e:
        print(f"删除文件{file_path}时出错：{e}")
file_list = os.listdir(path)
print(file_list)
# 遍历每个文件名，如果包含空格就重命名
for filename in file_list:
    if "change" not in filename:
        print(filename)
        basename, extension = os.path.splitext(filename)
        print(basename + "===="+extension)
        basename=basename.strip()
        basename = basename.replace(' ', '-')
        basename = basename.replace(' ', '-')
        basename = basename.replace('（', '(')
        basename = basename.replace('）', ')')
        # os.rename(path+"\\"+filename, path+"\\change\\"+basename+".pcap")
        shutil.copy2(os.path.join(path, filename), os.path.join(pathchange, basename + extension))
