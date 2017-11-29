"""
从excel读取数据,删除对应库中数据
"""

import os
import xlrd
import re
import datetime
import pymysql
import csv

#遍历源路径,获取全部文件路径名
def execute(regexXls,regexCsv,sourcePath):
    for parent, dirnames, filenames in os.walk(sourcePath):
        # print('源文件总数',filenames.__len__())
        for filename in filenames:
            data = []
            fullFileName = os.path.join(parent, filename)
            # 匹配xls/xlsx
            if re.match(regexXls, fullFileName, re.IGNORECASE):
                data = getEmailFromXls(fullFileName)
                print('当前执行文件', fullFileName)
            # 匹配csv
            elif re.match(regexCsv, fullFileName, re.IGNORECASE):
                print('当前文件', fullFileName)
                data = getEmailFromCsv(fullFileName)
            if data:
                    # 删除对应数据
                    delDb(data)

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
        f.write(str(xlsFile))
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
        f.write(str(csvFile))
        f.write("\n")
        f.close()

#提取邮箱
def getEmails(arg):
    emailList = []
    #将每个数据作为字符串,findall邮箱
    for cell in arg:
        regex = '([a-zA-Z0-9][a-zA-Z0-9.\-\_+]+@([a-zA-Z0-9]+[\-_\.+]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3})'  # 匹配完全
        result = re.findall(regex,str(cell),re.IGNORECASE)
        for i in  result:
            emailList.append(i[0])
    return (emailList)


#数据库删除数据
def delDb(data):
    global dbTable
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = db.cursor()
    # print('data',data.__len__())
    try:
        for i in data:
            print(i)
            # sql = "DELETE FROM " + dbTable + " WHERE EMAIL = '{}'".format('zhaozhh@cgnpc.com.cn')
            sql = 'DELETE FROM  EMAILTEST WHERE EMAIL = "{0}" '.format(i)
            # sql = "select * from " + dbTable + " where email = '{}'".format('zhaozhh@cgnpc.com.cn')
            # print(sql)
            cursor.execute(sql)
            db.commit()
    except Exception as  err:
        print('删除错误',err)
    #关闭数据库
    db.close()

if __name__ == "__main__":
    #待删除数据的表名
    # dbTable = " EMAILTEST"
    dbTable = " EMAILM11D8"
    starttime = datetime.datetime.now()
    sourcePath = 'E:/pppwork/'
    # sourcePath = 'E:/pppsource/'
    #存错误信息文件
    savePath = 'E:/pppresult/'
    regexXls = '(.)+\.(xls|xlsx)$'
    regexCsv = '.+\.csv$'
    # 执行函数
    execute(regexXls, regexCsv, sourcePath)
    endtime = datetime.datetime.now()
    print('运行时间:',endtime - starttime)