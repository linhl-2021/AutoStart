import pandas as pd
import sys
args1 = sys.argv[1:]
args2 = sys.argv[2:]

data = pd.read_csv(args1[0], encoding='utf-8',error_bad_lines=False)

writer = pd.ExcelWriter(args2[0], engine="xlsxwriter")

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
