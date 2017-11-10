"""
第5版本
从数据库读取邮件,对不符合规则邮箱清洗,写入另表
"""

import datetime
import pymysql
import re

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

#写入数据库
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
        print('写入错误',err)
    #关闭数据库
    db.close()

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    #查表名
    selectDbTable = " EMAILFROMSIMON"
    #写表名
    insertDbTable = " EMAILFROMSIMON2"
    # 清洗结果
    results = []
    #获取邮件地址
    datas = selectFromDb()
    for email in datas:
        temp = getEmails(email[0])
        if temp:
            results.append(getEmails(email[0]))
    #写入数据库
    insertDb(results)
    endtime = datetime.datetime.now()
    print('运行时间:', endtime - starttime)