member = ['Zack','Mary','James','Peter','Lilia','Bronya']
print (f"The first list is {member}.")
print (f"But the member {member[1]} can't come coz she's ill.")

member[1] = "Joe"
print (f"The second list is {member}.")
print ("Now we have a bigger table for more people.")

member.insert(0,"Goodenough")
member.append("Planc")
member.insert(2,"Maxwell")
print (f"The third list is {member}.")
print ("But again, the table can't be sent here on time ")

pop0 = member.pop(0)
print (f"Sorry, we can't invite {pop0}.")
pop0 = member.pop(0)
print (f"Sorry, we can't invite {pop0}.")
pop0 = member.pop(0)
print (f"Sorry, we can't invite {pop0}.")
pop0 = member.pop(0)
print (f"Sorry, we can't invite {pop0}.")
pop0 = member.pop(0)
print (f"Sorry, we can't invite {pop0}.")
pop0 = member.pop(0)
print (f"Sorry, we can't invite {pop0}.")
pop0 = member.pop(0)
print (f"Sorry, we can't invite {pop0}.")
print (f"{member[0]} is still invited.")
print (f"{member[1]} is still invited.")

del member[0], member[0]
print (member)