"""
取出数据库数据写入excel方法2 48000条/表  OPENPYXL
写入前分页查询,
"""
import math
import datetime
import pymysql
import os
import openpyxl as xl
import pandas as pd

#分页数据库查询
def selectFromDb(lines,fun):
    global selectDbTable
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = db.cursor()
    # try:
    sql = "SELECT count(EMAIL) FROM" + selectDbTable
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    len = cursor.fetchone()
    print(len[0])
    print('len[0',math.ceil(len[0] / lines))
    for i in range(math.ceil(len[0] / lines)):
        results = []
        print(i*lines,(i+1)*lines)
        sql = "SELECT email FROM " + selectDbTable + " ORDER BY id asc LIMIT {},{}".format(i * lines,lines)
        cursor.execute(sql)
        data = cursor.fetchall()
        for key in data:
            results.extend(key)
        fun(results)
    db.close()
    # except Exception as err:
    #     print('读取数据库出错',err)

#写入excel/
def writeXlsx(data):#data可以不需要而直接写入excel提升效率?
    print("写ru数据表被执行",data. __len__())
    global writeCount,savePath
    writeCount += 1
    excelNameCount =  fileCount(savePath) + 1#获取存储文件夹文件数
    # print('获取到文件数',excelNameCount)

    wb = xl.Workbook()
    ws = wb.active
    ws.title = "sheet1"
    for i in range(data.__len__()):
        # 用 + 拼接不能使用
        ws["A%d" % (i + 1)].value = data[i]
    wb.save(savePath + str(excelNameCount) + '.xlsx')
# 获取写入目标文件夹的文件数,用于计数命名
def fileCount(savePath):
    for parent, dirnames, filenames in os.walk(savePath):
        # print('文件数..................', filenames.__len__())
        # 获取当前文件夹写文件数,继续数目新增命名.xls文件
        fileCount = filenames.__len__()
    return fileCount

def writeCsv(data):
    global writeCount, savePath
    writeCount += 1
    excelNameCount = fileCount(savePath) + 1  # 获取存储文件夹文件数
    dataframe = pd.DataFrame({'emailAddress': data})

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    # dataframe.to_csv("E:/test.csv",index=False,sep='')
    dataframe.to_csv(savePath + str(excelNameCount) + '.csv', index=False, mode='w')

if __name__ == "__main__":
    writeCount = 0
    starttime = datetime.datetime.now()
    #每表数据条数
    # lines = 2000
    lines = 48000
    #查表名
    # selectDbTable = " EMAILFROMSIMON"
    selectDbTable = " EMAILTEST"
    # selectDbTable = " EMAILM11D8"
    #存储路径
    # savePath = "E:/pppresult/email/"
    savePath = "E:/ppptest/"
    #执行
    selectFromDb(lines,writeCsv)
    endtime = datetime.datetime.now()
    print('运行时间:', endtime - starttime)