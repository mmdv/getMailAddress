#1判断字符串是否包含字符串
# 第一种方法：in
string = 'helloworld'
if 'world' in string:
    print( 'Exist')
else:
    print( 'Not exist')
# 第二种方法：find
string = 'helloworld'
if string.find('world') == 5: #5的意思是world字符从那个序开始，因为w位于第六个，及序为5，所以判断5
    print( 'Exist')
else:
    print('Not exist')
# 第三种方法：index，此方法与find作用类似，也是找到字符起始的序号
if string.index('world') > -1: #因为-1的意思代表没有找到字符，所以判断>-1就代表能找到
    print('Exist')
else:
    print( 'Not exist')