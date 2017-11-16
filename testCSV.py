import pandas as pd

#任意的多组列表
a = [1,2,3]
b = [4,5,6]

#字典中的key值即为csv中列名
dataframe = pd.DataFrame({'':a})

#将DataFrame存储为csv,index表示是否显示行名，default=True
# dataframe.to_csv("E:/test.csv",index=False,sep='')
dataframe.to_csv("E:/test.csv", index = False, mode = 'w')  #w重新写入   mode="a" 继续写入