"""
取出数据库数据写入excel 48000条/表
"""

import xlwt
import datetime
import pymysql
import re
import os
from openpyxl import Workbook

#数据库查询全部邮箱
def selectFromDb():
    global selectDbTable
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = db.cursor()
    try:
        sql = "SELECT EMAIL FROM" + selectDbTable
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        db.close()
        return results
    except Exception as err:
        print('读取数据库出错',err)

#email地址过滤
def getEmails(arg):
    #将每个数据作为字符串,findall邮箱
    regex = "[a-zA-Z0-9][a-zA-Z0-9.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+"
    email = re.findall(regex,str(arg),re.IGNORECASE)  #返回值为 list
    # while '' in email:
    #     email.remove('')
    return email[0]

#写入excel
def writeExcel(data,lines):#data可以不需要而直接写入excel提升效率?
    print("写ru数据表被执行",data)
    global writeCount,savePath
    excelNameCount =  fileCount(savePath) - 1#获取存储文件夹文件数
    print('获取到文件数',excelNameCount)
    # 48000行数据换一张表
    x = 0
    wb = Workbook()
    sheet = wb.active
    sheet.title = "sheet1"
    for i in range(data.__len__()):
        sheet["A%d" % (x + 1)].value = data[i]
        x += 1
        if (i-1) % lines == 0 and i != 0:
            writeCount += 1
            wb.save(savePath + str(excelNameCount) + '.xlsx')
            excelNameCount += 1
            x = 0

# 获取写入目标文件夹的文件数,用于计数命名
def fileCount(savePath):
    for parent, dirnames, filenames in os.walk(savePath):
        # print('文件数..................', filenames.__len__())
        # 获取当前文件夹写文件数,继续数目新增命名.xls文件
        fileCount = filenames.__len__()
    return fileCount

if __name__ == "__main__":
    writeCount = 0
    starttime = datetime.datetime.now()
    #每表数据条数
    lines = 100
    #查表名
    selectDbTable = " EMAILTEST"
    #存储路径
    savePath = "E:/"
    # 清洗结果
    results = []
    #获取邮件地址
    datas = selectFromDb()
    for email in datas:
        try:
            temp = getEmails(email[0])
            if temp:
                results.append(getEmails(email[0]))
        except:
            print('空数据')
    #写入excel
    writeExcel(results,lines)
    endtime = datetime.datetime.now()
    print('运行时间:', endtime - starttime)