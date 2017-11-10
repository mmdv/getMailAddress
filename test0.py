'''
该函数主要参数为:excel_writer。
excel_writer:写入的目标excel文件，可以是文件路径、ExcelWriter对象;
sheet_name:被写入的sheet名称，string类型，默认为'sheet1';
na_rep:缺失值表示，string类型;
header:是否写表头信息，布尔或list of string类型，默认为True;
index:是否写行号，布尔类型，默认为True;
encoding:指定写入编码，string类型。
'''
from openpyxl import Workbook
data = [1,2,3]
wb = Workbook()
# 创建一个工作表，然后
sheet = wb.active
# 找到活动的sheet页。空的excel表默认的sheet页就叫Sheet，如果想改名字，可以直接给title属性赋值。
sheet.title = "sheet1"
# 这个属性是可读可写的。当然，这个只针对当前活动页，别的页的话，可以用create_sheet和remove_sheet进行添加和删除。
# 往sheet页里面写内容就比较简单了，跟上面读一样，
sheet['C3'] = 'Hello world!'
for i in range(data.__len__()):
  sheet["A%d" % (i+1)].value = data[i]
# 我们还可以进行花式操作，比如写写公式：
sheet["E1"].value = "=SUM(A:A)"
# 最后记得保存
wb.save('E:/output1.xlsx')

