import datetime

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


# 连个list判断重复数据
lista = [1,2,3,4]
listb = [2,8,0,9,1]
listc = [a for a in lista if a in listb]
if listc.__len__() > 0:
    print(listc)
