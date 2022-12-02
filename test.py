import re

str = 'The rain in Spain'

x = re.search(r"\b!@#$%^&*()-_=", str)

if x:
    print(x.span())
else:
    print(x)

print('hello')