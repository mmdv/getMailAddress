# -*- coding:utf-8 -*-  
# 邮箱格式-正则表达式匹配  

import re

# 一次匹配多个邮箱  
str1 = "'aaf ssa@ss.net asdf  asdb@163.com.cn; asdf ss-a@ss.net asdf asdd.cba@163.com afdsaf'"
regex = "^(')?[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+(')?.*$"
reg_str1 = r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)'

# mod = re.compile(reg_str1)
#
# items = mod.findall(str1)
#
# for item in items:
#     print(item)

if re.match(regex,str1):
    print('1')
else:
    print('0')



    # 输出全部数据,匹配邮箱

    # first_sheet = TC_workbook.sheet_by_index(0)
    # print("First sheet Name:", first_sheet.name)
    # print("First sheet Rows:", first_sheet.nrows)
    # print("First sheet Cols:", first_sheet.ncols)
    #
    # second_sheet = TC_workbook.sheet_by_name(1)
    # print("Second sheet Rows:", second_sheet.nrows)
    # print("Second sheet Cols:", second_sheet.ncols)
    #
    # first_row = second_sheet.row_values(0)
    # print("First row:", first_row)
    # first_col = second_sheet.col_values(0)
    # print("First Column:", first_col)

    # cell/获取指定单元格
    # cell_value = first_sheet.cell(1, 0).value
    # print("The 1th method to get Cell value of row 2 & col 1:", cell_value)
    # cell_value2 = first_sheet.row(1)[0].value
    # print("The 2th method to get Cell value of row 2 & col 1:", cell_value2)
    # cell_value3 = first_sheet.col(0)[1].value
    # print("The 3th method to get Cell value of row 2 & col 1:", cell_value3)