import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "", "db3")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# # 使用 execute() 方法执行 SQL，如果表存在则删除
# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
#
# # 使用预处理语句创建表
# sql = """CREATE TABLE EMPLOYEE (
#          FIRST_NAME  CHAR(20) NOT NULL,
#          LAST_NAME  CHAR(20),
#          AGE INT,
#          SEX CHAR(1),
#          INCOME FLOAT )
#          """
# data = (('nariai_tetsuro@kobelconet.com','222'),( 'rchen@visa.com','222'),( 'dindo.chu@roche.com','222'),('0000','222'))
data =[('s11', 1), ('s21', 2)]
data = tuple(data)
print(type(data))
sql = "insert IGNORE into  email (email,filename) values( %s, %s)"
cursor.executemany(sql, data)
db.commit()
for i in data:
    print(i)

    # try:
    # sql = "insert ignore into email (email,filename) values ('{0}','{1}')".format(str(i),'99')
        # 执行sql语句
    # cursor.execute(sql)
        # 提交到数据库执行
        # 如果发生错误则回滚
        # db.commit()
    # except:
    #     continue
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print("Database version : %s " % data)

# 关闭数据库连接
db.close()