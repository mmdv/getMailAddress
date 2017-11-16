import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "", "db3")

cursor = db.cursor()

data =[('s11', 1), ('s21', 2)]
print ('10%4 = ', 10%4)
data = tuple(data)
print(type(data))
limits = 300
print(824%300)
result = []
# sql = "insert IGNORE into  email (email,filename) values( %s, %s)"
sqlall = "SELECT * FROM emailtest ORDER BY id asc"
sql = "SELECT * FROM emailtest ORDER BY id asc LIMIT 0,300"
sql1 = "SELECT email FROM emailtest ORDER BY id asc LIMIT {},{}".format(300,300)
# sql = "DELETE FROM EMAILTEST WHERE EMAIL = '{}'".format('wang.zongyin@zte.com.cn')
sql = "select * from emailtest where email = '{}'".format('8009130000@163.com')
cursor.execute(sql)
print(cursor.fetchall())
# db.commit()

# print('直接查询',cursor.fetchone())
# if 824 == cursor.fetchone():
#     print('直接查询',type(cursor.fetchone()))
# temp = cursor.fetchone()
# print(temp,'----------------')
# len = temp
# print('templen',len[0])
# print(len[0] % 300 + 1)
# for i in range(int(len[0] / 300) + 1):
#
#     sql = "SELECT * FROM emailtest ORDER BY id asc LIMIT {},{}".format(i*300,(i+1)*300)
#     cursor.execute(sql)
#     data = cursor.fetchall()
#     result.extend(data)
# print('result',result.__len__())
# for i in result:
#     print(i)
# cursor.execute(sqlall)
# data = cursor.fetchall()
# print('dataalll',data.__len__())
#
# # db.commit()
# print('----------------------------',data.__len__())
#
#     # try:
#     # sql = "insert ignore into email (email,filename) values ('{0}','{1}')".format(str(i),'99')
#         # 执行sql语句
#     # cursor.execute(sql)
#         # 提交到数据库执行
#         # 如果发生错误则回滚
#         # db.commit()
#     # except:
#     #     continue
# cursor.execute("SELECT VERSION()")
#
# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
#
# print("Database version : %s " % data)

# 关闭数据库连接
db.close()