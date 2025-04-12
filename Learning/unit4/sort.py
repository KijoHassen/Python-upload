cars = ['bmw','audi','byd','toyota']
cars.sort() #按首字母排序，sort修改是永久的
print(cars)

cars.sort(reverse=True)
print(cars)

print("\n1st:")
print(cars)

print("\n2nd:")
print(sorted(cars)) #sorted排序是临时的

print("\n3th:")
print(sorted(cars,reverse=True))

cars.reverse() #reverse倒序是永久的
print(f"\n{cars}")

print(len(cars)) #len()确定列表长度