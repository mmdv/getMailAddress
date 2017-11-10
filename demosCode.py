import re
import datetime
import pymysql

#1匹配邮件地址列
def regMatchEmail():
    regex = "^(')?[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+(')?.*$"
    str = "'lxie@photronics.com'; 'grace.y.gu@gsk.com'; 'selina.r.liu@gsk.com';"
    if re.match(regex,str,re.IGNORECASE):
        return("匹配")
    else:
        return("不匹配")

#2提取邮箱地址
def getAllEmail():
    str = "'lxie@photronics.com'; 'grace.y.gu@gsk.com'; 'selina.r.liu@gsk.com';"
    regex = r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)'
    result = re.findall(regex,str,re.IGNORECASE)
    addressList = []
    for i in range(result.__len__()):
        addressList.append(result[i][0])

    return(addressList)

#3遍历文件夹下文件
def getFileNames(root):
    import os
    import os.path

    # this folder is custom
    rootdir = "E:/pyworkspace"
    for parent, dirnames, filenames in os.walk(rootdir):
        # case 1:
        for dirname in dirnames:
            print("parent folder is:" + parent)
            print("dirname is:" + dirname)
        # case 2
        for filename in filenames:
            print('文件名:', filename)
            print("parent folder is:" + parent)
            print("filename with full path:" + os.path.join(parent, filename))


if __name__ == "__main__":
    print(regMatchEmail())
# 4计算运行时间差
# starttime = datetime.datetime.now()
# #long running
# endtime = datetime.datetime.now()
# print (endtime - starttime)


#5global用法
X = 100
def foo():
    global X
    print('foo() x = ', X)
    X = X + 5
    print('Changed in foo(), x = ', X)

def fun():
    global X
    print('fun() x = ', X)
    X = X + 1
    print('Changed in fun(), x = ', X)

if __name__ == '__main__':
    foo()
    fun()
    print('Result x = ', X)

#6判断两个列表是否有重复数据
#方法1,单独list有无重复数据均可
lista = [1,2,3,4]
listb = [2,8,0,9,1]
listc = [a for a in lista if a in listb]
if listc.__len__() > 0:
    print(listc)
#方法2:单独list无重复数据
set1 = set(lista)
set2 = set(listb)
data = set1 & set2   #&取列表交集,  | 取合集   无序
if data.__len__() > 0:
    print (data)

#7异常处理+写入文件
    # try:
    #     data = fun(excelPathName)
    #     # print('dataN',dataPrevious['dataN'])
    #     # 写数据库
    #     opearDb(data, excelPathName)
    # except Exception as err:
    #     print('文件读取出错', err)
    #     #     记录错误信息
    #     f = open(savePath + "errLog.txt", "a")
    #     f.write(excelPathName)
    #     f.write("\n")
    #     f.close()

#8操作数据库
def opreateDb():
    # db = pymysql.connect("localhost", "root", "", "db3") #加不了编码
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset="utf8")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "insert ignore into email (email,filename) values ('{0}','{1}')".format(str(i), '99')
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    # 如果发生错误则回滚
    db.commit()
    db.close()

#9获取csv文件邮箱数据
def getEmailFromCsv(csvfile):
    with open(csvfile, "r") as csvfile:
        # 读取csv文件，返回的是迭代类型
        row = 0  # 前十行寻找
        reader = csv.reader(csvfile)
        data = [row for row in reader]  # 现存数据
        columns = []
        for i in data:
            flag = False
            col = -1
            row += 1
            for key in i:
                col += 1
                if re.match('.*(mail|邮箱|邮件).*', key, re.IGNORECASE):
                    flag = True
                    columns.extend(getAllEmail([r[col] for r in data]))
                elif re.match("^(')?[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+(')?.*$", key, re.IGNORECASE):
                    flag = True
                    columns.extend(getAllEmail([r[col] for r in data]))
            if row == 10 or (col == (i.__len__() - 1) and flag):
                break
    return set(columns)

#10读取文件
def openFile():
    # 最方便的方法是一次性读取文件中的所有内容放到一个大字符串中：
    all_the_text = open('d:/text.txt').read()
    print(all_the_text)
    all_the_data = open('d:/data.txt', 'rb').read()
    print(all_the_data)
    # 更规范的方法
    file_object = open('d:/text.txt')
    try:
        all_the_text = file_object.read()
        print(all_the_text)
    finally:
        file_object.close()
        # 下面的方法每行后面有‘\n'
    file_object = open('d:/text.txt')
    try:
        all_the_text = file_object.readlines()
        print(all_the_text)
    finally:
        file_object.close()
        # 三句都可将末尾的'\n'去掉
    file_object = open('d:/text.txt')
    try:
        # all_the_text = file_object.read().splitlines()
        # all_the_text = file_object.read().split('\n')
        all_the_text = [L.rstrip('\n') for L in file_object]
        print(all_the_text)
    finally:
        file_object.close()
        # 逐行读
    file_object = open('d:/text.txt')
    try:
        for line in file_object:
            print(line, end='')
    finally:
        file_object.close()
        # 每次读取文件的一部分

    def read_file_by_chunks(file_name, chunk_size=100):
        file_object = open(file_name, 'rb')
        while True:
            chunk = file_object.read(chunk_size)
            if not chunk:
                break
            yield chunk
        file_object.close()

    for chunk in read_file_by_chunks('d:/data.txt', 4):
        print(chunk)

#11简单的pandas示例
import pandas as pd
def leaPandas():
    writer = pd.ExcelWriter('E:/output.xlsx')
    df = pd.DataFrame(data={'col1':[1,1], 'col2':[2,2]})
    df.to_excel(writer, sheet_name='sheet1')
    writer.save()
    print('\n\n写入excel成功~~')

#listwhile操作 去除空值
def fun12(arg):
    while '' in arg:  # 去除列表为空地址
        arg.remove('')
    while re.match("(.*)email(.*)|(.*)邮箱(.*)|(.*)e(.*)mail(.*)", arg[0], re.IGNORECASE):
        arg = arg[1:arg.__len__()]  # 去除第一行email字段