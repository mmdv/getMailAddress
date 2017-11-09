import re

fileName = 'E:/pppsource\VIK\VIK-12.7.25\Finance 10w.csv'
data = ['22@qq.com','33@ww.com']
regex = r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)'

result = re.findall(regex,str(data),re.IGNORECASE)
print(result)
dat = []
for i in result:
    print(i)
for i in range(result.__len__()):
    dat.append(result[i][0])
print(dat)


rs = []

if not rs:
    print(999999)