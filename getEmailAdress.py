import os
import xlrd
import re
import xlwt
import datetime

dataPrevious = {'dataP':[],'dataN':[]}
parity = 0
#遍历源数据路径
def getAllExcelNames(regex,sourcePath,savePath):
    print(sourcePath,regex)
    global parity
    for parent, dirnames, filenames in os.walk(sourcePath):
        for filename in filenames:
            if re.match(regex, filename, re.IGNORECASE):
                excelPathName = os.path.join(parent,filename)#当前文件路径及文件名
                print('文件路径:', excelPathName)
                try:
                    dataPrevious['dataN'] = getDataFromExcel(excelPathName)
                    # print('全部数据',dataPrevious['dataN'])
                except Exception as err:
                    print('文件读取出错',err)
            # 比较数据是否重复
            flag = [i for i in dataPrevious['dataP'] if i in dataPrevious['dataN'] ]
            if flag.__len__() > 0:
                #利用set去重,取合集,避免遗漏
                dataPrevious['dataN'] = set(dataPrevious['dataN']) | set(dataPrevious['dataP'])
                # print(dataPrevious['dataN'])
            #写入表格操作
            writeExcel(dataPrevious['dataN'],excelPathName,savePath)
            dataPrevious['dataP'] = dataPrevious['dataN']#后读取数据前存
            parity += 1
            dataPrevious['dataP'] = dataPrevious['dataN']
#获取数据,返回示例:oneExcelData[[sheet1],[sheet2],,,]
def getDataFromExcel(excelPathName):
    # 读取文件
    dataCurrentExcel = []
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
            i = 0
            flag = False
            list = []
            for colCell in sheetCurrent.row_values(0):  # 遍历当前sheet第一行
                # print('当前表',x,'的第一行',colCell)
                if re.match('email|e.mail|邮箱', colCell, re.IGNORECASE):  # 如果列表第一行存在email字段栏
                    # print('含有mail字段列',colCell)
                    temp = sheetCurrent.col_values(i)
                    while '' in temp:  # 去除列表为空地址
                        temp.remove('')
                    dataCurrentExcel.extend(temp)
                    flag = True
                    break
                i += 1
            if not flag:  # 第一行不存在mail字样,打印全部数据过滤出邮箱
                emailList = checkThreeRows(sheetCurrent)
                if emailList:
                    dataCurrentExcel.extend(emailList)
    return dataCurrentExcel

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
            if re.match(regex,x):
                sheetHasMail = True
                break
    if sheetHasMail:
        temp = getAllEmail(sheetCurrent.col_values(flag))
        return temp
    else:
        return False

#获取首行包含mail字样列值
def getAllEmail(arg):
    addressList = []
    for i in arg:
        str = i
        regex = r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)'
        result = re.findall(regex,str,re.IGNORECASE)
        for i in range(result.__len__()):
            addressList.append(result[i][0])
    return (addressList)

#写入excel
def writeExcel(data,currentExcelName,savePath):#data可以不需要而直接写入excel提升效率?
    # print("写ru数据表被执行",sourceExcelpath)
    global writeCount
    excelNameCount =  fileCount(savePath) - 1#获取存储文件夹文件数
    # print('获取到文件数',excelNameCount)
        # 30000行数据换一张表
    x = 0#数据列计数
    for i in range(data.__len__()):
        if i % 30000 == 0:
            writeCount += 1
            x = 0
            new_workbook = xlwt.Workbook()
            new_sheet = new_workbook.add_sheet("sheet1")
            sheet2 = new_workbook.add_sheet("sheet2")
            sheet2.write(0,0,currentExcelName)
            excelNameCount += 1
        new_sheet.write(x, 0, data[i])
        new_workbook.save(savePath + str(excelNameCount) + ".xls")
        x += 1

# 获取写入目标文件夹的文件数,用于计数命名
def fileCount(savePath):
    for parent, dirnames, filenames in os.walk(savePath):
        # print(parent)
        # print('文件数..................', filenames.__len__())
        for filename in filenames:
            print('文件名',filename)
        excelNameCount = filenames.__len__()  # 获取当前文件夹写文件数,继续数目新增命名.xls文件
    print('存储路径文件夹文件数',excelNameCount)
    return excelNameCount

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    writeCount = 0
    # long running
    #遍历全部文件
    getAllExcelNames('(.)+\.xls|\.xlsx',"E:/testExcelData",r"E:/excelAddressAll/")#正则表达式,数据源路径,目标路径
    endtime = datetime.datetime.now()
    print('邮件列表获取完成,运行时间:',endtime - starttime)
    print('写入表数', writeCount)