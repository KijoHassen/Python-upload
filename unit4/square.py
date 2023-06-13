squares = []#empty list
for i in range(1,11):#遍历
    square = i**2#计算并赋值给临时变量
    squares.append(square)#不断将临时变量赋给空列表
print(squares)

"""优化代码，不使用临时变量"""
cubes = []
for j in range(1,11):
    cubes.append(j**3)#直接给cubes变量append上j的立方即可
print(cubes)

"""列表解析"""
squares_2 = [value**2 for value in range(1,11)]
print(squares_2)
#相当于定语从句