import pandas as pd

#任意的多组列表
a = [1,2,3]
b = [4,5,6]

#字典中的key值即为csv中列名
dataframe = pd.DataFrame({'':a})

#将DataFrame存储为csv,index表示是否显示行名，default=True
# dataframe.to_csv("E:/test.csv",index=False,sep='')
dataframe.to_csv("E:/test.csv", index = False, mode = 'w')  #w重新写入   mode="a" 继续写入


import re
lis = []

# 灏竣领导力研究中心 clschina
# 博特 bote.com.cn
# 嘉迪圣安 edushine.com
# 卓弈 zytraining.cn
# 易知 kmelearning.com
# 厦门学一 xueyizx.com
# 卓越体验 expjoy.com

str = 'AMA amachina'
# print(re.findall(r'([a-zA-Z]+(.[0-9a-zA-Z]+)+)',str))
# print(re.findall(r'([a-z]+(.?[a-z])+)',str))


#
for line in open("foo.txt"):
    # print(line)
    #提取后缀
    res = re.findall(r'(@?[0-9a-z]+(.[0-9a-z]+)+)',line)
    if not re.match('@',res[0][0]):
        # str = res[0][0]
        email = '@'+ res[0][0]
    # print(res[0][0])
    else:
        email = res[0][0]
    lis.append(email)
#
# print(lis)
for i in lis:
    print(i)