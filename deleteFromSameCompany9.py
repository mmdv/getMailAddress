"""
删除对应公司邮箱(like),删除前先存储
"""

import os
import xlrd
import re
import datetime
import pymysql
import csv

#数据库查询全部邮箱
def selectFromDb(likeText):
    global dbTable
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = db.cursor()
    try:
        sql = "SELECT EMAIL FROM" + dbTable + " WHERE EMAIL LIKE  '%{0}%'".format(likeText)
        print('sql',sql)
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print('result',results)
        db.close()
        # return results
        insertDb(results)
    except Exception as err:
        print('读取数据库出错',err)

def insertDb(data):
    global insertDbTable
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = db.cursor()
    try:
        sql = "INSERT IGNORE INTO " + insertDbTable + " (EMAIL) VALUES ( %s )"
        print(data,'-------------')
        cursor.executemany(sql, tuple(data))
        # 提交到数据库执行
        db.commit()
        print('写入执行')
    except Exception as  err:
        print('写入错误', err)
    # 关闭数据库
    db.close()

#数据库删除数据
def delDb(likeText):
    global dbTable
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = db.cursor()
    # print('data',data.__len__())
    try:
        sql = "DELETE FROM  " + dbTable + " WHERE EMAIL like '%{0}%' ".format(likeText)
        print(sql)
        # sql = 'DELETE FROM  EMAILTEST WHERE EMAIL like  %"{0}" % '.format(likeText)
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
    insertDbTable = " m11d8unsubscribe "
    # dbTable = " EMAILM11D8"
    starttime = datetime.datetime.now()
    sourcePath = 'E:/pppwork/'
    # sourcePath = 'E:/pppsource/'
    #存错误信息文件
    savePath = 'E:/pppresult/'
    # delDb('@cn.amorepacific.com')
    selectFromDb('@cn.amorepacific.com')
    delDb('@cn.amorepacific.com')
    # 执行函数
    endtime = datetime.datetime.now()
    print('运行时间:',endtime - starttime)