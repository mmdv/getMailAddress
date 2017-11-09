"""
第四个版本
遍历源路径读取写入数据库,按列匹配邮箱地址
非读取错误文件和特殊形式获取全部邮箱地址
executemany()N倍速度于单行单数据插入mysql
"""

import os
import xlrd
import re
import datetime
import pymysql
import csv

#遍历源路径,获取全部文件路径名
def getFullFileNames(sourcePath):
    # print(sourcePath,regex)
    fullFileNames = []
    for parent, dirnames, filenames in os.walk(sourcePath):
        # print('源文件总数',filenames.__len__())
        for filename in filenames:
            # 匹配.xls/.xlsx
            fullFileNames.append(os.path.join(parent, filename))
    return fullFileNames

#匹配xls,xlsx/csv,对应获取相应数据,写入数据库
def execute(regexXls,regexCsv,fullFileName):

    datas = []

    #匹配到xls/xlsx
    if re.match(regexXls, fullFileName, re.IGNORECASE):
        datas = getEmailFromXls(fullFileName)  # 函数名做参数
    # 匹配csv
    elif re.match(regexCsv, fullFileName, re.IGNORECASE):
        # print('匹配到csv')
        datas = getEmailFromCsv(fullFileName)
    if not datas:
        # 写入数据库
        insertDb(datas)
        return
    return

#获取xls/xlsx数据
def getEmailFromXls(xlsFile):

    try:
        dataCurrentExcel = []
        # 获取当前excel
        excelCurrent = xlrd.open_workbook(xlsFile)
        # 获取当前excel表所有sheet
        all_sheets_list = excelCurrent.sheet_names()
        # print('所有sheet名',all_sheets_list)
        for x in all_sheets_list:
            # print('当前sheet:', x)
            sheetCurrent = excelCurrent.sheet_by_name(x)
            # print(sheetCurrent.row_values(0))
            if sheetCurrent.nrows != 0 and sheetCurrent.ncols != 0:
                for i in range(sheetCurrent.ncols):
                    #按列提取邮箱
                    dataCurrentExcel.extend(getEmails(sheetCurrent.col_values(i)))
        return set(dataCurrentExcel)  # set去重
    except Exception as err:

        f = open(savePath + "errLog2.txt", "a")
        f.write(xlsFile)
        f.write("\n")
        f.close()

#获取csv数据
def getEmailFromCsv(csvFile):
    try:
        dataCurrentExcel = []
        with open(csvFile, "r") as csvFile:
            # 读取csv文件，返回的是迭代类型
            reader = csv.reader(csvFile)
            data = [row for row in reader]  # 现存数据
            for i in data:
                dataCurrentExcel.extend(getEmails(i))
        return set(dataCurrentExcel)
    except Exception as err:
        #     记录读取错误文件
        f = open(savePath + "errLog2.txt", "a")
        f.write(csvFile)
        f.write("\n")
        f.close()

#提取邮箱
def getEmails(arg):
    emailList = []
    #将每个数据作为字符串,findall邮箱
    for cell in arg:
        regex = r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)'
        result = re.findall(regex,str(cell),re.IGNORECASE)
        for i in range(result.__len__()):
            emailList.append(result[i][0])
    return (emailList)

#写入数据库
def insertDb(data):
    global insertCount,dbTable
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset="utf8")
    cursor = db.cursor()
    insertCount += 1
    print('data',data.__len__())
    try:
        # sql = "INSERT IGNORE INTO EMAILFROMSIMON (EMAIL) VALUES ( %s )"
        sql = "INSERT IGNORE INTO " + dbTable + " (EMAIL) VALUES ( %s )"
        cursor.executemany(sql,tuple(data))
        # 提交到数据库执行
        db.commit()
    except Exception as  err:
        print('写入错误',err)
    #关闭数据库
    db.close()

if __name__ == "__main__":
    dbTable = "EMAILFROMSIMON2"
    starttime = datetime.datetime.now()
    #打开数据库
    insertCount = 0
    sourcePath = 'E:/pppsource'
    savePath = 'E:/pppresult/'
    regexXls = '(.)+\.(xls|xlsx)$'
    regexCsv = '.+\.csv$'
    # 获取源路径文件名
    fullFileNames = getFullFileNames(sourcePath)
    #遍历文件获取数据
    for fileName in fullFileNames:
        execute(regexXls,regexCsv,fileName)
    print('写入次数', insertCount)
    endtime = datetime.datetime.now()
    print('运行时间:',endtime - starttime)