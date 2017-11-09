"""从源数据中copy出错误日志中的文件"""

import shutil
import os
import os.path

# 根据读取文件名复制文件到指定目录
#遍历文件目录
def getFileNames(sourcePath,errLogPath,dst):
    #待遍历源文件路径
    rootdir = sourcePath
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            data = getContentFromTxt(errLogPath)
            for filePath in data:
                if filename in filePath:
                    print('copy文件')
                    shutil.copy(os.path.join(parent, filename), dst)

#获取txt文件内容
def getContentFromTxt(txtFile):
    dataList = []
    # 逐行读
    file_object = open(txtFile)
    try:
        for line in file_object:
            dataList.append(line)
    finally:
        file_object.close()
    # print(dataList)
    return dataList

if __name__ == "__main__":
    errLogPath = "E:/pppresult/errLog.txt"
    sourcePath = "E:/Simon 数据"
    dst = "E:/pppcopyfile/"
    getFileNames(sourcePath,errLogPath,dst)