motor = ["honda","yamaha","suzuki"]
motor[0] = "ducati" #将ducati赋值给列表第一个元素
print (motor)

motor.append("ducati") #append在列表末尾添加元素
motor.insert(3,"idk other brand") #insert在索引3位置添加元素
print (motor)

del motor[-1] #del永久删除列表元素，不可再调用
print (motor)

popped = motor.pop() #pop()默认弹出栈顶元素
popped2 = motor.pop(0) #添加索引弹出指定元素
print (motor)
print (popped) #pop出的元素是赋值语句，可再调用
print (popped2)

too_expensive = "suzuki"
motor.remove(too_expensive) #在列表中删除指定的值，并可以再次调用
print (motor)
print (too_expensive)