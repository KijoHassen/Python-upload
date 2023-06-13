eg = ['q','w','e','r','t','y']
print(eg[1:3])#索引左闭右开，从零开始
#默认从头开始，到末结束，第三个数为步长
print(eg[-3:])#倒数第三个元素

#for中遍历切片
print(f"\nThe first three letters on the keyboard are:")
for letter in eg[:3]:
    print(letter)

