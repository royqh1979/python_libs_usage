#生成一百以内带退位减法 带进位加法

import win32com.client
import random

app = win32com.client.gencache.EnsureDispatch('Excel.Application')
excel_constants = win32com.client.constants

template_file = "g:/3位数竖式加减法作业模板.xlsx"
out_dir = "g:\\"
out_name = out_dir+"竖式"

max_number = 100
ratio_sub = 0.5
total_page = 1 # 总页数
seciton_per_page = 1 #每页的小节数
row_per_section = 8 #每页的行数
col_per_section = 3 #每页的列数
row_starts=[0]

workbook = app.Workbooks.Open(template_file)
# print(workbook.ActiveSheet.Cells(1,1).Value())

random.seed()
for page in range(total_page):
    for j in range(seciton_per_page):
        row_start = row_starts[j]
        for i in range(row_per_section*col_per_section):
            row = (i%row_per_section)*4+1
            col = i//row_per_section+1
            type_ratio=random.random()
            while True:
                x1 = random.randint(1,9)
                x2 = random.randint(0,9)
                x3 = random.randint(0,9)
                y1 = random.randint(1,9)
                y2 = random.randint(0,9)
                y3 = random.randint(0,9)
                x = x1*100+x2*10+x3
                y = y1*100+y2*10+y3
                z = x + y
                if z<=999 and  ( (y2+x2>9) or (y3+x3>9)):
                    break
            if type_ratio<ratio_sub:
                workbook.ActiveSheet.Cells(row + row_start, col).Value =   f"  {z}"
                workbook.ActiveSheet.Cells(row + row_start + 1, col).NumberFormatLocal = "@"
                workbook.ActiveSheet.Cells(row + row_start+1, col).Value = f"- {y}"
                workbook.ActiveSheet.Cells(row + row_start + 1, col).HorizontalAlignment =excel_constants.xlRight
                workbook.ActiveSheet.Cells(row + row_start + 1, col).Font.Underline =excel_constants.xlUnderlineStyleSingle

            else:
                workbook.ActiveSheet.Cells(row + row_start, col).Value =     f"  {x}"
                workbook.ActiveSheet.Cells(row + row_start + 1, col).NumberFormatLocal = "@"
                workbook.ActiveSheet.Cells(row + row_start + 1, col).Value = f"+ {y}"
                workbook.ActiveSheet.Cells(row + row_start + 1, col).HorizontalAlignment = excel_constants.xlRight
                workbook.ActiveSheet.Cells(row + row_start + 1, col).Font.Underline =excel_constants.xlUnderlineStyleSingle

    out_file = f"{out_name}{page+1:03d}.pdf"
    print(out_file)
    workbook.ActiveSheet.ExportAsFixedFormat(excel_constants.xlTypePDF,out_file,
                                             Quality = excel_constants.xlQualityStandard,
                                             IncludeDocProperties = True,
                                             IgnorePrintAreas=False,
                                             OpenAfterPublish=False)

workbook.Close(SaveChanges=False)
app.Quit()

