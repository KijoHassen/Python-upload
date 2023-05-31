people = ['bronya','jingyuan','welt yang','stella']
for person in people:
    print(f"{person.title()}, could you join in my team?")
    print(f"I need your help, {person.title()}.\n") #在同一个缩进下的语句是迭代输出的一个整体，参见下文。
"""
读取for 单数 in 复数列表，并将第n个值赋给单数变量
重复调用变量，直到遍历结束。
"""
print("Thank you, everyone!\n")

"""
以下是典型的缩进错误
"""
for person in people:
    print(f"{person.title()}, could you join in my team?")
    print(f"I need your help, {person.title()}.")
    print("Thank you, everyone!\n") #本句不应出现在迭代整体之内