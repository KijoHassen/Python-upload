cars = ['byd','bmw','benz','audi','toyota']

for car in cars:
    if car == "byd":
        print(car.upper())
    else:
        print(car.title())
###
archon = "Zhongli"

if archon != "RaidenEi":
    print(f"\nThe correct name is {archon}.")
###
names = ['zhangsan','lisi','wangwu','zhaoliu','qianqi']
name_1 = 'hutao'
name_2 = 'zhangsan'

if name_1 in names:
    print(f"\nYou are invited.")
else:
    print(f"\nYou are not invited.")

if name_2 not in names:
    print(f"\nYou are not invited.")
else:
    print(f"\nYou are invited.")
###