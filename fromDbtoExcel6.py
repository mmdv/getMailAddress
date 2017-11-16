"""
取出数据库数据写入excel 48000条/表
很慢,很慢,很慢
"""

import xlwt
import datetime
import pymysql
import re
import os

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
    email = re.findall(regex,str(arg),re.IGNORECASE)
    return email

#写入excel
def writeExcel(data,lines):#data可以不需要而直接写入excel提升效率?
    # print("写ru数据表被执行")
    global writeCount,savaPath
    excelNameCount =  fileCount(savePath) - 1#获取存储文件夹文件数
    # print('获取到文件数',excelNameCount)
    # 48000行数据换一张表
    x = 0#数据列计数
    for i in range(data.__len__()):
        if i % lines == 0:
            writeCount += 1
            x = 0
            new_workbook = xlwt.Workbook()
            new_sheet = new_workbook.add_sheet("sheet1")
            excelNameCount += 1
        new_sheet.write(x, 0, list(data)[i])
        new_workbook.save(savePath + str(excelNameCount) + ".xls")
        x += 1

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
    lines = 48000
    #查表名
    selectDbTable = "  EMAILM11D8"
    #存储路径
    savePath = "E:/pppresult/"
    # 清洗结果
    results = []
    #获取邮件地址
    datas = selectFromDb()
    for email in datas:
        temp = getEmails(email[0])
        if temp:
            results.append(getEmails(email[0]))
    #写入excel
    writeExcel(results,lines)
    endtime = datetime.datetime.now()
    print('运行时间:', endtime - starttime)