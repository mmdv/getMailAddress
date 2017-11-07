import os
import xlrd
import re
import datetime
import pymysql

#遍历源数据路径
def getAllExcelNames(regex,sourcePath,savePath):
    # print(sourcePath,regex)
    for parent, dirnames, filenames in os.walk(sourcePath):
        # print('源文件总数',filenames.__len__())
        for filename in filenames:
            if re.match(regex, filename, re.IGNORECASE):
                excelPathName = os.path.join(parent,filename)#当前文件路径及文件名
                # try:
                data = getDataFromExcel(excelPathName)
                    # 写入数据库
                opearDb(list(data), excelPathName)
                # except Exception as err:
                #     print('文件读取出错',err)
                    #记录错误信息
                    # f = open(savePath + "errLog.txt","a")
                    # f.write( excelPathName )
                    # f.write("\n")
                    # f.close()
#获取数据
def getDataFromExcel(excelPathName):
    # 读取文件
    dataCurrentExcel = []
    # print('当前文件路径名:', excelPathName)
    excelCurrent = xlrd.open_workbook(excelPathName)
    # 获取当前excel表所有sheet
    all_sheets_list = excelCurrent.sheet_names()
    # print('所有sheet名',all_sheets_list)
    for x in all_sheets_list:
        # print('当前sheet:', x)
        sheetCurrent = excelCurrent.sheet_by_name(x)
        # 判断当前sheet第一行是否含有mail字样
        # print(sheetCurrent.row_values(0))
        if sheetCurrent.nrows != 0 and sheetCurrent.ncols != 0:
            flag = False
            if sheetCurrent.nrows > 10:
                rows = 10
            else:
                rows = sheetCurrent.nrows
            for col in range(rows):
                i = 0
                for colCell in sheetCurrent.row_values(col):  # 遍历当前sheet第一行
                # print('当前表',x,'的第一行',colCell)
                    if re.match("(.*)email(.*)|(.*)邮箱(.*)|(.*)e(.*)mail(.*)", str(colCell), re.IGNORECASE):  # 如果列表第一行存在email字段栏
                        # print('首行匹配到邮箱地址',i)
                        temp = sheetCurrent.col_values(i)
                        # print('temp', temp)
                        temp = getAllEmail(temp)
                        dataCurrentExcel.extend(temp)
                        flag = True
                        break
                    i += 1
                if flag:
                    break
            if not flag:  # 第一行不存在mail字样,打印全部数据过滤出邮箱
                emailList = checkThreeRows(sheetCurrent)
                if emailList:
                    dataCurrentExcel.extend(emailList)
    return set(dataCurrentExcel)#set去重

# 检测不到email字样,输出前三行,匹配地址邮箱
def checkThreeRows(sheetCurrent):
    regex = "^(')?[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+(')?.*$"
    temp = []
    sheetHasMail = False
    if sheetCurrent.nrows > 3:
        count = 3
    else:
        count = sheetCurrent.nrows
    for i in range(count):
        flag = -1
        for x in sheetCurrent.row_values(i):
            flag +=1#记录出现邮箱列
            if re.match(regex,str(x)):
                sheetHasMail = True
                break
    if sheetHasMail:
        temp = getAllEmail(sheetCurrent.col_values(flag))
        return temp
    else:
        return False

#提取数据中邮箱地址
def getAllEmail(arg):
    while '' in arg:  # 去除列表为空地址
        arg.remove('')
    while re.match("(.*)email(.*)|(.*)邮箱(.*)|(.*)e(.*)mail(.*)", arg[0], re.IGNORECASE):
        arg = arg[1:arg.__len__()]  # 去除第一行email字段
    addressList = []
    for i in arg:
        string = i
        regex = r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)'
        result = re.findall(regex,str(string),re.IGNORECASE)
        for i in range(result.__len__()):
            addressList.append(result[i][0])
    return (addressList)

#连接数据库
def opearDb(data,filename):
    global writeCount,db,cursor
    writeCount += 1
    print('data',data.__len__())
    for i in data:
        sql = "insert ignore into email (email,filename) values ('{0}','{1}')".format(str(i), str(filename))
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
# 获取写入目标文件夹的文件数,用于计数命名
def fileCount(savePath):
    for parent, dirnames, filenames in os.walk(savePath):
        # print('文件数..................', filenames.__len__())
        excelNameCount = filenames.__len__()  # 获取当前文件夹写文件数,继续数目新增命名.xls文件
    return excelNameCount

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    #打开数据库
    # db = pymysql.connect("localhost", "root", "", "db3") #加不了编码
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='db3', charset="utf8")
    cursor = db.cursor()
    writeCount = 0
    #遍历全部文件
    getAllExcelNames('(.)+\.(xls|xlsx)$',"E:/testExcelData",r"E:/excelAddressAll/")#正则表达式,数据源路径,错误文件存储路径
    #关闭数据库
    db.close()
    print('写入表数', writeCount)
    endtime = datetime.datetime.now()
    print('邮件列表获取完成,运行时间:',endtime - starttime)