#生成一百以内带退位减法 带进位加法

from comtypes.client import CreateObject,Constants
import random


app = CreateObject("Excel.Application")
excel_constants = Constants(app)

template_file = "g:/带余数除法口算作业模板.xlsx"
out_dir = "g:\\"
out_name = out_dir+"口算"

total_page = 10 # 总页数
seciton_per_page = 2 #每页的小节数
row_per_section = 10 #每页的行数
col_per_section = 3 #每页的列数
row_starts=[2, 16]

workbook = app.Workbooks.open(template_file)
# print(workbook.ActiveSheet.Cells(1,1).Value())

random.seed()
for page in range(total_page):
    for j in range(seciton_per_page):
        row_start = row_starts[j]
        for i in range(row_per_section*col_per_section):
            row = i%row_per_section+1
            col = i//row_per_section+1
            x1 = random.randint(11,99)
            x2 = random.randint(2,9)

            str = f"{x1} x {x2} = "

            workbook.ActiveSheet.Cells(row + row_start, col).Value[()]=str
    out_file = f"{out_name}{page+1:03d}.pdf"
    print(out_file)
    workbook.ActiveSheet.ExportAsFixedFormat(excel_constants.xlTypePDF,out_file,
                                             Quality = excel_constants.xlQualityStandard,
                                             IncludeDocProperties = True,
                                             IgnorePrintAreas=False,
                                             OpenAfterPublish=False)

workbook.Close(SaveChanges=False)
app.Quit()
