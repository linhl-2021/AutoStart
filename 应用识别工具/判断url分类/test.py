from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys

def check_url_sort(check_url):
    # 要查询的 URL
    url = "https://www.fortiguard.com/webfilter"

    # 构建 payload 数据，这里使用一个示例字典
    payload = {
        'url': check_url,
        'webfilter_search_form_submit': 'submit',
        'ver': 9,
    }

    # 设置 User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'  # 替换成你自己的 User-Agent 字符串
    }

    # 发送 POST 请求，传递 payload 数据和请求头
    response = requests.post(url, data=payload, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        # 处理响应数据
        # 请根据实际情况解析响应数据
        # print(response.text)
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到所有 H4 标签
        h4_tags = soup.find_all('h4')

        # 打印 H4 标签的文本内容
        for h4_tag in h4_tags:
            if h4_tag.text.strip().startswith("Category"):
                # print(f"查询url为：{check_url}，查询结果为：{h4_tag.text.strip()}")
                return h4_tag.text.strip()
    else:
        print("无法访问网站")

def creat_result_file(src_filename,result_filename_csv,result_filename_excel):


    with open(result_filename_csv, 'w', encoding='utf-8') as file1:
            file1.write("666,666,666,666,666,666,666,666,666,666,666,develop,test,result"+"\n")
            file1.close()
    # 打开文件并逐行读取域名
    with open(src_filename, 'r',encoding='utf-8') as file:
        for line in file:
            # 去除每行两边的空白字符
            line = line.strip()
            develop = line.split(',')[-1]
            # 使用逗号分隔每行的内容
            domain = line.split(',')[1]
            # 调用查询函数并打印结果
            category = check_url_sort(domain).replace("Category: ", "")
            if develop in category:
                result="yes"
            else:
                result="no" 

            print(f"域名: {domain}, 分类信息: {category}")
            with open(result_filename_csv, 'a', encoding='utf-8') as file2:
                file2.write(f"{line},{category},{result}\n")
                file2.close()
    
    data = pd.read_csv(result_filename_csv, encoding='utf-8',error_bad_lines=False)

    writer = pd.ExcelWriter(result_filename_excel, engine="xlsxwriter")

    data.to_excel(writer, 'ok', header=True, index=False)

    workbook  = writer.book

    worksheet = writer.sheets['ok']

    # 垂直对齐方式
    # 水平对齐方式
    # 自动换行

    content_format = workbook.add_format({
        'valign': 'vcenter',
        'align': 'center',
        'text_wrap': True
    }) 

    worksheet.set_column("A:A",50, content_format)
    worksheet.set_column("B:B",45, content_format)
    worksheet.set_column("C:C",10, content_format)
    worksheet.set_column("D:D",5, content_format)
    worksheet.set_column("E:E",18, content_format)
    worksheet.set_column("F:F",75, content_format)
    worksheet.set_column("G:G",5, content_format)
    # 设置所有行高
    worksheet.set_default_row(82)

    writer.save()
    writer.close()

src_filename = "E:\\workspace\\python\\应用识别工具\\判断url分类\\1.csv"
result_filename_csv = "E:\\workspace\\python\\应用识别工具\\判断url分类\\20230919.csv"    
result_filename_excel= "E:\\workspace\\python\\应用识别工具\\判断url分类\\20230919.xlsx" 

creat_result_file(src_filename,result_filename_csv,result_filename_excel)