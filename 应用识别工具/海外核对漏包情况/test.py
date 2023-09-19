import filecmp
import os
import shutil

#判断src_path目录下的文件名不在dest_path1，dest_path2目录下
def compare_files(src_path, dest_path1, dest_path2):
    # 获取源目录和其他目标目录下的文件列表
    src_files = os.listdir(src_path)
    dest1_files = os.listdir(dest_path1)
    dest2_files = os.listdir(dest_path2)

    # 遍历源目录下的文件
    # for file in src_files:
    #     src_file_path = os.path.join(src_path, file)
    #     dest_file_path = os.path.join(dest_path4, file)

    #     # 判断该文件是否存在于其他目标目录中
    #     if file not in dest1_files and file not in dest2_files and file not in dest3_files:
    #         shutil.copy(src_file_path, dest_file_path)
    #         print(f"File {file} copied from {src_path} to {dest_path4}")
    for file in src_files:
        src_file_path = os.path.join(src_path, file)
        if file not in dest1_files and file not in dest2_files :
            print(f"{src_file_path} 存在漏包 ")

#判断dest_path1，dest_path2目录下的文件名不在目录下src_path
def compare_files2(src_path, dest_path1, dest_path2):
    # 获取源目录和其他目标目录下的文件列表
    src_files = os.listdir(src_path)
    dest1_files = os.listdir(dest_path1)
    dest2_files = os.listdir(dest_path2)

    # 遍历源目录下的文件
    # for file in src_files:
    #     src_file_path = os.path.join(src_path, file)
    #     dest_file_path = os.path.join(dest_path4, file)

    #     # 判断该文件是否存在于其他目标目录中
    #     if file not in dest1_files and file not in dest2_files and file not in dest3_files:
    #         shutil.copy(src_file_path, dest_file_path)
    #         print(f"File {file} copied from {src_path} to {dest_path4}")
    for file1 in dest1_files:
        src_file_path = os.path.join(dest_path1, file1)
        if file1 not in src_files :
            print(f"{src_file_path} 不存在总包下 ")
    for file2 in dest2_files:
        src_file_path = os.path.join(dest_path2, file2)
        if file2 not in src_files :
            print(f"{src_file_path} 不存在总包下 ")

#判断dest_path1，dest_path2目录下的文件名相同
def compare_files3(dest_path1, dest_path2):
    # 获取源目录和其他目标目录下的文件列表
    dest1_files = os.listdir(dest_path1)
    dest2_files = os.listdir(dest_path2)
    for file1 in dest1_files:
        src_file_path = os.path.join(dest_path1, file1)
        if file1  in dest2_files :
            print(f"{src_file_path} 存在相同文件 ")
    # for file2 in dest2_files:
    #     src_file_path = os.path.join(dest_path2, file2)
    #     if file2 not in src_files :
    #         print(f"{src_file_path} 不存在总包下 ")
    

def copy_files(src_path, dest_path1, dest_path2, dest_path3, dest_path4):
    # 获取源目录和其他目标目录下的文件列表
    src_files = os.listdir(src_path)
    dest1_files = os.listdir(dest_path1)
    dest2_files = os.listdir(dest_path2)
    dest3_files = os.listdir(dest_path3)

    # 遍历源目录下的文件
    for file in src_files:
        src_file_path = os.path.join(src_path, file)
        dest_file_path = os.path.join(dest_path4, file)

        # 判断该文件是否存在于其他目标目录中
        if file not in dest1_files and file not in dest2_files and file not in dest3_files:
            shutil.copy(src_file_path, dest_file_path)
            print(f"File {file} copied from {src_path} to {dest_path4}")

def copy_sim_files(src_path, dest_path1, dest_path2, dest_path3, dest_path4):
    # 获取源目录和其他目标目录下的文件列表
    src_files = os.listdir(src_path)
    dest1_files = os.listdir(dest_path1)
    dest2_files = os.listdir(dest_path2)
    dest3_files = os.listdir(dest_path3)

    # 遍历源目录下的文件
    # for file in src_files:
    #     src_file_path = os.path.join(src_path, file)
    #     dest_file_path = os.path.join(dest_path2, file)
    #     file_name=file.split('_')[1].split('@')[0]
    #     print(file_name)
    #     # 判断该文件是否存在于其他目标目录中
    #     for file2 in dest1_files:
    #         if file_name in file2:
    #             shutil.copy(src_file_path, dest_file_path)
    #             print(f"File {file} copied from {src_path} to {dest2_files}")
    
    
    for file1 in dest1_files:
        flag = False
        for  file2 in dest2_files:
            file_name=file2.split('_')[1].split('@')[0]
            if  file_name  in file1 :
                flag=True
                break
            else:
                flag=False
                continue
        if not flag: 
            print(f"缺少： {file1}")

def judge_file(src_path, dest_path1):
    src_files = os.listdir(src_path)
    dest1_files = os.listdir(dest_path1)
    for file_name in src_files:
        file_name = file_name.replace(' ', '-')
        file_name = file_name.replace(' ', '-')
        file_name = file_name.replace('（', '(')
        file_name = file_name.replace('）', ')')
        for file in dest1_files:
            file = file.replace(' ', '-')
            file = file.replace(' ', '-')
            file = file.replace('（', '(')
            file = file.replace('）', ')')
            if  file_name == file:
                flag=True
                break
            else:
                flag=False
        if not flag: 
            print(file_name)

# 测试代码
src_path = "D:\\工作\\20230220应用识别用例\\海外激活\\pacp\\all\\EN\\1-CH\\总包"
dest_path1 = "D:\\工作\\20230220应用识别用例\\海外激活\\pacp\\all\\EN\\1-CH\\原始包-合格"
dest_path2 = "D:\\工作\\20230220应用识别用例\\海外激活\\pacp\\all\\EN\\1-CH\\不合格"
dest_path3 = "D:\\工作\\20230220应用识别用例\\海外激活\\pacp\\all\\English\\7-EN\\原始包-不合格"
dest_path4 = "D:\\工作\\20230220应用识别用例\\海外激活\\pacp\\all\\English\\7-EN\\漏包"
# judge_file(src_path, dest_path1)
# copy_files(src_path, dest_path1, dest_path2, dest_path3, dest_path4)
# compare_files(src_path, dest_path1, dest_path2)
# compare_files2(src_path, dest_path1, dest_path2)
compare_files3(dest_path1, dest_path2)
