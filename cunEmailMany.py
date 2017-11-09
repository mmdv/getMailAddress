"""读取标准单列整理过邮箱列表写入数据库"""

import os
import pymysql
import xlrd
import xlwt
import datetime

#遍历数据源路径文件名
def getAllExcelNames(sourcePath):
    # print(sourcePath,regex)
    excelPathName = []
    for parent, dirnames, filenames in os.walk(sourcePath):
        print('源文件总数',filenames.__len__())
        for filename in filenames:
            excelPathName.append(os.path.join(parent, filename))
    return excelPathName
#获取文件邮箱数据
def getEmailFromExcel(excelPathName):
    # 读取文件
    global savaPath
    dataCurrentExcel = []
    print('当前文件路径名:', excelPathName)
    try:
        excelCurrent = xlrd.open_workbook(excelPathName)
        # 获取当前excel表所有sheet
        all_sheets_list = excelCurrent.sheet_names()
        # print('所有sheet名',all_sheets_list)
        for x in all_sheets_list:
            # print('当前sheet:', x)
            sheetCurrent = excelCurrent.sheet_by_name(x)
            # print(sheetCurrent.row_values(0))
            dataCurrentExcel.extend(sheetCurrent.col_values(0))
        dataCurrentExcel = list(set(dataCurrentExcel))  # set去重
    except Exception as err:
        print('文件读取出错', err)
            #     记录错误信息
        f = open(savaPath + "simonResultErrLog.txt", "a")
        f.write(excelPathName)
        f.write("\n")
        f.close()

    return dataCurrentExcel
#写入数据库db3,emailonly表
def insertDb(data):
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset="utf8")
    cursor = db.cursor()
    """效率很低
    sql = "insert ignore into EMAILFROMSIMON (email) values ('{0}')".format(str(i))
    cursor.execute(sql)"""
    try:
        sql = "INSERT IGNORE INTO EMAILFROMSIMON (EMAIL) VALUES ( %s )"
        cursor.executemany(sql,tuple(data))
        # 提交到数据库执行
        db.commit()
    except Exception as  err:
        print('写入错误',err)
    db.close()
#查询数据库
def selectDb():
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset="utf8")
    cursor = db.cursor()
    try:
        sql = "SELECT EMAIL FROM EMAILFROMSIMON"
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print('读出数据',results)
    except Exception as err:
        print('读取数据库出错',err)
    return results
# 查询存储路径文件数
def fileCount(savePath):
    for parent, dirnames, filenames in os.walk(savePath):
        # print('文件数..................', filenames.__len__())
        excelNameCount = filenames.__len__()  # 获取当前文件夹写文件数,继续数目新增命名.xls文件
    return excelNameCount

#写入excel,48000一份
def writeExcel(data,savePath):
        # 30000行数据换一张表
    fileCou = fileCount(savePath) - 1
    x = 0#数据列计数
    for i in range(data.__len__()):
        if i % 48000 == 0:
            x = 0
            fileCou += 1
            new_workbook = xlwt.Workbook()
            new_sheet = new_workbook.add_sheet("sheet1")
        new_sheet.write(x, 0, data[i])
        new_workbook.save(savePath + str(fileCou) + ".xls")
        x += 1

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    sourcePath = "E:/py48src/"
    savaPath = "E:/py48res/"
    # 获取源文件路径名称
    allFile = getAllExcelNames(sourcePath)
    # 根据路径名获取每个表邮箱
    for oneFile in allFile:
        data = getEmailFromExcel(oneFile)
        #写入数据库/去重/存储
        insertDb(data)
    #提取邮件/48000一份excel
    # res = selectDb()
    #写入excel
    # writeExcel(res,savaPath)
    endtime = datetime.datetime.now()
    print('邮件列表获取完成,运行时间:', endtime - starttime)