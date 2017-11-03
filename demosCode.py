#1匹配邮件地址列
import re
import datetime

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
def getAllFileName(root):
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
