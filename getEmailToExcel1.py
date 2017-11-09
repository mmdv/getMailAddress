"""
第一个版本
遍历源路径,匹配3行mail字样,10行邮件地址,写入excel(10行外被遗漏,写入excel效率低)
"""

import os
import xlrd
import re
import xlwt
import datetime
import csv

dataPrevious = {'dataP':[],'dataN':[],'excelFile':[]}

#遍历源数据路径
def getAllExcelNames(regexXls,regexCsv,sourcePath):
    # print(sourcePath,regex)
    for parent, dirnames, filenames in os.walk(sourcePath):
        print('源文件总数',filenames.__len__())
        for filename in filenames:
            #匹配.xls/.xlsx
            if re.match(regexXls, filename, re.IGNORECASE):
                execute(parent,filename,getEmailFromExcel)#函数名做参数
            #匹配csv
            if re.match(regexCsv,filename,re.IGNORECASE):
                # print('匹配到csv')
                execute(parent,filename,getEmailFromCsv)

#匹配.xls/xlsx/csv后执行函数
def execute(parent,filename,fun):
    global dataPrevious
    excelPathName = os.path.join(parent, filename)  # 当前文件路径及文件名
    print('匹配到',excelPathName)
    try:
        dataPrevious['dataN'] = fun(excelPathName)
        # print('dataN',dataPrevious['dataN'])
    except Exception as err:
        print('文件读取出错', err)
        #     记录错误信息
        f = open(savePath + "errLog.txt", "a")
        f.write(excelPathName)
        f.write("\n")
        f.close()

    # 比较数据是否重复
    # print('dataP',dataPrevious['dataP'])
    flag = [i for i in dataPrevious['dataN'] if i in dataPrevious['dataP']]  # 交集
    # 或者 flag = set(dataPrevious['dataN']) & set(dataPrevious['dataP'])
    if flag.__len__() > 0:
        # 利用set,减去交集
        dataPrevious['dataN'] = dataPrevious['dataN'] - set(flag)  # 减去交集
    # 写入表格操作
    writeExcel(dataPrevious['dataN'], excelPathName, savePath)
    dataPrevious['excelFile'] = excelPathName  # 存储当前excel名称
    dataPrevious['dataP'] = dataPrevious['dataN']  # 后读取数据前存

#获取数据,返回示例:oneExcelData[[sheet1],[sheet2],,,],返回set
def getEmailFromExcel(excelPathName):
    # 读取文件
    dataCurrentExcel = []
    print('当前文件路径名:', excelPathName)
    excelCurrent = xlrd.open_workbook(excelPathName)
    # 获取当前excel表所有sheet
    all_sheets_list = excelCurrent.sheet_names()
    # print('所有sheet名',all_sheets_list)
    for x in all_sheets_list:
        # print('当前sheet:', x)
        sheetCurrent = excelCurrent.sheet_by_name(x)
        # 判断当前sheet第一行是否含有mail字样
        # print(sheetCurrent.row_values(0))
        if sheetCurrent.nrows != 0 and sheetCurrent.ncols != 0:
            flag = False
            if sheetCurrent.nrows > 10:
                rows = 10
            else:
                rows = sheetCurrent.nrows
            for col in range(rows):
                i = 0
                for colCell in sheetCurrent.row_values(col):  # 遍历当前sheet第一行
                # print('当前表',x,'的第一行',colCell)
                    if re.match('.*(mail|邮箱|邮件).*', str(colCell), re.IGNORECASE):  # 如果列表第一行存在email字段栏
                        # print('首行匹配到邮箱地址',i)
                        temp = sheetCurrent.col_values(i)
                        # print('temp', temp)
                        temp = getAllEmail(temp)
                        dataCurrentExcel.extend(temp)
                        flag = True
                        break
                    i += 1
                if flag:
                    break
            if not flag:  # 第一行不存在mail字样,打印全部数据过滤出邮箱
                emailList = checkThreeRows(sheetCurrent)
                if emailList:
                    dataCurrentExcel.extend(emailList)
    return set(dataCurrentExcel)#set去重

# 检测不到email字样,输出前三行,匹配地址邮箱
def checkThreeRows(sheetCurrent):
    regex = "^(')?[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+(')?.*$"
    temp = []
    sheetHasMail = False
    if sheetCurrent.nrows > 3:
        count = 3
    else:
        count = sheetCurrent.nrows
    for i in range(count):
        flag = -1
        for x in sheetCurrent.row_values(i):
            flag +=1#记录出现邮箱列
            if re.match(regex,str(x)):
                sheetHasMail = True
                break
    if sheetHasMail:
        temp = getAllEmail(sheetCurrent.col_values(flag))
        return temp
    else:
        return False

#获取csv文件邮箱
def getEmailFromCsv(csvfile):
    with open(csvfile, "r") as csvfile:
        # 读取csv文件，返回的是迭代类型
        row = 0  # 前十行寻找
        reader = csv.reader(csvfile)
        data = [row for row in reader]  # 现存数据
        columns = []
        for i in data:
            flag = False
            col = -1
            row += 1
            for key in i:
                col += 1
                if re.match('.*(mail|邮箱|邮件).*', key, re.IGNORECASE):
                    flag = True
                    columns.extend(getAllEmail([r[col] for r in data]))
                elif re.match("^(')?[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+(')?.*$", key, re.IGNORECASE):
                    flag = True
                    columns.extend(getAllEmail([r[col] for r in data]))
            if row == 10 or (col == (i.__len__() - 1) and flag):
                break
    return set(columns)

#提取数据中邮箱地址
def getAllEmail(arg):
    while '' in arg:  # 去除列表为空地址
        arg.remove('')
    while re.match("(.*)email(.*)|.*(邮箱|邮件).*|(.*)e(.*)mail(.*)", arg[0], re.IGNORECASE):
        arg = arg[1:arg.__len__()]  # 去除第一行email字段
    addressList = []
    for i in arg:
        string = i
        regex = r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)'
        result = re.findall(regex,str(string),re.IGNORECASE)
        for i in range(result.__len__()):
            addressList.append(result[i][0])
    return (addressList)

#写入excel
def writeExcel(data,currentExcelName,savePath):#data可以不需要而直接写入excel提升效率?
    # print("写ru数据表被执行")
    global writeCount
    excelNameCount =  fileCount(savePath) - 1#获取存储文件夹文件数
    # print('获取到文件数',excelNameCount)
        # 30000行数据换一张表
    x = 0#数据列计数
    for i in range(data.__len__()):
        if i % 30000 == 0:
            writeCount += 1
            x = 0
            new_workbook = xlwt.Workbook()
            new_sheet = new_workbook.add_sheet("sheet1")
            sheet2 = new_workbook.add_sheet("sheet2")
            sheet2.write(0,0,currentExcelName)
            excelNameCount += 1
        new_sheet.write(x, 0, list(data)[i])
        new_workbook.save(savePath + str(excelNameCount) + ".xls")
        x += 1

# 获取写入目标文件夹的文件数,用于计数命名
def fileCount(savePath):
    for parent, dirnames, filenames in os.walk(savePath):
        # print('文件数..................', filenames.__len__())
        excelNameCount = filenames.__len__()  # 获取当前文件夹写文件数,继续数目新增命名.xls文件
    return excelNameCount

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    writeCount = 0
    sourcePath = 'E:/pppsource'
    savePath ='E:/pppresult/'
    regexXls = '(.)+\.(xls|xlsx)$'
    regexCsv = '.+\.csv$'
    #遍历全部文件
    getAllExcelNames(regexXls,regexCsv,sourcePath)#正则表达式,数据源路径,目标路径
    endtime = datetime.datetime.now()
    print('邮件列表获取完成,运行时间:',endtime - starttime)
    print('写入表数', writeCount)