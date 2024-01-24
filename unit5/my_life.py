age = 18

if age < 2:
    stat = 'baby'
elif age < 4:
    stat = 'kid'
elif age < 13:
    stat = 'child'
elif age < 20:
    stat = 'teenager'
elif age < 65:
    stat = 'adult'
else:
    stat = 'senior'
    

print(f"This guy is {age} year(s) old now,\nso he or she is a {stat}.")