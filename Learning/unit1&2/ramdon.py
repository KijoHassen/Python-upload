import random

# 定义一个目标子串
GRAMMAR = "ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789"


def random_str1(length):
    #生成随机长度str
    target = ""
    grammar_length = len(GRAMMAR)-1
    if length > 0:
        for i in range(length):
            tmp_str = random.choice(GRAMMAR)	# 使用random.choice()
            tmp_str = GRAMMAR[random.randint(0, grammar_length)]	# 使用random.randint()
            target += tmp_str
        return target
    else:
        raise IndexError()
        

# 测试用例
print("", random_str1(82))