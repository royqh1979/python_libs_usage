#生成一百以内带退位减法 带进位加法

from comtypes.client import CreateObject,Constants
import random


app = CreateObject("Excel.Application")
excel_constants = Constants(app)

template_file = "g:/带余数除法口算作业模板.xlsx"
out_dir = "g:\\"
out_name = out_dir+"口算"

total_page = 30 # 总页数
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
            x3 = random.randint(11,99)
            t1 = random.choice([1,2])
            t2 = random.choice([1,2])
            t3 = random.choice([1,2])
            t4 = random.choice([1,2,3])
            str = '';
            y = 0;

            if t4 == 1: #前方括号
                if t1 == 1:  # 先乘除
                    if t2 == 1:  # 乘
                        while True:
                            x1 = random.randint(11, 99)
                            x2 = random.randint(2, 9)
                            str1 = f"{x1} * {x2}"
                            y=x1*x2
                            if y<100:
                                break
                    else:
                        while True:
                            x1 = random.randint(11, 99)
                            x2 = random.randint(2, 9)
                            str1 = f"{x1*x2} ÷ {x2}"
                            y=x1
                            if x1*x2<100:
                                break
                else:
                    x1 = random.randint(11, 99)
                    x2 = random.randint(11, 99)
                    if t2 == 1: # 加
                        while x1+x2>99:
                            x1 = random.randint(11, 99)
                            x2 = random.randint(11, 99)
                        str1 = f"{x1} + {x2}"
                        y=x1+x2
                    else:
                        if x1>x2:
                            str1 = f"{x1} - {x2}"
                            y=x1-x2
                        else:
                            str1 = f"{x2} - {x1}"
                            y=x2-x1
                str1 = "("+str1+")"
                if t1==1: #后加减
                    if t3 == 1 : #加
                        x1 = random.randint(11, 99)
                        str = f"{str1} + {x1}"
                    else:
                        x1 = random.randint(0,y)
                        str = f"{str1} - {x1}"
                else:
                    if (t3 == 1) or (y<10): #乘
                        if y>9:
                            x1 = random.randint(2, 9)
                        else:
                            x1 = random.randint(11,99)
                        str = f"{str1} * {x1}"
                    else:
                        x1 = random.randint(2,9)
                        str = f"{str1} ÷ {x1}"
            elif t4 == 2: #后方括号
                if t1 == 1:  # 后乘除
                    if t2 == 1:  # 乘
                        while True:
                            x1 = random.randint(11, 99)
                            x2 = random.randint(2, 9)
                            str1 = f"{x1} * {x2}"
                            y=x1*x2
                            if y<100:
                                break
                    else:
                        while True:
                            x1 = random.randint(11, 99)
                            x2 = random.randint(2, 9)
                            str1 = f"{x1*x2} ÷ {x2}"
                            y=x1
                            if x1*x2<100:
                                break
                else:
                    x1 = random.randint(11, 99)
                    x2 = random.randint(11, 99)
                    if t2 == 1: # 加
                        while x1+x2>99:
                            x1 = random.randint(11, 99)
                            x2 = random.randint(11, 99)
                        str1 = f"{x1} + {x2}"
                        y=x1+x2
                    else:
                        if x1>x2:
                            str1 = f"{x1} - {x2}"
                            y=x1-x2
                        else:
                            str1 = f"{x2} - {x1}"
                            y=x2-x1
                str1 = "("+str1+")"
                if t1==1: #先加减
                    if t3 == 1 : #加
                        x1 = random.randint(11, 99)
                        str = f"{x1} + {str1}"
                    else:
                        x1 = random.randint(y,99)
                        str = f"{x1} - {str1}"
                else:
                    if (t3 == 1) or (y>9): #乘
                        if y>9:
                            x1 = random.randint(2, 9)
                        else:
                            x1 = random.randint(11,99)
                        str = f"{x1} * {str1}"
                    else:
                        x1 = random.randint(11,99)
                        str = f"{x1} ÷ {str1}"
            else: #无括号
                if t2 == 1:  # 乘
                    while True:
                        x1 = random.randint(11, 99)
                        x2 = random.randint(2, 9)
                        str1 = f"{x1} * {x2}"
                        y = x1 * x2
                        if y < 100:
                            break
                else:
                    while True:
                        x1 = random.randint(11, 99)
                        x2 = random.randint(2, 9)
                        str1 = f"{x1 * x2} ÷ {x2}"
                        y = x1
                        if x1 * x2 < 100:
                            break
                if t1 == 1: #先乘除
                    if t3 == 1 : #加
                        x1 = random.randint(11, 99)
                        str = f"{str1} + {x1}"
                    else:
                        x1 = random.randint(0,y)
                        str = f"{str1} - {x1}"
                else:
                    if t3 == 1 : #加
                        x1 = random.randint(11, 99)
                        str = f"{x1} + {str1}"
                    else:
                        x1 = random.randint(y,99)
                        str = f"{x1} - {str1}"
            str = str + "="
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
