import re

fileName = 'E:/pppsource\VIK\VIK-12.7.25\Finance 10w.csv'
data = ['3334@qq.cmo','fish-yu-@qq.com','15651610029@js.chinaunicom.com+','--loreal_intern@126.com.','还有这22@qq.com','635347773@qq.com','fish.yu@j-and-s.cn','--huliang@cernet.com--','e-e@ll-ll.com.cn','--聊了10几分钟后竟然说不考虑啦guojie1211@hotmail.com','.233@qq.com']
# regex = r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)'    #存在问题,第一个值会被匹配到
# regex = '^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+'    #匹配
# regex = '^[A-Za-zd]+([-_.][A-Za-zd]+)*@([A-Za-zd]+[-.])+[A-Za-zd]{2,5}$'  #匹配
# regex = r"([a-zA-Z0-9_.+-]+@[a-pr-zA-PRZ0-9-]+\.[a-zA-Z0-9-.]+)"       #查找,过滤qq邮箱
# regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"             #查找,有问题  匹配----
# regex = "([a-zA-Z0-9][a-zA-Z0-9.-_+]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9]+){2,3})"             #查找,后缀长度不正确
# regex = '(([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3})'
regex = '([a-zA-Z0-9][a-zA-Z0-9.\-\_+]+@([a-zA-Z0-9]+[\-_\.+]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3})' #匹配完全
# regex = r'([a-zA-Z0-9][a-zA-Z0-9.\-_+]+@([a-zA-Z0-9]+[-_.+]?)*[a-zA-Z0-9]+.[a-zA-Z]{2,3})'
print(data.__len__())
result = re.findall(regex,str(data),re.IGNORECASE)
for i in result:
    print(i[0])
print(result.__len__())
# dat = []
# for i in result:
#     print(i)
# for i in range(result.__len__()):
#     dat.append(result[i][0])
# print(dat)


rs = [[]]

if not rs:
    print(999999)

