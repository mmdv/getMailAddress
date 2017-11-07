import datetime
import datetime
import re
import xlrd
import csv
# list1 = [1,2,3,4,8,8]
# list2 = [2,3,5,8,8]
# # list3 = [ i for i in set(list1) if i in set(list2) ]
# list1 = list1[1:list1.__len__()]
# print('list4',list1[0])
# print(set(list1) | set(list2))
# # print(list3)
#
# f = open("E:/hello.txt","w")
# for i in range(20):
#        f.write(str(i))
#        f.write("\n")
# f.close()
# regex = "(.*)email(.*)|(.*)邮箱(.*)|(.*)e(.*)mail(.*)"
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# for i in range(3):
#     flag = 0
#     for x in range(8):
#         flag +=1
#         if(x ==3):
#             break
# print(flag)
#
# r = False
# if not r :
#     print(999)
#
# data = []
# for i in range(30000):
#     data.append(i)
#
#     starttime = datetime.datetime.now()
#
# x = 29999
# for i in range(30000):
#     if x < data[i]:
#         print('kkkk')
#
# endtime = datetime.datetime.now()
# print(endtime-starttime)
# color = []
# if not color:
#     print('911')
#
# data = [1,2,3]
# print(data.__len__())
# datar = [[]for i in range(data.__len__())]
#
# for i in range(10):
#     datar[0].append(i)
# for i in range(7):
#     datar[1].append(i)
# datar.extend(datar[0])
#
# print(datar)
# # print(datar[1])
#
#
# lista = ['', '', '', '', '', '', '', '', '', '', '']
#
# for i in lista:
#     print('aa',i)
# if lista:
#     print('aaa')
#
#
# regex = '.+\.csv$'
# regex = '.+\.(csv|xls|xlsx)$'
# regex = '.*(mail|邮箱|邮件).*'
# if re.match(regex,'22.douc22.email.xlsx',re.IGNORECASE):
#     print('匹配')
# else:
#     print('nonono')

def getAllEmail(arg):
    while '' in arg:  # 去除列表为空地址
        arg.remove('')
    if arg.__len__() > 0:
        while re.match("(.*)email(.*)|(.*)(邮箱|邮件)(.*)|(.*)e(.*)mail(.*)", str(arg[0]), re.IGNORECASE):
            arg = arg[1:arg.__len__()]  # 去除第一行email字段
    addressList = []
    for i in arg:
        string = i
        regex = r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)'
        result = re.findall(regex,str(string),re.IGNORECASE)
        for i in range(result.__len__()):
            addressList.append(result[i][0])
    return (addressList)

with open("E:/pppsource\jj.repeat.csv", "r") as csvfile:
    # 读取csv文件，返回的是迭代类型
    row = 0 #前十行寻找
    reader = csv.reader(csvfile)
    data = [row for row in reader] #现存数据
    columns = []
    for i in data:
        flag = False
        col = -1
        row +=1
        for key in i:
            col += 1
            if re.match('.*(mail|邮箱|邮件).*',key,re.IGNORECASE):
                print('keyi')
                flag = True
                columns.extend(getAllEmail([r[col] for r in data]))
            elif re.match("^(')?[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+(')?.*$",key,re.IGNORECASE):
                print('也可以')
                flag = True
                columns.extend(getAllEmail([r[col] for r in data]))
        if row == 10 or (col == (i.__len__()-1) and flag):
            break
    print(columns)