name = "zaCK brIGht" #输入的信息是大小写混杂的
print (name.title()) #标题样式，首字母大写
print (name.upper()) #全部大写
print (name.lower()) #全部小写

first_name = "Kijo"
second_name = "Hassen"
full_name = f"{first_name} {second_name}" #f字符串 f是format的缩写，调用{}内的变量替换为其值
#上面两个{}之间的空格是会被输出的
print (full_name)
print (f"Hello, {full_name.upper()}!") #f字符串内也可以添加其他字符

greeting_message = f"Hi, {full_name.upper()}!" #将f字符串赋值给一般字符串再输出
print (greeting_message)

name2 = (" zack-bright ") #字符串内空格会被输出
print (name2.lstrip())
print (name2.rstrip())
print (name2.strip())

str = "this is a sentence,\nthis, too,\nthis, of course, too."
print (str)

CONSTANT = "299792458" #一般将常量全部大写