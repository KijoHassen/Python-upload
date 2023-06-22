width = (1,2,3,4,5)#元组tuple是不可修改的
height = (6,)#如果只有一个元素，需要加上,
print("The former (w,h) is:")
for w in width:
    print(f"({w},{height[0]})")

width = (10,11,12,13,14)#可以通过重新给元组赋值来修改元组
height = (114514,)
print("\nThe new (w,h) is:")
for w2 in width:
    print(f"({w2},{height[0]})")