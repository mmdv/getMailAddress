import datetime
import re

list1 = [1,2,3,4,8,8]
list2 = [2,3,5,8,8]
# list3 = [ i for i in set(list1) if i in set(list2) ]
list1 = list1[1:list1.__len__()]
print('list4',list1[0])
print(set(list1) | set(list2))
# print(list3)

f = open("E:/hello.txt","w")
for i in range(20):
       f.write(str(i))
       f.write("\n")
f.close()
regex = "(.*)email(.*)|(.*)邮箱(.*)|(.*)e(.*)mail(.*)"
if re.match(regex,'Bill to:email'):
    print('匹配')
else:
    print('no')


























for i in range(3):
    flag = 0
    for x in range(8):
        flag +=1
        if(x ==3):
            break
print(flag)

r = False
if not r :
    print(999)

data = []
for i in range(30000):
    data.append(i)

    starttime = datetime.datetime.now()

x = 29999
for i in range(30000):
    if x < data[i]:
        print('kkkk')

endtime = datetime.datetime.now()
print(endtime-starttime)
color = []
if not color:
    print('911')

data = [1,2,3]
print(data.__len__())
datar = [[]for i in range(data.__len__())]

for i in range(10):
    datar[0].append(i)
for i in range(7):
    datar[1].append(i)
datar.extend(datar[0])

print(datar)
# print(datar[1])


lista = ['', '', '', '', '', '', '', '', '', '', '']

for i in lista:
    print('aa',i)
if lista:
    print('aaa')