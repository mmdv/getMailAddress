"""
读取数据库,删除对应另库中数据
"""

import os
import xlrd
import re
import datetime
import pymysql
import csv
#数据库查询全部邮箱
def selectFromDb():
    global selectDbTable
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = db.cursor()
    try:
        sql = "SELECT EMAIL FROM " + selectDbTable
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        db.close()
        return results
    except Exception as err:
        print('读取数据库出错',err)

#数据库删除数据
def delDb(data):
    global dbTable
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = db.cursor()
    # print('data',data.__len__())
    try:
        for i in data:
            sql = "DELETE FROM  " + dbTable + "  WHERE EMAIL = '{}'".format(i[0])
            cursor.execute(sql)
            db.commit()
    except Exception as  err:
        print('删除错误',err)
    #关闭数据库
    db.close()

if __name__ == "__main__":
    #待删除数据的表名
    # dbTable = " EMAILTEST"
    selectDbTable = "m11d8unsubscribe"
    dbTable = " EMAILM11D8"
    starttime = datetime.datetime.now()
    #存错误信息文件
    savePath = 'E:/pppresult/'
    # 执行函数
    data = selectFromDb()
    delDb(data)
    endtime = datetime.datetime.now()
    print('运行时间:',endtime - starttime)