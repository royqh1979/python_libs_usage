#生成一百以内带退位减法 带进位加法

import win32com.client
import random


app = win32com.client.DispatchEx('Excel.Application')
excel_constants = win32com.client.constants

template_file = "g:/口算作业模板.xlsx"
out_dir = "g:\\"
out_name = out_dir+"口算"

max_number = 100
ratio_sub = 0.1 #减法题的比例
ratio_add = 0.1 #加法题的比例
ratio_mul = 0.1 #乘法题的比例

ratio_carry = 0.8 # 进退位比例
total_page = 30 # 总页数
seciton_per_page = 2 #每页的小节数
row_per_section = 10 #每页的行数
col_per_section = 3 #每页的列数
row_starts=[2, 16]

total_add_with_carry = 0 #带进位加法题目数
total_add_with_no_carry=0 #不带进位加法题目数
total_sub_decomposition = 0 #带退位减法题目数
total_sub_no_decomposition=0 #不带退位减法题目数
total_mul = 0 # 乘法题比例
total_div = 0 # 除法题比例

workbook = app.Workbooks.Open(template_file)
# print(workbook.ActiveSheet.Cells(1,1).Value())

random.seed()
for page in range(total_page):
    for j in range(seciton_per_page):
        row_start = row_starts[j]
        for i in range(row_per_section*col_per_section):
            type_ratio=random.random()
            carry_or_not_ratio=random.random()
            row = i%row_per_section+1
            col = i//row_per_section+1
            if type_ratio<ratio_sub:
                # 生成减法
                while True:
                    x = random.randint(1, max_number)
                    y = random.randint(1, x)
                    if carry_or_not_ratio < ratio_carry:  # 需要退位
                        if (x % 10) < (y % 10):
                            total_sub_decomposition += 1
                            break
                    else:
                        if (x % 10) >= (y % 10):
                            total_sub_no_decomposition += 1
                            break
                str = f"{x} ― {y}"
            elif type_ratio < ratio_sub + ratio_add:
                # 生成加法
                while True:
                    x = random.randint(1,max_number-1)
                    y = random.randint(1,max_number-x)
                    if carry_or_not_ratio<ratio_carry: #需要进位
                        if (x%10)+(y%10) >= 10:
                            total_add_with_carry+=1
                            break
                    else:
                        if (x%10)+(y%10) < 10:
                            total_add_with_no_carry += 1
                            break
                str = f"{x} ＋ {y}"
            elif type_ratio < ratio_sub + ratio_add + ratio_mul:
                # 生成乘法
                x = random.randint(2,9)
                y = random.randint(2,9)
                str = f"{x} × {y}"
                total_mul += 1
            else:
                # 生成除法
                x1 = random.randint(2, 9)
                x2 = random.randint(2, 9)
                if random.random() < 0.1:
                    y = 0
                else:
                    y = random.randint(1, x2 - 1)

                str = f"{x1 * x2 + y} ÷ {x2}"
                total_div += 1
            str = f"{str:>8s} ="
            workbook.ActiveSheet.Cells(row + row_start, col).Value=str
    out_file = f"{out_name}{page+1:03d}.pdf"
    print(out_file)
    workbook.ActiveSheet.ExportAsFixedFormat(excel_constants.xlTypePDF,out_file,
                                             Quality = excel_constants.xlQualityStandard,
                                             IncludeDocProperties = True,
                                             IgnorePrintAreas=False,
                                             OpenAfterPublish=False)

workbook.Close(SaveChanges=False)
app.Quit()
print(f"加法题目数量：{total_add_with_carry} {total_add_with_no_carry} {total_add_with_carry + total_add_with_no_carry}")
print(f"减法题目数量：{total_sub_decomposition} {total_sub_no_decomposition} {total_sub_decomposition + total_sub_no_decomposition}")
print(f"乘法题目数量：{total_mul}")
print(f"除法题目数量：{total_div}")
