"""
=连接的是赋值语句，是共同指向
"""
eg = [1,2,3,4,5,6,7,8]
eg2=eg
print(eg)
print(eg2)

eg.append(9)
eg2.append(0)
print(eg)
print(eg2)
#这行不通，eg,eg2此时共同指向同一个列表

exmp = [0,9,8,7,6,5]
exmp2 = exmp[:]#创建了一个副本再赋值
print(exmp)
print(exmp2)

exmp.append(4)
exmp2.append(3)
print(exmp)
print(exmp2)
#这样就是两个不同列表了