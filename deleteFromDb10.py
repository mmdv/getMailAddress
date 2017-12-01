"""
读取列表公司邮箱后缀
数据库删除对应邮箱
删除前先存储到其他数据库
"""

import os
import xlrd
import re
import datetime
import pymysql
import csv

# 读取待删除公司邮箱后缀
#遍历数据源路径文件名
def getAllFileNames(sourcePath):
    # print(sourcePath)
    excelPathName = []
    for parent, dirnames, filenames in os.walk(sourcePath):
        print('源文件总数',filenames.__len__())
        for filename in filenames:
            excelPathName.append(os.path.join(parent, filename))
    return excelPathName
#获取文件邮箱数据
def getDomainFromFile(excelPathName):
    dataCurrent = []
    for i in excelPathName:
        for line in open(i):
            res = re.findall(r'(@?[0-9a-z]+(.[0-9a-z]+)+)', line)
            if not re.match('@', res[0][0]):
                email = '@' + res[0][0]
                dataCurrent.append(email)
            else:
                email = res[0][0]
                dataCurrent.append(email)
    return dataCurrent

#数据库查询全部邮箱
def selectFromDb(likeText):
    global opera_dbname
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = db.cursor()
    try:
        sql = "SELECT EMAIL FROM" + opera_dbname + " WHERE EMAIL LIKE  '%{0}%'".format(likeText)
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        db.close()
        return results
    except Exception as err:
        print('读取数据库出错',err)

def insertDb(data):
    global insertDbTable
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = db.cursor()
    try:
        sql = "INSERT IGNORE INTO " + insertDbTable + " (EMAIL) VALUES ( %s )"
        cursor.executemany(sql, tuple(data))
        # 提交到数据库执行
        db.commit()
    except Exception as  err:
        print('写入错误', err)
    # 关闭数据库
    db.close()

#数据库删除数据
def delDb(company_domain):
    global opera_dbname
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset='utf8')
    cursor = db.cursor()
    # print('data',data.__len__())
    try:
        sql = "DELETE FROM  " + opera_dbname + " WHERE EMAIL like '%{0}%' ".format(company_domain)
        # print(sql)
        cursor.execute(sql)
        db.commit()
    except Exception as  err:
        print('删除错误',err)
    #关闭数据库
    db.close()

if __name__ == "__main__":
    #待删除数据的表名
    opera_dbname = " emailfromsimon"
    #插入删除数据表
    insertDbTable = " m11d8unsubscribe "
    # dbTable = " EMAILM11D8"
    starttime = datetime.datetime.now()
    sourcePath = 'E:/pppwork/companylist/'
    # sourcePath = 'E:/pppsource/'
    #源文件名list
    file_list = getAllFileNames(sourcePath)
    # print(file_list)
    #公司邮箱后缀
    company_list = getDomainFromFile(file_list)
    # print(company_list,'-----------')
    for i in company_list:
        # print(i)
        #查询数据库
        email_list = selectFromDb(i)

        if email_list:
            # 删除前存入新库
            insertDb(email_list)
            for email in email_list:
                print(email[0])
                #删除数据库
                delDb(email[0])


    #存错误信息文件
    savePath = 'E:/pppresult/'
    endtime = datetime.datetime.now()
    print('运行时间:',endtime - starttime)